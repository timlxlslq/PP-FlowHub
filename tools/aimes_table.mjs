const REQUIRED_HEADERS = ["工厂单号", "工厂单名称", "销售单名称", "拆单时间"];
/** 读取可见工厂单表头、数据行及加载和空表标志。
 * 参数：page：AIMES 浏览器页面。
 */
const tableSnapshot = page => page.evaluate(() => {
  /** 根据布局矩形与计算样式判断元素是否可见。
   * 参数：element：待检查的页面元素。
   */
  const isVisible = element => {
    if (!element || element.getClientRects().length === 0) return false;
    const style = window.getComputedStyle(element);
    return style.display !== "none" && style.visibility !== "hidden" &&
      style.visibility !== "collapse" && style.opacity !== "0";
  };
  /** 读取元素文本并去除首尾空白，缺失元素返回空串。
   * 参数：element：页面元素。
   */
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
  /** 检查任一选择器是否匹配到可见元素。
   * 参数：selectors：加载或空表提示的选择器列表。
   */
  const visibleMatch = selectors => selectors.some(selector =>
    Array.from(document.querySelectorAll(selector)).some(isVisible));
  /** 判断数据行是否为空表占位提示。
   * 参数：row：候选表格行元素。
   */
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

/** 将表头、行数和加载状态组合为诊断文本。
 * 参数：snapshot：当前表格快照。
 */
const diagnostic = snapshot =>
  `表头=${snapshot.headers.join(" | ")}; 行数=${snapshot.rows.length}; ` +
  `可见加载状态=${snapshot.loadingVisible ? "是" : "否"}; ` +
  `空表占位=${snapshot.emptyVisible ? "是" : "否"}`;

/** 列出当前表头缺少的必需元数据列。
 * 参数：headers：当前可见表头列表。
 */
const missingRequiredHeaders = headers =>
  REQUIRED_HEADERS.filter(alias => !headers.some(header => header === alias || header.includes(alias)));

/** 构造包含等待时限和快照诊断的未就绪错误。
 * 参数：snapshot：当前表格快照；timeoutMs：等待毫秒数。
 */
const notReadyError = (snapshot, timeoutMs) => {
  const error = new Error(`AIMES_TABLE_NOT_READY：AIMES 工厂订单表在 ${timeoutMs}ms 内未就绪；诊断：${diagnostic(snapshot)}`);
  error.code = "AIMES_TABLE_NOT_READY";
  return error;
};

/** 构造缺少必要列的结构错误并附带缺失列清单。
 * 参数：headers：当前表头；missing：缺失列名称列表。
 */
const schemaError = (headers, missing) => {
  const error = new Error(`AIMES 工厂订单表缺少必要列；当前表头：${headers.join(" | ")}`);
  error.code = "AIMES_TABLE_SCHEMA";
  error.missingColumns = missing;
  return error;
};

/** 等待并读取可见工厂单表，不把加载中的短暂空表当作结果。
 * 参数：page：浏览器页面；timeoutMs：最长等待毫秒数；requireMetadata：是否要求完整元数据列。
 */
export async function readAimesTable(page, { timeoutMs = 15000, requireMetadata = true } = {}) {
  const deadline = Date.now() + Math.max(1, Number(timeoutMs) || 15000);
  let snapshot = await tableSnapshot(page);
  /** 检查已有表头、加载结束且存在数据或明确空表标记。
   * 参数：current：当前表格快照。
   */
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
