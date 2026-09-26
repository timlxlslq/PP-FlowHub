"""
这个文件是专门用于管理企业微信相关接口等，包括读取写入智能文档。
"""
import json
import subprocess
import sqlite3
import database
import traceback
from pathlib import Path
from typing import Any



def _run_wecom_command(args):
    """运行企微命令并解析 JSON，移除附带身份上下文；args 为子命令及参数列表。"""
    result = subprocess.run(
        ["wecom-cli", *args],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    data = json.loads(result.stdout)

    data.pop("extra_identity_context", None)

    return data


def get_smartsheet_info(doc_url):
    """读取智能表格信息；doc_url 为传给企微命令的文档标识或链接。"""
    return _run_wecom_command(
        [
            "smartsheet",
            "get",
            "--docid",
            doc_url,
        ]
    )


# 接口单次最多 1000 条，且要求 limit × 列数 < 10000。
# 100 是每一页的条数，不是总上限；get_records 会翻页直到读完。
_RECORDS_PAGE_LIMIT = 100


def get_records(doc_url, sheet_id):
    """分页拉取子表记录并合并；doc_url 为文档标识或链接，sheet_id 为子表标识。"""
    all_records = []
    cursor = None
    last_page = {}

    while True:
        args = [
            "smartsheet",
            "records",
            "list",
            "--docid",
            doc_url,
            "--sheet-id",
            sheet_id,
            "--type",
            "records",
            "--limit",
            str(_RECORDS_PAGE_LIMIT),
        ]
        if cursor:
            args.extend(["--cursor", cursor])

        last_page = _run_wecom_command(args)
        page_records = last_page.get("records") or []
        all_records.extend(page_records)

        # has_more 为假，或没有下一页游标，说明已经读完。
        if not last_page.get("has_more"):
            break
        cursor = last_page.get("next_cursor")
        if not cursor or not page_records:
            break

    result = dict(last_page)
    result["records"] = all_records
    result["has_more"] = False
    result.pop("next_cursor", None)
    return result

def get_text(values, field_name):
    """提取文本字段，兼容文本列表和字符串；values 为字段字典，field_name 为字段名称。"""
    field_value = values.get(field_name)

    """
    if field_value and isinstance(field_value, list):
        return field_value[0].get("text")
    return None
    """
    match field_value:

        # 1. 匹配列表：列表第一个元素是字典，且包含 'text' 键
        # (适用于 PP No, Order Status, Note 等)
        case [{"text": text}, *_]:
            return text

        # 2. 直接是字符串 (适用于 Pick Up Date)
        case str(): 
            return field_value

        # 3. 其他所有情况（None、空列表 []、数字等）    
        case _:
            return None

class WeComRepository:
    """wecom模块专用的数据仓库，独立管理数据库连接与事务"""

    def __init__(self, state_dir: Path):
        """设置状态目录 state_dir 并确保数据库结构已创建。"""
        # database_path() 用 Path 的 / 拼接文件名；字符串没有这个运算。
        self.state_dir = Path(state_dir)
        self.db_path = database.database_path(self.state_dir)

        # 初始化时确保数据库及所有表结构已创建
        database.ensure_schema(self.db_path)

    def _get_connection(self) -> sqlite3.Connection:
        """创建启用外键的新 SQLite 连接；无显式参数，使用当前仓库的数据库路径。"""
        conn = sqlite3.connect(self.db_path)
        # 开启外键支持（推荐）
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def get_db_order_status(self, order_id: str) -> list[tuple]:
        """按 order_id 查询本地订单状态；发生异常时打印诊断信息，并始终关闭连接。"""
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT order_id, stage FROM orders WHERE order_id = ?",
                (order_id,)
            )
            return cursor.fetchall()
        except Exception as e:
        # 2. 只有当 try 块报错时，才会进入这里
          print(f"捕获到异常简报: {e}")
    
        # 如果想输出详细的报错堆栈信息（包含报错具体在哪一行）：
          print("详细报错堆栈如下：")
          traceback.print_exc()

        finally:
            conn.close()

    def update_wecom_order_status(self, order_id: str) -> list[tuple]:
        """预留企微订单状态更新接口，当前尚未实现；order_id 为待更新订单号。"""


if __name__ == "__main__":
    url = "https://doc.weixin.qq.com/smartsheet/s3_AYUASwYkAGICNMtHJEcNaRtajUemi"

    data = get_records(
        doc_url=url,
        sheet_id="q979lj",
    )

    records = data["records"]

    print("总记录数：", len(records))

    order_list = []
    pp_no_seen_list = set()
    pp_no_duplicates_list = set()

    for record in records:
       values = record.get("values")
       if not values:
          continue

       order_value = values.get("PP No")
       order = {}

       if not order_value:
          continue

       pp_no = order_value[0]["text"]
       pp_no = pp_no.upper()
       if pp_no in pp_no_seen_list:
          pp_no_duplicates_list.add(pp_no)
       else:
          pp_no_seen_list.add(pp_no)

       order = {
        "pp_no": order_value[0]["text"],
        "record_id": record.get("record_id"),
        "order_status": get_text(values, "Order Status"),
        "pick_up_date": get_text(values, "Pick Up Date"),
        "note": get_text(values, "Note")
       }
       order_list.append(order)

    #print(order_list)
    if pp_no_duplicates_list:
        print(f"重复订单号：“ {pp_no_duplicates_list}")

    """
    wecomrepository = WeComRepository(Path.home() / "Documents/pp-flowhub/data")
    wecomrepository._get_connection()
    orderlist1 = wecomrepository.get_db_order_status("PP0070")
    print(orderlist1)
    """
