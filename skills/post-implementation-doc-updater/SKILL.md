---
name: post-implementation-doc-updater
description: 僅在使用者明確要求、具可驗證的實作變更證據且有既有文件目標時，更新或同步相關文件。
metadata:
  short-description: 依實作證據最小化更新既有文件與 memo
---

# Post-Implementation Doc Updater

依已完成的實作變更，最小化更新 README、Markdown、changelog、API 參考、Notion memo 或 Codex context brief，使文件與可驗證變更一致。不是從頭撰寫新文件的流程。

## 啟用條件

僅在同時具備下列條件時使用：

- 使用者明確要求更新、對齊或同步既有文件。
- 有 diff、commit、PR、release、migration、變更檔清單或可引用的 code-change 摘要。
- 至少有一個具體文件目標。

若缺少證據或目標，先索取會影響正確性或授權的最少資訊。一般文件撰寫、摘要、翻譯、Notion 整理、coding 任務 prompt、實作前 brief 或正式交付文件，改用對應流程。

## 作業方式

- 以 diff 與變更檔為最高可信證據；只有使用者摘要時，標為 `summary-based`。
- 只更新受公共 API、使用者可見行為、安裝設定、部署、遷移、相容性或既有架構描述影響的文件；行為無差異的內部重構通常不更新。
- 先讀取必要 diff 與目標段落，產生最小變更；不將內部細節推論為公開保證，不新增祕密或非必要個資。
- 需要影響盤點時執行 `scripts/scan_changed_files.py --repo <repo-root>`；跨多個目標時依 [文件更新規則](references/doc-update-rules.md) 建立精簡更新計畫，並以 `scripts/validate_doc_update_plan.py` 檢查。

## Notion 與 Markdown

- 未明確要求 Notion 時，不讀寫 Notion。
- 只有使用者明確指定 Notion 目標，或目標 Markdown 有明確關聯時，才依 [Notion 同步讀寫契約](references/notion-sync-reader-writer-contract.md) 讀取精準目標。
- 預設不雙向同步；只有明確授權、同時提供雙方目標，或 Markdown 標示 `sync_mode: bidirectional` 時才同步。
- 寫入前使用對應 `inspect_*` script 取得目標狀態；Markdown 全檔替換需先 dry-run 並驗證 SHA-256。Notion live 寫入後立即重新讀取確認。

## 交付

回報使用的變更證據、實際更新的目標、未更新的理由、Notion／Markdown 同步結果，以及已執行與未執行的驗證。
