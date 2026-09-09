---
name: coding-task-prompt-builder
description: 從最少必要欄位建立簡潔、可直接執行的 coding 任務 prompt，並保留 scope、契約與驗收邊界。
metadata:
  short-description: 精簡 coding 任務 prompt 產生器
---

# Coding 任務 Prompt Builder

將使用者提供的任務資訊整理成可直接交給 coding agent 的 prompt。只輸出 prompt 本文，不加教學、前言或流程回顧；使用者當次指示優先。

## 輸入

必要欄位：`GOAL`。

可選欄位：`TASK_TYPE`、`EVIDENCE`、`SCOPE`、`CONTRACT`、`CONSTRAINTS`、`ACCEPTANCE`、`UNKNOWNS`、`FILE_HINTS`。

## 規則

- 只保留會影響任務的資訊；不重複 repo 既有規則或可直接查得的資訊。
- 不擴張 scope、不改寫 contract，也不把未知補成事實。
- implementation 採最小必要修改；diagnosis、review、planning 預設唯讀。
- 只有未知會阻礙授權、契約或必要決策時才列為 blocker，其餘列為 open item。
- 驗收條件必須可觀察；不捏造 API、檔案、版本、命令或驗證結果。
- 未經明確要求，不加入 commit、push 或 deploy。

直接輸出可交接的任務 prompt；空白可選欄位直接省略。
