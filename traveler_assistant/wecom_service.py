"""
这个文件是专门用于管理企业微信相关接口等，包括读取写入智能文档。
"""
import json
import subprocess
import sqlite3
import database
from pathlib import Path
from typing import Any



def _run_wecom_command(args):
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
    return _run_wecom_command(
        [
            "smartsheet",
            "get",
            "--docid",
            doc_url,
        ]
    )


def get_records(doc_url, sheet_id, limit=100):
    return _run_wecom_command(
        [
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
            str(limit),
        ]
    )

def get_text(values, field_name):
    """安全提取 SmartSheet 文本字段"""
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
    """企微模块专用的数据仓库，独立管理数据库连接与事务"""

    def __init__(self, state_dir: Path):
        self.state_dir = state_dir
        self.db_path = database.database_path(state_dir)
        
        # 初始化时确保数据库及所有表结构已创建
        database.ensure_schema(self.db_path)

    def _get_connection(self) -> sqlite3.Connection:
        """创建一个全新的 SQLite 连接（随用随开）"""
        conn = sqlite3.connect(self.db_path)
        # 开启外键支持（推荐）
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def save_outbound_record(self, record_data: dict[str, Any]) -> bool:
        """保存企微读取到的出库单数据"""
        doc_number = record_data.get("document_number", "").strip()
        if not doc_number:
            return False

        # 使用 Context Manager 自动管理事务（提交/回滚）
        with self._get_connection() as conn:
            # 1. 写入出库主单
            conn.execute(
                """
                INSERT INTO outbound_documents(
                    document_number, document_type, order_id, factory_order, 
                    status, source, source_path, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(document_number) DO UPDATE SET
                    status = excluded.status,
                    updated_at = excluded.updated_at
                """,
                (
                    doc_number,
                    record_data.get("document_type", ""),
                    record_data.get("order_id", ""),
                    record_data.get("factory_order", ""),
                    record_data.get("status", "recorded"),
                    "wecom",
                    record_data.get("source_path", ""),
                    database._now()  # 复用 database.py 的时间生成函数
                )
            )

            # 2. 复用 database.py 现成的辅助函数，建立出库单与工厂订单的关联
            database.ensure_outbound_document_factory_links(
                connection=conn,
                document_number=doc_number,
                order_id=record_data.get("order_id", ""),
                factory_value=record_data.get("factory_order", ""),
                updated_at=database._now()
            )

        return True

    def get_pending_documents(self) -> list[tuple]:
        """查询企微模块需要的单据"""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT document_number, order_id, status FROM outbound_documents WHERE source = 'wecom'"
            )
            return cursor.fetchall()

if __name__ == "__main__":
    url = "https://doc.weixin.qq.com/smartsheet/s3_AYUASwYkAGICNMtHJEcNaRtajUemi"

    data = get_records(
        doc_url=url,
        sheet_id="q979lj",
        limit=100,
    )

    records = data["records"]

    print("总记录数：", len(records))

    order_list = []

    for record in records:
       values = record.get("values")
       if not values:
          continue

       order_value = values.get("PP No")
       order = {}

       if not order_value:
          continue

       order = {
        "pp_no": order_value[0]["text"],
        "order_status": get_text(values, "Order Status"),
        "pick_up_date": get_text(values, "Pick Up Date"),
        "note": get_text(values, "Note")
       }
       order_list.append(order)

    print(order_list)