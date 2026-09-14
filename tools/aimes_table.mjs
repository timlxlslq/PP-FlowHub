const REQUIRED_HEADERS = ["工厂单号", "工厂单名称", "销售单名称", "拆单时间"];
const tableSnapshot = page => page.evaluate(() => {
  const isVisible = element => {
    if (!element || element.getClientRects().length === 0) return false;
    const style = window.getComputedStyle(element);
    return style.display !== "none" && style.visibility !== "hidden" &&
      style.visibility !== "collapse" && style.opacity !== "0";
  };
  const text = element => String(element?.textContent || "").trim();
  const loadingSelectors = [
    ".el-loading-mask",
    ".el-loading-spinner",
    ".ant-spin-spinning",
    "[aria-busy='true']",
  ];
  const emptySelectors = [
    ".el-table__empty-block",
    ".el-table__empty-text",
    ".ant-empty",
    ".ant-empty-description",
  ];
  const visibleMatch = selectors => selectors.some(selector =>
    Array.from(document.querySelectorAll(selector)).some(isVisible));
  const emptyRow = row => {
    if (emptySelectors.some(selector => row.matches(selector) || row.querySelector(selector))) return true;
    const values = Array.from(row.querySelectorAll("td")).filter(isVisible).map(text);
    const nonEmptyValues = values.filter(Boolean);
    return nonEmptyValues.length === 1 && /^(?:暂无数据|暂无|无数据|no data)$/i.test(nonEmptyValues[0]);
  };
  const headerRows = Array.from(document.querySelectorAll("thead tr")).filter(isVisible);
  const candidates = headerRows.map(row =>
    Array.from(row.querySelectorAll("th")).filter(isVisible).map(text));
  const headers = candidates.reduce(
    (longest, candidate) => candidate.length > longest.length ? candidate : longest,
    [],
  );
  const rows = [];
  let emptyRowVisible = false;
  for (const row of Array.from(document.querySelectorAll("tbody tr")).filter(isVisible)) {
    if (emptyRow(row)) {
      emptyRowVisible = true;
      continue;
    }
    const values = Array.from(row.querySelectorAll("td")).filter(isVisible).map(text);
    if (values.length > 0) rows.push(values);
  }
  return {
    headers,
    rows,
    loadingVisible: visibleMatch(loadingSelectors),
    emptyVisible: emptyRowVisible || visibleMatch(emptySelectors),
  };
});

const diagnostic = snapshot =>
  `表头=${snapshot.headers.join(" | ")}; 行数=${snapshot.rows.length}; ` +
  `可见加载状态=${snapshot.loadingVisible ? "是" : "否"}; ` +
  `空表占位=${snapshot.emptyVisible ? "是" : "否"}`;

const missingRequiredHeaders = headers =>
  REQUIRED_HEADERS.filter(alias => !headers.some(header => header === alias || header.includes(alias)));

const notReadyError = (snapshot, timeoutMs) => {
  const error = new Error(`AIMES_TABLE_NOT_READY：AIMES 工厂订单表在 ${timeoutMs}ms 内未就绪；诊断：${diagnostic(snapshot)}`);
  error.code = "AIMES_TABLE_NOT_READY";
  return error;
};

const schemaError = (headers, missing) => {
  const error = new Error(`AIMES 工厂订单表缺少必要列；当前表头：${headers.join(" | ")}`);
  error.code = "AIMES_TABLE_SCHEMA";
  error.missingColumns = missing;
  return error;
};

/** Wait for and read the visible AIMES factory-order table without accepting a transient empty tbody. */
export async function readAimesTable(page, { timeoutMs = 15000, requireMetadata = true } = {}) {
  const deadline = Date.now() + Math.max(1, Number(timeoutMs) || 15000);
  let snapshot = await tableSnapshot(page);
  const isBaseReady = current =>
    current.headers.some(header => header.length > 0) &&
    !current.loadingVisible &&
    (current.rows.length > 0 || current.emptyVisible);
  while (!isBaseReady(snapshot) || (requireMetadata && missingRequiredHeaders(snapshot.headers).length > 0)) {
    const remaining = deadline - Date.now();
    if (remaining <= 0) {
      if (isBaseReady(snapshot) && requireMetadata) {
        throw schemaError(snapshot.headers, missingRequiredHeaders(snapshot.headers));
      }
      throw notReadyError(snapshot, timeoutMs);
    }
    await page.waitForTimeout(Math.min(250, remaining));
    snapshot = await tableSnapshot(page);
  }

  if (requireMetadata) {
    const missing = missingRequiredHeaders(snapshot.headers);
    if (missing.length > 0) throw schemaError(snapshot.headers, missing);
  }
  return { headers: snapshot.headers, rows: snapshot.rows };
}
