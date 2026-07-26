# `i-have-adhd` skill 應用評估

<!-- 評估產物。建立：2026-07-21（skill 評估 session）。
     本檔只做評估與建議，未改動任何制度核心檔（reporting.md、hard-rules.md 等）。
     第 6 節的整合建議為待核准提案，需使用者核准後另開改動落實。 -->

**評估對象**：[`ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd)（MIT）
**評估標的**：本專案 `claude-institution` 是否／如何採用此 skill

---

## 1. 結論先行

**不建議原樣安裝**這個 marketplace plugin，理由是本專案 `institution/rules-lib/reporting.md` 已獨立蒸餾出它約
**八成**的規則，且它的 opt-in slash-command 形態與本專案「輸出風格應常載、規則要放對層」的哲學相衝。

**建議**：只把它真正比本專案多出來的 **3 條規則**（每回合重述進度、結尾給一個 <2 分鐘可做的下一步、
具體時間估計）蒸餾成 1–2 行，補進既有 `reporting.md`／`hard-rules.md`。草稿見第 6 節，需使用者核准後另開改動落實。

---

## 2. i-have-adhd 是什麼

一個給 coding agent（Claude Code／Codex／Cursor）的**輸出風格 skill**，目的是「stop it from burying the answer」——
讓回應對 ADHD 讀者更好讀、更可執行。以 marketplace plugin 安裝，用 slash command `/i-have-adhd` 觸發。

它立基於五個「神經現實」：工作記憶有限（資訊捲出螢幕就消失）、理解 ≠ 執行、起步要靠最小的第一動作、
時間估計需要具體、進度可見驅動多巴胺。由此展開 **10 條規則**：

| # | 規則 | 白話 |
|---|---|---|
| 1 | Lead with action | 先講行動，不是脈絡或計畫 |
| 2 | Number multi-step tasks | 多步驟編號，一項一個有界動作 |
| 3 | End with one concrete next action | 結尾一個 <2 分鐘可做的下一步 |
| 4 | Suppress tangents | 先解決第一個問題，別岔題 |
| 5 | Restate state each turn | 每回合重述進度（讀者記不住上一則） |
| 6 | Specific time estimates | 「15 分鐘」勝過「一些工作」 |
| 7 | Make wins visible | 具體講「現在什麼能動了」 |
| 8 | Matter-of-fact errors | 就事論事報錯，直接講因與修法 |
| 9 | Cap lists at 5 | 清單上限 5 項，多了就排序或拆「現在／稍後」 |
| 10 | Skip preamble/pleasantries | 省略開場、recap、收尾提問 |

破例時機：需要解釋、破壞性動作（要安全確認）、除錯鬼打牆、真有歧義時可覆寫。

---

## 3. 逐條映射：10 條規則 × 本專案既有對應

| # | i-have-adhd 規則 | 本專案既有對應 | 判定 |
|---|---|---|---|
| 1 | Lead with action | `hard-rules #14`「結論先行」＋`reporting.md §1`（好/壞例俱全） | **重疊** |
| 2 | Number multi-step tasks | `reporting.md §4`（可列舉才開結構）＋ hard-rules 計畫節「可勾選項目」 | **重疊** |
| 3 | One concrete next action (<2min) | 無直接對應。`reporting.md §3` 給的是「決策選項表」，不是「一個最小下一步」 | **新增** |
| 4 | Suppress tangents | `reporting.md §2`「選擇性省略」（彎路、讀過哪些檔、試錯次數一律省略） | **重疊** |
| 5 | Restate state each turn | 無直接對應。起手式（`CLAUDE.md`）重述的是「任務範圍+判準」，非每回合進度 | **新增** |
| 6 | Specific time estimates | 無對應。本專案不要求時間估計 | **新增** |
| 7 | Make wins visible | `done-check`：每個 ✅ 必附實際指令與輸出；`reporting.md §1` 好例「測試全綠（輸出見下）」 | **重疊** |
| 8 | Matter-of-fact errors | 誠實條款（`judgment.md`）＋`hard-rules #8`（不確定就寫「我不確定」）＋`done-check` 鐵則 | **重疊** |
| 9 | Cap lists at 5 | `reporting.md §3`「選項 ≤3」、`§4`「例行回報 ≤10 行」；起手式「開場提問 ≤5 題」 | **部分**（本專案更嚴，但無通用清單上限） |
| 10 | Skip preamble/pleasantries | `reporting.md §1`（過程放結論後）＋`§2`（省略無關過程） | **重疊** |

**小計**：重疊 6 條、部分 1 條、新增 3 條。本專案在 `reporting.md`（2026-07-14 建立）已把 ADHD 溝通原則的主體
獨立蒸餾完成，且做得更細（好例/壞例、決策選項表、與誠實條款的分工邊界）。

---

## 4. 分層適配分析

本專案的核心原則是**「規則的強制力來自放對層，不是寫更多」**（`CLAUDE.md` 分層表，能上不下）。用這把尺量 i-have-adhd：

- **輸出風格屬「每次都要守」的常載範疇** → 對應層 1（`hard-rules #14`）＋層 2 常載按需檔（`reporting.md`，
  路由表註明「準備向使用者回報時」讀）。本專案已經把它放在正確的層。
- **i-have-adhd 卻是層 2 的 opt-in slash command**（`/i-have-adhd`）：只有被呼叫那一回合才生效。
  輸出風格若要 opt-in，等於預設不生效——與「常載」矛盾。

**原樣 marketplace 安裝的三個落差**：
1. **生效時機錯**：slash command 不呼叫就不套用；風格規則需常載。
2. **語言**：規則是英文；本專案全繁中，且要求「用使用者的語言」（`reporting.md §4`）。
3. **版本控管邊界**：marketplace plugin 由 Claude Code 自行抓取維護，活在 `institution/` 快照與 `restore.sh`
   之外，違反本專案「制度檔要能版本控管、可 restore」的設計。

---

## 5. 衝突檢查（採用前必過）

新增規則不得凌駕本專案既有的更高優先條文（衝突優先序：誠實條款 > hard-rules > 按需檔/skills，見 `CLAUDE.md`）：

- **規則 9「清單上限 5」vs `done-check` 固定模板**：done-check 報告的邊界情況等欄位是**逐字產物**，
  不受「上限 5」約束。採用時須註明「上限適用於敘述性清單，不適用固定模板」。
- **規則 4/10「省略」vs 誠實條款必填欄位**：本專案已明訂省略的是**無關過程**，不是壞消息；
  且 `hard-rules #3`「已驗證: 」、`#4`「範圍外發現: 」、`judgment`「AUTH: 」是**永遠保留**的必填欄位
  （`reporting.md:27-28`）。i-have-adhd 的「suppress/skip」若無此界線會誤傷誠實條款——本專案已有防線，**採用時不得放寬**。
- **規則 3「一個下一步」vs `reporting.md §3` 決策選項表**：兩者不衝突而是互補——選項表用於「要使用者做決定」，
  「一個 <2 分鐘下一步」用於「使用者可自己往前走」的情境。採用時要講清楚各自適用場合。

**結論**：3 條新增規則與既有制度**無不可解衝突**，但落地時必須明寫上述三條邊界，否則會鬆動誠實條款。

---

## 6. 採用建議（待核准提案）

把 3 條真正新增的規則蒸餾入既有檔，維持繁中與檔尾 Changelog 慣例。**以下為草稿，需使用者核准後另開改動落實，本次不改核心檔。**

**建議落點：`reporting.md` 新增一節**（因三條都是「回報寫法」，與 reporting.md 主題一致，屬層 2 常載按需檔）：

> ### 5. ADHD 友善補充（借鏡 ayghri/i-have-adhd）
> - **可見進度**：多回合任務每回合開頭一行複述「已完成 X／進行中 Y／待辦 Z」，讀者不必回捲。
>   （與起手式的「任務範圍+判準」複述不同：那是開場一次，這是每回合的進度快照。）
> - **一個下一步**：不需使用者做決定時，結尾給**一個** <2 分鐘可做的具體下一步（動詞開頭），
>   而非開放式「你覺得呢？」。需使用者做決定時仍用 §3 選項表。
> - **具體估計**：講工作量用具體單位（「約 15 分鐘／改 3 檔」），不用「一些／很快」。
> - 邊界：本節的「省略／精簡」不得凌駕誠實條款必填欄位（見 §2 末段）；固定模板（如 /done-check）不受上限約束。

**替代落點**（若嫌 reporting.md 變長）：僅取「可見進度」一條升到 `hard-rules`，其餘留 reporting.md。
建議前者——三條同源、同主題，集中一節較好維護。

**不建議**：`claude plugin marketplace add ayghri/i-have-adhd`（原樣安裝，落差見第 4 節）。

---

## 7. 附：若仍想「原樣試用」

若使用者想先體感原 skill 再決定，最小侵入做法是把 SKILL.md 中文化後放進 `institution/skills/i-have-adhd/`
（比照現有 skill 慣例補 YAML frontmatter + 中文 description），當一個可 `/i-have-adhd` 呼叫的層 2 skill 試跑，
**不動既有檔**。但這仍是 opt-in，只適合「試用對照」，不適合當長期方案——長期仍回到第 6 節的蒸餾整合。

---

## Changelog

- 2026-07-21：初版評估（skill 評估 session）。結論：不原樣安裝，建議蒸餾 3 條新增規則入 reporting.md；
  未改動任何制度核心檔，整合待使用者核准。
- 2026-07-21：第 6 節整合提案經使用者核准，已落實進 reporting.md §5。
