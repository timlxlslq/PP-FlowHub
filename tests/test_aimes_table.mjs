import assert from "node:assert/strict";
import fs from "node:fs";
import { chromium } from "playwright";
import { readAimesTable } from "../tools/aimes_table.mjs";

const HEADERS = ["工厂单号", "工厂单名称", "销售单名称", "拆单时间"];

// 生成测试表格 HTML；headers 为列标题，rows 为二维单元格数据。
const tableMarkup = (headers = HEADERS, rows = []) => `
  <div id="factory-table" class="el-table">
    <table>
      <thead><tr>${headers.map(/* 将标题包入表头单元格；header 为当前标题文本。 */ header => `<th>${header}</th>`).join("")}</tr></thead>
      <tbody>${rows.map(/* 将一行数据包入表格行；row 为当前行的单元格数组。 */ row => `<tr>${row.map(/* 将值包入数据单元格；value 为单元格内容。 */ value => `<td>${value}</td>`).join("")}</tr>`).join("")}</tbody>
    </table>
  </div>`;

// 生成含工厂单搜索框的测试页面；body 为要插入的页面 HTML。
const pageMarkup = body => `
  <input placeholder="请输入工厂单号">
  ${body}
`;

// 在独立页面中运行回归并确保关闭页面。
// browser 为浏览器实例；body 为页面 HTML；test 为接收 page 的异步测试回调。
async function withPage(browser, body, test) {
  const page = await browser.newPage();
  try {
    await page.route("**/*", /* 阻止页面外部请求；route 为被拦截的网络请求。 */ route => route.abort());
    await page.setContent(pageMarkup(body));
    return await test(page);
  } finally {
    await page.close();
  }
}

// 启动离线浏览器，验证表头、数据和加载遮罩的等待规则及错误分类。
// 参数：无；完成或失败后均关闭浏览器。
async function main() {
  const configuredBrowser = process.env.TRAVELER_BROWSER_EXECUTABLE || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
  const browserOptions = {
    headless: true,
    args: ["--no-first-run", "--no-default-browser-check"],
  };
  if (fs.existsSync(configuredBrowser)) browserOptions.executablePath = configuredBrowser;
  const browser = await chromium.launch({
    ...browserOptions,
  });
  try {
    await withPage(browser, "", /* 验证输入框先出现时仍等待表头和数据；page 为隔离测试页面。 */ async page => {
      await page.evaluate(/* 延迟插入整张表格；markup 为待插入的表格 HTML。 */ ({ markup }) => {
        setTimeout(/* 延迟创建表格，模拟异步加载；无参数。 */ () => document.body.insertAdjacentHTML("beforeend", markup), 60);
      }, { markup: tableMarkup(HEADERS, [["F100", "Kitchen", "PP001", "2026-09-11"]]) });
      const result = await readAimesTable(page, { timeoutMs: 1000 });
      assert.deepEqual(result.headers, HEADERS, "输入框先出现时应等待表头");
      assert.deepEqual(result.rows, [["F100", "Kitchen", "PP001", "2026-09-11"]], "输入框先出现时应等待行");
    });

    await withPage(browser, tableMarkup(), /* 验证表头先出现时继续等待数据行；page 为隔离测试页面。 */ async page => {
      await page.evaluate(/* 安排数据行的延迟更新，模拟页面异步渲染；无参数。 */ () => {
        setTimeout(/* 加入稍后才出现的数据行；无参数。 */ () => {
          document.querySelector("tbody").innerHTML = "<tr><td>F101</td><td>Office</td><td>PP002</td><td>2026-09-12</td></tr>";
        }, 60);
      });
      const result = await readAimesTable(page, { timeoutMs: 1000 });
      assert.deepEqual(result.rows, [["F101", "Office", "PP002", "2026-09-12"]], "表头先出现时不能提前返回空行");
    });

    await withPage(browser, `
      ${tableMarkup(HEADERS, [["F104", "Delayed header", "PP004", "2026-09-14"]])}
    `, /* 验证表头节点文字延迟时仍继续等待；page 为隔离测试页面。 */ async page => {
      await page.locator("th").first().evaluate(/* 临时清空表头文字并延迟恢复；node 为首个表头元素。 */ node => {
        const text = node.firstChild;
        if (text) text.nodeValue = "";
        setTimeout(/* 恢复表头文字，模拟延迟渲染；无参数。 */ () => { node.textContent = "工厂单号"; }, 60);
      });
      const result = await readAimesTable(page, { timeoutMs: 1000, requireMetadata: true });
      assert.deepEqual(result.headers, HEADERS, "表头节点先出现但文字延后时应继续等待");
      assert.deepEqual(result.rows, [["F104", "Delayed header", "PP004", "2026-09-14"]]);
    });

    await withPage(browser, `
      <div class="el-loading-mask" id="visible-loading" style="width:10px;height:10px"></div>
      <div class="el-loading-mask" id="hidden-loading" style="display:none"></div>
      ${tableMarkup(HEADERS, [["FOLD", "旧数据", "OLD", "旧时间"]])}
    `, /* 验证可见加载遮罩阻止读取旧行，隐藏遮罩不阻塞；page 为隔离测试页面。 */ async page => {
      await page.evaluate(/* 安排加载结束和数据替换；无参数。 */ () => {
        setTimeout(/* 隐藏可见遮罩并替换旧数据行；无参数。 */ () => {
          document.querySelector("#visible-loading").style.display = "none";
          document.querySelector("tbody").innerHTML = "<tr><td>F102</td><td>Fresh</td><td>PP003</td><td>2026-09-13</td></tr>";
        }, 60);
      });
      const result = await readAimesTable(page, { timeoutMs: 1000 });
      assert.deepEqual(result.rows, [["F102", "Fresh", "PP003", "2026-09-13"]], "可见加载遮罩期间不得读取旧行，隐藏遮罩不应阻塞");
    });

    await withPage(browser, `
      ${tableMarkup(HEADERS)}
      <div class="el-table__empty-block"><span>暂无数据</span></div>
    `, /* 验证明确空状态返回空行数组；page 为隔离测试页面。 */ async page => {
      const result = await readAimesTable(page, { timeoutMs: 500 });
      assert.deepEqual(result.rows, [], "明确 empty 状态应返回空行");
    });

    await withPage(browser, `
      ${tableMarkup(HEADERS)}
      <table aria-label="ant-empty-table">
        <tbody><tr class="ant-table-placeholder"><td colspan="4">
          <div class="ant-empty"><div class="ant-empty-description">暂无数据</div></div>
        </td></tr></tbody>
      </table>
    `, /* 验证表体中的 Ant 空表占位符返回空行数组；page 为隔离测试页面。 */ async page => {
      const result = await readAimesTable(page, { timeoutMs: 500 });
      assert.deepEqual(result.rows, [], "tbody 内 Ant 空表占位行应返回空行");
    });

    await withPage(browser, tableMarkup(["工厂单号", "工厂单名称"], [["F103", "Missing metadata"]]), /* 验证缺少必要列时报告结构错误；page 为隔离测试页面。 */ async page => {
      await assert.rejects(
        /* 触发要求完整元数据的表格读取；无参数。 */ () => readAimesTable(page, { timeoutMs: 500, requireMetadata: true }),
        /* 判断拒绝原因是否为缺列错误；error 为捕获到的异常。 */ error => error instanceof Error && error.message.includes("AIMES 工厂订单表缺少必要列"),
        "实际缺列必须报告 AIMES schema 失败"
      );
    });

    await withPage(browser, "", /* 验证一直没有表格时报告专用未就绪错误；page 为隔离测试页面。 */ async page => {
      await assert.rejects(
        /* 在短时限内读取始终未就绪的表格；无参数。 */ () => readAimesTable(page, { timeoutMs: 120, requireMetadata: true }),
        /* 判断拒绝原因是否为表格未就绪；error 为捕获到的异常。 */ error => error instanceof Error && error.message.includes("AIMES_TABLE_NOT_READY"),
        "始终未就绪必须使用专用超时错误"
      );
    });
  } finally {
    await browser.close();
  }
  console.log("AIMES table offline regression tests passed");
}

await main();
