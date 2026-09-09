---
name: codex-context-brief-builder
description: 將使用者明確提供的實作契約素材轉為可重複使用的 Codex Markdown context brief；不用於一般摘要或一次性 coding 任務。
metadata:
  short-description: 建立精簡、可追溯的 coding context brief
---

# Codex Context Brief Builder

將規格、API 文件、schema、整合指南或驗收條件，壓縮成後續實作可重複使用的 Markdown context brief。保留精確契約與來源追溯，不產出一般摘要、正式成品文件或直接實作。

## 啟用條件

僅在同時具備下列條件時使用：

- 使用者提供或明確指定可讀取的來源素材。
- 素材包含實作相關契約，例如行為、欄位、流程、權限、錯誤處理或驗收條件。
- 使用者要求可重複使用的 Codex／coding agent Markdown context brief。

單純文件轉 Markdown、一般摘要、Notion 整理、正式 PDF/DOCX、單一 coding prompt 或實作後文件更新，改用對應流程。

## 作業方式

- 先確認來源邊界、預定使用方式與輸出目標；只在缺口影響正確性或覆蓋範圍時追問。
- 保留名稱、路徑、欄位、enum、狀態碼、驗證、安全／權限、錯誤、限制、範例與驗收條件。
- 壓縮行銷文字、重複背景與不影響實作的敘事；不把缺漏、衝突或 OCR 結果寫成已確認事實。
- 多份來源保留可追溯的來源邊界；資料過大時只抽取與任務相關的區段。

## 按需工具

- PDF、DOCX、XLSX 或其他結構化檔案：先執行 `scripts/extract_source_text.py <source-file>`；掃描檔或關鍵圖片無法原生抽取時才加 `--ocr-fallback`。
- OCR、表格或萃取不足時，將覆蓋度標為 `partial` 或 `unverified`，並保留來源位置。
- 完成 brief 後執行 `scripts/validate_context_brief.py <brief.md>`；需要機器可讀結果時加 `--json`。

## 輸出契約

可寫入時建立實體 Markdown，建議檔名為 `<source-or-project-name>_Codex_Context_Brief.md`。內容至少包含：Metadata、Scope、實作摘要、Contracts and invariants、Codex 實作指引、未解項目與來源追溯；只保留適用的 API、資料模型、流程、錯誤或安全段落。

最終回覆列出輸出位置、來源覆蓋度、已執行驗證與重要未確認項目。
