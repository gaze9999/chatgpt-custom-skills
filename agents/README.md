# Agent 治理與同步

此目錄的 [AGENTS.md](./AGENTS.md) 是跨專案 global 指示的可版控來源 在其他電腦 clone repository 後, 仍須將它安裝至該電腦的 `$CODEX_HOME/AGENTS.md` 或預設的 `~/.codex/AGENTS.md`; repository 內的副本不會自動套用為 global 指示

## 分層

- Global `AGENTS.md` 保存穩定的語言偏好, 授權邊界, 執行原則與驗證誠實性
- 專案 root 與 nested `AGENTS.md` 保存該 repository 的架構, 規格, 工作範圍與驗證方式
- Custom Skill 保存只在特定任務需要的詳細程序 [task-routing](../skills/task-routing/SKILL.md) 負責分流與交接判斷, 不自行授予建立 task 或委派的權限
- 目前 task 保存具體目標, 當次授權, 工作區狀態, 未解問題與停止條件

SFAP 等專案的 role 設定, 未提交變更與本機 exclude 策略屬專案層, 不複製到此 global 來源檔 使用者若更改 task 名稱, 跨 task 回報仍須以實際 `threadId` 定位

## 跨電腦同步

先修改本 repository 的 `agents/AGENTS.md`, 審查 diff 與公開內容, 再以 `python scripts/install_global_agents.py --install` 單向安裝 不帶參數時只比對; 已安裝版本不同時預設拒絕覆寫, 可先人工合併, 或明確加上 `--replace` 並保留自動備份

Skills 仍從 repository 的 `skills/` 目錄獨立安裝, 依根目錄 [README](../README.md) 執行驗證與鏡像比對 Release 僅提供各 Skill 的 ZIP asset; global 指示由 repository 來源檔與安裝 script 管理
