# ChatGPT Custom Skills

可重複使用的 ChatGPT / Codex Skills 集合，集中管理 Skill 行為、內部資源與可選的 agent metadata。

本 repository 的目標是讓不同任務可以直接重用已整理好的 Skill，同時維持清楚的責任邊界，避免把一次性需求或完整基礎 prompt 重複寫在多個位置。

## Skills

| Skill | 路徑 | 用途 | 主要輸出 |
|---|---|---|---|
| [Agent Governance Architect](./skills/agent-governance-architect/SKILL.md) | `skills/agent-governance-architect` | 盤點並重整 `AGENTS.md`、subagent 職責與指示分層，移除不必要的重複規則 | Agent / subagent 治理規範修改 |
| [Coding Task Prompt Builder](./skills/coding-task-prompt-builder/SKILL.md) | `skills/coding-task-prompt-builder` | 將最小必要的需求、scope、contract、驗收條件與停點整理成可直接交給 coding agent 的任務 prompt | 精簡 coding task prompt |
| [Codex Context Brief Builder](./skills/codex-context-brief-builder/SKILL.md) | `skills/codex-context-brief-builder` | 將規格書、API 文件、schema、需求文件或整合指南整理成可重複給 Codex 使用的 Markdown context brief | Codex context summary Markdown |
| [Document Production Pipeline](./skills/document-production-pipeline/SKILL.md) | `skills/document-production-pipeline` | 將使用者內容、來源與版面需求整理成可直接交付的正式文件；未指定格式時預設 PDF | PDF；或依需求輸出 DOCX / Markdown 等支援格式 |
| [Editorial Illustration Image Pipeline](./skills/editorial-illustration-image-pipeline/SKILL.md) | `skills/editorial-illustration-image-pipeline` | 將使用者提供的圖片、可選視覺調整與內建 base prompt 合併後，直接執行 editorial illustration 圖片生成 | 每張來源圖對應一張獨立插畫 |
| [Post-Implementation Doc Updater](./skills/post-implementation-doc-updater/SKILL.md) | `skills/post-implementation-doc-updater` | 程式改版、PR、diff、release 或 refactor 後，更新 docs、Markdown memo、Notion memo、changelog、API reference 或 Codex context brief | 與實作變更對齊的文件／memo 更新 |

## 設計原則

- 每個 Skill 只負責明確的一類任務。
- 共用或較長的基礎內容放在 Skill 自己的 `references/` 中，避免在多處維護相同 prompt 或規範。
- 專案層級、角色層級與單次任務的指示盡量分離，降低規則重複與 context 成本。
- README 只提供開始使用所需的資訊；各 Skill 的完整行為以各自的 `SKILL.md` 為準。

## 安裝

每個 Skill 都可以獨立安裝，不需要安裝整個 repository 內的其他 Skill。

### 手機／平板 ChatGPT App

行動端建議透過 **GitHub Releases 的單一 Skill ZIP asset** 安裝，不需要先下載整個 repository，也不需要在手機／平板手動解壓縮 repository ZIP。

1. 開啟本 repository 的 **Releases**：

   ```text
   https://github.com/gaze9999/chatgpt-custom-skills/releases
   ```

2. 選擇要使用的 release。

3. 在 **Assets** 中下載要安裝的單一 Skill ZIP，例如：

   ```text
   agent-governance-architect.zip
   coding-task-prompt-builder.zip
   codex-context-brief-builder.zip
   document-production-pipeline.zip
   editorial-illustration-image-pipeline.zip
   post-implementation-doc-updater.zip
   ```

4. 不要自行解壓縮。ZIP 內應保留該 Skill 的完整目錄內容，例如：

   ```text
   document-production-pipeline/
   ├── SKILL.md
   ├── agents/
   │   └── openai.yaml
   └── references/
       └── document-production-guidelines.md
   ```

5. 在 ChatGPT App 開啟 **Plugins → Skills → Create → Upload from your computer**。

6. 從手機／平板的檔案選擇器直接選取剛才下載的 Skill ZIP。

7. 等待 ChatGPT 完成掃描與安裝，再到 Skills 清單確認對應名稱是否出現。

### Desktop / Web

若目前使用的 ChatGPT / Codex 用戶端支援從 GitHub repository 安裝或載入 Skill，可指定：

```text
Repository: gaze9999/chatgpt-custom-skills
Skill path: skills/<skill-name>
```

例如：

```text
Repository: gaze9999/chatgpt-custom-skills
Skill path: skills/document-production-pipeline
```

各 Skill 可獨立安裝；不需要一次載入整個 `skills/` 目錄。

若使用上傳方式，也可以直接使用 Releases 中對應的單一 Skill ZIP asset。

### 本機查看內容

```bash
git clone https://github.com/gaze9999/chatgpt-custom-skills.git
cd chatgpt-custom-skills
```

## Release 封裝規則

為了讓手機／平板可以直接安裝，每個 release 應另外提供每個 Skill 的獨立 ZIP asset，而不是只依賴 GitHub 自動產生的 repository source archive。

每個 ZIP 的頂層應直接包含單一 Skill 目錄，例如：

```text
document-production-pipeline.zip
└── document-production-pipeline/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    └── references/
        └── document-production-guidelines.md
```

Release assets 建議保持與 Skill 目錄相同的 basename，方便辨識與版本管理。

## 使用方式

### Agent Governance Architect

適合處理：

```text
盤點這個 repo 的 AGENTS.md 與 subagent 規則，移除跨層重複，保留必要的專案約束。
```

此 Skill 聚焦在 agent governance，不應順便修改 production code。

### Coding Task Prompt Builder

適合處理：

```text
把這個需求整理成可以直接交給 coding agent 的 task prompt，保留 scope、contract、acceptance criteria 與 stop conditions。
```

輸出重點是任務本身，不重複一般 coding style、repo 已存在的規則或可直接查得的版本資訊。

### Codex Context Brief Builder

適合處理：

```text
把這份 API 文件整理成之後可以重複給 Codex 使用的 context brief Markdown，保留 endpoint、schema、error handling 與 open questions。
```

此 Skill 聚焦在長文件壓縮成可重用 Codex 背景，不負責直接實作，也不取代單次任務 prompt。輸出應保留實作契約、限制、例外情境與來源追蹤，避免之後每次都重新貼完整規格書。

### Document Production Pipeline

未指定輸出格式時預設產生 PDF；使用者可以明確要求 DOCX、Markdown 或多格式輸出。

例如：

```text
把這些資料整理成正式技術教學文件，包含目錄、章節化說明、範例與參考資料，預設 PDF。
```

或：

```text
同一份內容請輸出 PDF、DOCX 與 Markdown。
```

Pipeline 會依 `references/document-production-guidelines.md` 處理檔名、文件版本、目錄、分頁、表格、引用與最終 QA，並直接交付文件 artifact。

### Editorial Illustration Image Pipeline

使用時提供一張或多張來源圖片，可再用自然語言補充當次調整，例如：

```text
人物再小一點，右側增加留白，整體色調稍微偏暖。
```

Pipeline 會將：

```text
來源圖片
+ references/base-prompt.md
+ 使用者當次可選調整
→ 直接圖片生成
```

每張來源圖片獨立處理，不把多張圖片自動合併成 collage；正常流程直接輸出圖片，不另外輸出組裝後的 prompt。

### Post-Implementation Doc Updater

適合處理：

```text
這次功能改完後，根據目前 diff 更新 README、docs、memo、Notion 和 Codex context brief。
```

此 Skill 聚焦在 implementation 之後的文件同步。它會先判斷程式變更是否真的影響文件，再更新必要的 Markdown、Notion memo、changelog、API reference 或 Codex context brief；內部 refactor、test-only、format-only 變更通常不更新文件。

### 檔案角色

- `SKILL.md`：Skill 的主要行為、適用範圍、輸入／輸出與限制。
- `agents/openai.yaml`：該 Skill 的 agent / interface metadata。
- `references/`：Skill 執行時需要引用、但不適合重複塞進 `SKILL.md` 的內部內容。
- `assets/`：icon、模板或執行時可能使用但通常不需讀入 context 的素材。
- `scripts/`：可重複、可程式化的掃描、驗證或轉換流程。
