---
name: document-production-pipeline
description: 從使用者需求與來源素材建立可交付的文件 artifact；未指定格式時預設輸出 PDF。
metadata:
  short-description: 預設 PDF 的文件產出 pipeline，可依需求輸出 DOCX／Markdown
---

# 文件成品產出 Pipeline

將使用者的內容、來源與限制整理為可交付文件，而非只輸出草稿或生成 prompt。未指定格式時產出 PDF；指定 DOCX、Markdown 或多種格式時以使用者要求為準。

## 核心流程

- 確認目標、受眾、已有內容、必要來源與限制，再建立資訊架構。
- 需要外部資料時，只使用可直接支持敘述的可靠來源；可能變動的資訊先查證。
- 建立真正可開啟的 artifact，保留使用者提供的事實、數字、專有名詞與引用；不捏造無法確認的資料。
- 依文件用途與格式需求，讀取 [文件產出指引](references/document-production-guidelines.md)。

## 格式與品質

- PDF：文字可選取、字型與繁中／日文正常顯示；需 render 時檢查目錄、標題、表格與留白。
- DOCX：使用原生 Heading、TOC 與頁碼欄位；必要時 render 確認目錄與頁碼。
- Markdown：維持連續 heading hierarchy，不模擬頁碼或固定紙張版面。
- 多格式輸出需維持事實、章節與引用一致，允許格式特有的版面差異。

涉及科學、醫療、健康、藥學或心理學的文件，使用 APA 第七版文內引用與參考資料；其他內容也需使用可追溯且直接支持主張的來源。

## 按需驗證

依輸出格式執行對應工具：`scripts/validate_pdf.py`、`scripts/validate_docx.py`、`scripts/validate_markdown.py`；使用 APA 時執行 `scripts/validate_apa7.py`。無法完成 render 或其他檢查時，標記未驗證與原因，不宣稱通過。

最終回覆僅列出成品連結、格式、已完成驗證與未驗證項目。
