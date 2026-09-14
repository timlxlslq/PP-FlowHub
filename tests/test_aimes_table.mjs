import assert from "node:assert/strict";
import fs from "node:fs";
import { chromium } from "playwright";
import { readAimesTable } from "../tools/aimes_table.mjs";

const HEADERS = ["工厂单号", "工厂单名称", "销售单名称", "拆单时间"];

const tableMarkup = (headers = HEADERS, rows = []) => `
  <div id="factory-table" class="el-table">
    <table>
      <thead><tr>${headers.map(header => `<th>${header}</th>`).join("")}</tr></thead>
      <tbody>${rows.map(row => `<tr>${row.map(value => `<td>${value}</td>`).join("")}</tr>`).join("")}</tbody>
    </table>
  </div>`;

const pageMarkup = body => `
  <input placeholder="请输入工厂单号">
  ${body}
`;

async function withPage(browser, body, test) {
  const page = await browser.newPage();
  try {
    await page.route("**/*", route => route.abort());
    await page.setContent(pageMarkup(body));
    return await test(page);
  } finally {
    await page.close();
  }
}

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
    await withPage(browser, "", async page => {
      await page.evaluate(({ markup }) => {
        setTimeout(() => document.body.insertAdjacentHTML("beforeend", markup), 60);
      }, { markup: tableMarkup(HEADERS, [["F100", "Kitchen", "PP001", "2026-09-11"]]) });
      const result = await readAimesTable(page, { timeoutMs: 1000 });
      assert.deepEqual(result.headers, HEADERS, "输入框先出现时应等待表头");
      assert.deepEqual(result.rows, [["F100", "Kitchen", "PP001", "2026-09-11"]], "输入框先出现时应等待行");
    });

    await withPage(browser, tableMarkup(), async page => {
      await page.evaluate(() => {
        setTimeout(() => {
          document.querySelector("tbody").innerHTML = "<tr><td>F101</td><td>Office</td><td>PP002</td><td>2026-09-12</td></tr>";
        }, 60);
      });
      const result = await readAimesTable(page, { timeoutMs: 1000 });
      assert.deepEqual(result.rows, [["F101", "Office", "PP002", "2026-09-12"]], "表头先出现时不能提前返回空行");
    });

    await withPage(browser, `
      ${tableMarkup(HEADERS, [["F104", "Delayed header", "PP004", "2026-09-14"]])}
    `, async page => {
      await page.locator("th").first().evaluate(node => {
        const text = node.firstChild;
        if (text) text.nodeValue = "";
        setTimeout(() => { node.textContent = "工厂单号"; }, 60);
      });
      const result = await readAimesTable(page, { timeoutMs: 1000, requireMetadata: true });
      assert.deepEqual(result.headers, HEADERS, "表头节点先出现但文字延后时应继续等待");
      assert.deepEqual(result.rows, [["F104", "Delayed header", "PP004", "2026-09-14"]]);
    });

    await withPage(browser, `
      <div class="el-loading-mask" id="visible-loading" style="width:10px;height:10px"></div>
      <div class="el-loading-mask" id="hidden-loading" style="display:none"></div>
      ${tableMarkup(HEADERS, [["FOLD", "旧数据", "OLD", "旧时间"]])}
    `, async page => {
      await page.evaluate(() => {
        setTimeout(() => {
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
    `, async page => {
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
    `, async page => {
      const result = await readAimesTable(page, { timeoutMs: 500 });
      assert.deepEqual(result.rows, [], "tbody 内 Ant 空表占位行应返回空行");
    });

    await withPage(browser, tableMarkup(["工厂单号", "工厂单名称"], [["F103", "Missing metadata"]]), async page => {
      await assert.rejects(
        () => readAimesTable(page, { timeoutMs: 500, requireMetadata: true }),
        error => error instanceof Error && error.message.includes("AIMES 工厂订单表缺少必要列"),
        "实际缺列必须报告 AIMES schema 失败"
      );
    });

    await withPage(browser, "", async page => {
      await assert.rejects(
        () => readAimesTable(page, { timeoutMs: 120, requireMetadata: true }),
        error => error instanceof Error && error.message.includes("AIMES_TABLE_NOT_READY"),
        "始终未就绪必须使用专用超时错误"
      );
    });
  } finally {
    await browser.close();
  }
  console.log("AIMES table offline regression tests passed");
}

await main();
