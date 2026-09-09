---
name: coding-task-prompt-builder
description: Use this skill when the user asks to turn a coding or software-engineering request into a concise, implementation-ready prompt for another coding agent, Codex task, subagent, or issue-style execution brief. Preserve scope, contracts, constraints, acceptance criteria, open items, and stop conditions. Do not use it when the user wants the code change, explanation, debugging, review, or architecture answer performed directly instead of a reusable task prompt.
---

# Coding Task Prompt Builder

將使用者提供的任務資訊整理成可直接交給 coding agent 的 prompt。只輸出任務 prompt，不加入教學、前言或流程回顧。使用者當次明確指示優先於本 skill 的預設規則。

## When to use this skill

Use this skill when the main deliverable is a coding task prompt, such as:

- converting a feature request, bug report, refactor plan, review scope, or migration goal into a coding-agent prompt
- preparing a Codex task, subagent handoff, implementation brief, or issue-style execution prompt
- compressing scattered coding requirements into scope, contract, constraints, acceptance criteria, and stop conditions
- rewriting an overly broad coding instruction into a bounded prompt for another agent

Do not use this skill when the user asks to implement, debug, explain, review, or design software directly. In those cases, answer or perform the requested engineering work instead of producing a prompt unless the user explicitly asks for a prompt.

## 輸入
- `GOAL`：必要，目標與預期結果。
- `TASK_TYPE`：可選，例如 implementation / diagnosis / review / planning。
- `EVIDENCE`：可選，已確認現況。
- `SCOPE`：可選，可修改或調查的範圍。
- `CONTRACT`：可選，必須保留的行為或介面。
- `CONSTRAINTS`：可選，任務特有限制。
- `ACCEPTANCE`：可選，可觀察的驗收條件。
- `UNKNOWNS`：可選，尚未確認事項。
- `FILE_HINTS`：可選，已知相關檔案。

## 規則
- 只保留會影響本任務的資訊；不要重複一般 coding style、repo 既有規則或可直接從 repo 查得的套件與版本資訊。
- 不擴張 `SCOPE`，不改寫 `CONTRACT`，不把未知資訊補成事實。
- Implementation 預設採最小必要修改；diagnosis / review / planning 保持唯讀。
- 未知資訊只有在阻礙授權、契約或必要決策時才列為 blocker；其餘列為 open item。
- 不捏造 API、檔案、版本、命令、測試結果或執行結果。
- 不加入 commit / push / deploy 要求，除非使用者明確指定。
- 驗收條件必須可觀察；只能依實際證據標示通過、失敗或未執行。
- 可選欄位沒有內容時直接省略，避免為固定格式增加無效 context。
- 若 prompt 要交給 subagent，`CONTEXT` 只放完成該子任務必要的已確認事實、相關檔案或來源、契約與限制；不得附上整段對話或要求繼承完整對話歷史。

## 輸出格式
依實際需要使用以下區塊，省略空白區塊：

```text
TASK
<目標、任務類型、預期結果>

CONTEXT
<已確認事實與相關檔案>

BOUNDARIES
<scope、contract、constraints、不可變更項>

EXECUTION
<完成任務所需的最小行動與限制>

ACCEPTANCE
<可觀察的驗收條件>

OPEN ITEMS / STOP CONDITIONS
<真正阻塞事項、未確認項與停止條件>
```

不要額外輸出上述 prompt 以外的內容。
