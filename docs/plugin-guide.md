# Claude Code Plugin 使用指南

> 依據 2026-10-23 `claude plugin list` 與 `~/.claude/plugins/` 實際檔案整理。
> 內容來自各 plugin 的 agent／command／SKILL.md frontmatter，plugin 升版後可能不準。

## 目錄

- [總覽](#總覽)
- [三種元件怎麼用](#三種元件怎麼用)
- [ws plugin（claude-code-workflows）](#ws-pluginclaude-code-workflows)
  - [backend-development](#backend-development)
  - [data-engineering](#data-engineering)
  - [frontend-mobile-development](#frontend-mobile-development)
  - [game-development](#game-development)
  - [javascript-typescript](#javascript-typescript)
  - [kubernetes-operations](#kubernetes-operations)
  - [llm-application-dev](#llm-application-dev)
  - [llm-finetuning](#llm-finetuning)
  - [machine-learning-ops](#machine-learning-ops)
  - [multi-platform-apps](#multi-platform-apps)
  - [observability-monitoring](#observability-monitoring)
  - [python-development](#python-development)
  - [ui-design](#ui-design)
- [claude.ai 同步 plugin](#claudeai-同步-plugin)
  - [data](#data)
  - [cowork-plugin-management](#cowork-plugin-management)
- [情境速查](#情境速查)
- [注意事項](#注意事項)

---

## 總覽

| Plugin | 版本 | Agents | Commands | Skills | 一句話 |
|---|---|---|---|---|---|
| backend-development | 1.3.2 | 8 | 1 | 9 | 後端架構、API、事件溯源、Temporal、TDD |
| data-engineering | 1.3.2 | 2 | 2 | 4 | 資料管線、Airflow、dbt、Spark、資料品質 |
| frontend-mobile-development | 1.2.3 | 2 | 1 | 4 | React／Next.js／React Native 前端 |
| game-development | 1.2.3 | 2 | 0 | 2 | Unity、Minecraft plugin、Godot |
| javascript-typescript | 1.2.3 | 2 | 1 | 4 | JS／TS 語言、Node.js 後端、測試 |
| kubernetes-operations | 1.2.3 | 1 | 0 | 4 | K8s 架構、manifest、Helm、GitOps、安全政策 |
| llm-application-dev | 2.0.6 | 3 | 3 | 8 | RAG、向量檢索、LangGraph agent、prompt |
| llm-finetuning | 1.0.0 | 3 | 2 | 10 | 以 eval 把關的 LLM 微調全流程 |
| machine-learning-ops | 1.2.2 | 3 | 1 | 2 | ML 建模、MLOps 管線、推薦系統 |
| multi-platform-apps | 1.3.1 | 6 | 1 | 0 | Web＋iOS＋Android＋桌面跨平台 |
| observability-monitoring | 1.2.3 | 4 | 2 | 4 | 監控、log、tracing、SLO、Grafana |
| python-development | 1.2.3 | 3 | 1 | 16 | Python 語言、FastAPI、Django、uv |
| ui-design | 1.0.5 | 3 | 4 | 9 | UI 設計、設計系統、無障礙 |
| data（同步） | 1.1.0 | 0 | — | 10 | 資料分析師：SQL、探索、視覺化、dashboard |
| cowork-plugin-management（同步） | 0.2.2 | 0 | — | 2 | 在 Cowork 桌面版建立／客製 plugin |

合計：42 個 agent、19 個 command、76 個 skill（ws），加上同步 plugin 的 12 個 skill。

kubernetes-operations 和 observability-monitoring 是 2026-10-23 為了 `/machine-learning-ops:ml-pipeline` 的 Phase 3–4 補裝的（見 [machine-learning-ops](#machine-learning-ops)），常駐成本分別約 588 與 966 tokens（`claude plugin details` 估算）。

---

## 三種元件怎麼用

| 元件 | 本質 | 怎麼觸發 | 適合 |
|---|---|---|---|
| **Command** | 一份寫好的多步驟流程 | 手動輸入 `/<plugin>:<command> <參數>` | 有固定流程的大任務（從需求到部署） |
| **Skill** | 一包知識／範例／checklist | ① Claude 依 description 自動載入；② 手動輸入 `/<plugin>:<skill>` | 寫碼時需要某領域的最佳實踐 |
| **Agent** | 帶專屬 system prompt 的 subagent，在獨立 context 執行 | 對話中指名（例：「用 `python-pro` agent 審這個模組」），或 command 內部自動派發 | 需要專家角度、或不想讓中間輸出塞滿主對話 |

補充：

- 輸入 `/` 後打 plugin 名稱或關鍵字，自動完成清單就會列出可用的 command 和 skill。
- **Orchestrator command 會在專案根目錄建立狀態資料夾**（例：`.feature-dev/state.json`），每個階段寫一份產出檔，並在 `PHASE CHECKPOINT` 停下來等你核准。中斷後再執行同一個 command，會問你要接續還是重新開始。
- Agent 的 `model` 欄位：`inherit` 代表沿用主對話的模型；`opus`／`sonnet` 代表固定使用該模型，不管主對話用哪個。

---

## ws plugin（claude-code-workflows）

### backend-development

**用途**：後端服務設計與實作，涵蓋 API 設計、微服務、事件溯源／CQRS、Temporal 工作流程、TDD、安全與效能審查。

**Command**

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/backend-development:feature-development` | `<功能描述> [--methodology tdd\|bdd\|ddd] [--complexity simple\|medium\|complex]` | 從需求到部署的端到端功能開發，共 3 階段 7 步驟 |

`feature-development` 的流程（產出寫在 `.feature-dev/`）：

1. **Discovery**：需求收集 → 架構與安全設計 → ⏸ Checkpoint 1
2. **Implementation**：後端實作 → 前端實作 → 測試、安全與效能驗證 → ⏸ Checkpoint 2
3. **Delivery**：部署與監控 → 文件與交接

**Agents**

| Agent | Model | 專長 |
|---|---|---|
| `backend-development-backend-architect` | inherit | 可擴充的 API 設計、微服務邊界、服務間通訊、韌性模式 |
| `backend-development-graphql-architect` | opus | GraphQL federation、效能、快取、即時系統 |
| `backend-development-performance-engineer` | sonnet | 回應時間、記憶體、查詢效率的 profiling 與優化 |
| `backend-development-security-auditor` | sonnet | OWASP Top 10、認證缺陷、合規審查 |
| `backend-development-tdd-orchestrator` | opus | 紅綠重構紀律、TDD 流程治理 |
| `backend-development-test-automator` | sonnet | 建立 unit／integration／E2E 測試 |
| `event-sourcing-architect` | inherit | Event store、projection、saga、最終一致性 |
| `temporal-python-pro` | inherit | Temporal Python SDK、durable workflow、saga |

**Skills**

| Skill | 用途 |
|---|---|
| `api-design-principles` | REST／GraphQL API 設計原則與規範 |
| `architecture-patterns` | Clean／Hexagonal Architecture、DDD |
| `microservices-patterns` | 服務邊界、事件驅動通訊、韌性模式 |
| `cqrs-implementation` | 讀寫模型分離 |
| `event-store-design` | Event store 的設計與技術選型 |
| `projection-patterns` | 從事件流建立 read model／materialized view |
| `saga-orchestration` | 跨服務分散式交易與補償動作 |
| `workflow-orchestration-patterns` | 用 Temporal 設計 durable workflow |
| `temporal-python-testing` | Temporal workflow 的 pytest 測試（time-skipping、mock、replay） |

**使用範例**

```
/backend-development:feature-development 會員點數兌換 API --methodology tdd --complexity medium
用 security-auditor agent 審查 src/auth/ 下的登入流程
```

---

### data-engineering

**用途**：批次與串流資料管線、資料倉儲、Airflow 排程、dbt 轉換、Spark 調校、資料品質，以及資料驅動的功能開發（A/B 測試）。

**Commands**

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/data-engineering:data-pipeline` | `<需求描述>` | 設計並實作資料管線：ingestion、orchestration、dbt 轉換、品質檢查、監控 |
| `/data-engineering:data-driven-feature` | `<功能描述> [--experiment-type ab\|multivariate\|bandit] [--confidence 0.90\|0.95\|0.99]` | 由資料洞察驅動的功能開發，5 階段 16 步驟、4 個 checkpoint |

`data-driven-feature` 的流程（產出寫在 `.data-driven-feature/`）：

1. **資料分析與假設**：EDA → 商業假設 → 實驗設計 → ⏸
2. **架構與埋點**：功能架構 → analytics 埋點設計 → 資料管線架構 → ⏸
3. **實作**：後端 → 前端 → ML 模型整合（有需要才做）→ ⏸
4. **驗證與上線**：analytics 驗證 → 實驗部署 → 漸進式放量 → 安全審查 → ⏸
5. **分析與決策**：統計分析 → 商業影響評估 → 優化路線圖

**Agents**

| Agent | Model | 專長 |
|---|---|---|
| `data-engineer` | opus | Spark、dbt、Airflow、雲端資料平台、即時串流 |
| `data-engineering-backend-architect` | inherit | 與 backend-development 的 backend-architect 內容相同（見[重複的 agent](#注意事項)） |

**Skills**

| Skill | 用途 |
|---|---|
| `airflow-dag-patterns` | Airflow DAG 的 operator、sensor、測試與部署 |
| `dbt-transformation-patterns` | dbt 模型組織、測試、文件、incremental 策略 |
| `spark-optimization` | 分區、快取、shuffle、記憶體調校 |
| `data-quality-frameworks` | Great Expectations、dbt tests、data contract |

**使用範例**

```
/data-engineering:data-pipeline 每小時從 Postgres CDC 同步訂單到 BigQuery，用 dbt 建彙總表
/data-engineering:data-driven-feature 首頁推薦區塊改版 --experiment-type ab --confidence 0.95
```

---

### frontend-mobile-development

**用途**：React 19／Next.js 前端與 React Native 行動 app 的實作。

**Command**

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/frontend-mobile-development:component-scaffold` | `<元件描述>` | 產生 React／React Native 元件，附 TypeScript、測試、樣式、Storybook story |

**Agents**

| Agent | Model | 專長 |
|---|---|---|
| `frontend-mobile-development-frontend-developer` | inherit | React 元件、響應式版面、client 狀態管理 |
| `frontend-mobile-development-mobile-developer` | inherit | React Native／Flutter／原生整合、離線同步 |

**Skills**

| Skill | 用途 |
|---|---|
| `nextjs-app-router-patterns` | App Router、Server Components、streaming、平行路由 |
| `react-native-architecture` | Expo、導覽、native module、離線同步 |
| `react-state-management` | Redux Toolkit／Zustand／Jotai／React Query 的選擇與設定 |
| `tailwind-design-system` | Tailwind v4 設計 token 與元件庫 |

---

### game-development

**用途**：遊戲開發，包含 Unity、Minecraft 伺服器 plugin 與 Godot。沒有 command。

**Agents**

| Agent | Model | 專長 |
|---|---|---|
| `unity-developer` | opus | Unity 6 LTS、C#、URP／HDRP、跨平台建置 |
| `minecraft-bukkit-pro` | opus | Bukkit／Spigot／Paper plugin、事件、指令系統 |

**Skills**

| Skill | 用途 |
|---|---|
| `unity-ecs-patterns` | Unity DOTS：ECS、Jobs、Burst |
| `godot-gdscript-patterns` | Godot 4 的 signal、scene、狀態機 |

---

### javascript-typescript

**用途**：JS／TS 語言層面的專業知識，包含型別系統、非同步、Node.js 後端與測試。

**Command**

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/javascript-typescript:typescript-scaffold` | `<專案描述>` | 建立 TS 專案骨架（Next.js、React＋Vite、Node.js API 或 library），使用 pnpm 並含測試與開發工具 |

**Agents**

| Agent | Model | 專長 |
|---|---|---|
| `javascript-pro` | inherit | ES6+、async、event loop、瀏覽器／Node 相容性 |
| `typescript-pro` | opus | 進階型別、泛型、嚴格型別安全 |

**Skills**

| Skill | 用途 |
|---|---|
| `modern-javascript-patterns` | ES6+ 語法、函數式寫法、重構舊程式碼 |
| `typescript-advanced-types` | 條件型別、mapped type、template literal type |
| `nodejs-backend-patterns` | Express／Fastify、middleware、錯誤處理、認證 |
| `javascript-testing-patterns` | Jest／Vitest／Testing Library |

---

### kubernetes-operations

**用途**：Kubernetes 架構與營運，包含 manifest 產生、Helm chart、GitOps 與安全政策。沒有 command。
`/machine-learning-ops:ml-pipeline` 的 Phase 3 會用到這裡的 agent。

**Agent**

| Agent | Model | 專長 |
|---|---|---|
| `kubernetes-operations-kubernetes-architect` | opus | EKS／AKS／GKE／OKE、GitOps（ArgoCD／Flux）、service mesh、progressive delivery、多租戶 |

**Skills**

| Skill | 用途 |
|---|---|
| `k8s-manifest-generator` | 產生 Deployment、Service、ConfigMap、Secret 等正式環境用 manifest |
| `helm-chart-scaffolding` | 設計與組織 Helm chart |
| `gitops-workflow` | 用 ArgoCD／Flux 做宣告式部署與持續 reconcile |
| `k8s-security-policies` | NetworkPolicy、Pod 安全標準、RBAC |

**使用範例**

```
用 kubernetes-architect agent 設計推論服務在 GKE 上的部署架構，含 GPU node pool 與 HPA
```

---

### llm-application-dev

**用途**：開發 LLM 應用，涵蓋 RAG、向量資料庫、embedding、混合檢索、LangChain／LangGraph agent、prompt 工程與 LLM 評估。

**Commands**

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/llm-application-dev:ai-assistant` | `<助理類型> [options]` | 建立 AI 助理應用（NLU、對話管理、外部整合） |
| `/llm-application-dev:langchain-agent` | `<agent 類型> [options]` | 用現代寫法建立 LangGraph agent |
| `/llm-application-dev:prompt-optimize` | `<prompt 文字或檔案>` | 用 CoT、few-shot、constitutional AI 等手法優化 prompt |

**Agents**

| Agent | Model | 專長 |
|---|---|---|
| `ai-engineer` | inherit | 正式環境的 LLM 應用、RAG、agent 編排 |
| `prompt-engineer` | inherit | prompt 設計與優化、system prompt |
| `vector-database-engineer` | inherit | Pinecone／Weaviate／Qdrant／Milvus／pgvector |

**Skills**

| Skill | 用途 |
|---|---|
| `rag-implementation` | RAG 系統整體架構 |
| `embedding-strategies` | embedding 模型選擇、chunking 策略 |
| `similarity-search-patterns` | 最近鄰查詢與檢索效能 |
| `hybrid-search-implementation` | 向量檢索加關鍵字檢索的混合方案 |
| `vector-index-tuning` | HNSW 參數、量化、延遲與 recall 的取捨 |
| `langchain-architecture` | LangChain 1.x／LangGraph 架構、記憶、工具整合 |
| `prompt-engineering-patterns` | 結構化 prompt、few-shot、CoT、prompt 除錯 |
| `llm-evaluation` | 自動指標、人工回饋、benchmark |

**使用範例**

```
/llm-application-dev:prompt-optimize prompts/classifier.txt
用 vector-database-engineer agent 評估我們的 pgvector 索引要不要換成 HNSW
```

---

### llm-finetuning

**用途**：用 eval 把關的 LLM 微調全流程。核心原則是**先有 eval harness 跟 baseline，才開始訓練**；每個階段都要產出指定檔案才能進下一階段。以 Unsloth 為主要工具。

**Commands**

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/llm-finetuning:finetune` | `[目標，例：'tune an 8B model to write our support replies']` | 從頭跑完 Phase 0–7 |
| `/llm-finetuning:promote-checkpoint` | `[run 目錄，例：runs/2026-07-13-support-bot]` | 用目前的 eval harness 重新審查既有 checkpoint，判定 PROMOTE 後才匯出 |

`finetune` 的階段與 gate 檔案：

| Phase | 內容 | 進下一階段前必須有 |
|---|---|---|
| 0 | Eval harness 與 baseline | `eval/baseline-<model>.json` |
| 1 | 評估是否真的需要微調（可改走 RAG／prompt）、選方法與模型 | `runs/<date>-<slug>/training-brief.md` |
| 2 | 資料集準備 | dataset card ＋ 驗證報告 |
| 3 | 環境檢查（見下方說明） | `env-report.json`，verdict 為 `ready`（`ready-with-warnings` 須你明確確認；`blocked` 直接停止） |
| 4 | 訓練 | 一個已完成的 checkpoint |
| 5 | Checkpoint gate | `promotion-report.md`；判定 `REJECT` 就停止，不會自動重訓 |
| 6 | 匯出 | 匯出產物與通過的 smoke test |
| 7 | Roadbook | 把本次的教訓與繞路做法附加寫入 `runs/<date>-<slug>/roadbook.md`（同一個 slug 重跑時只附加，不覆寫） |

**Phase 3 的環境檢查**預設交給 `dgx-spark-ops-engineer`（屬於 `dgx-spark-ops` plugin，目前**沒有安裝**）。沒裝時會改由 `llm-finetuning-training-engineer` 做一般的 NVIDIA 檢查（driver、VRAM、磁碟），`env-report.json` 會標 `platform: generic-nvidia`。

`eval/` 只建立一次，之後每次 run 都用同一套 goldens 比對，所以「通過」的標準在各次 run 之間一致。

**Agents**（刻意分工：負責 eval 的 agent 不參與訓練）

| Agent | Model | 專長 |
|---|---|---|
| `llm-finetuning-architect` | opus | 負責 eval gate 與方法／模型選擇；沒有 baseline 就不規劃訓練 |
| `llm-finetuning-eval-engineer` | sonnet | 建 golden set、grader、校準 judge、判定 checkpoint 能否晉升 |
| `llm-finetuning-training-engineer` | sonnet | 準備資料、產生訓練腳本、執行與監控訓練、匯出 |

**Skills**

| Skill | 用途 |
|---|---|
| `finetuning-method-selection` | 先判斷要不要微調，再選 SFT／DPO／GRPO／continued pretraining |
| `eval-harness-first` | golden set、per-failure-mode grader、judge 校準、baseline |
| `dataset-curation` | 資料格式化、chat template、packing、合成資料、dataset card |
| `trace-to-training-data` | 把 eval trace／正式環境 log 轉成 SFT 樣本與偏好資料對 |
| `lora-qlora-recipes` | LoRA／QLoRA 超參數：rank、alpha、target modules |
| `preference-optimization` | DPO／ORPO／KTO／SimPO |
| `grpo-rlvr-training` | GRPO 與可驗證獎勵的 RL（數學、程式、tool call） |
| `vision-sft` | VLM 微調（凍結 vision tower 加 LoRA） |
| `checkpoint-promotion` | drift budget、成對比較、遺忘檢查 |
| `quantized-export` | merged safetensors／LoRA-only／GGUF（imatrix）／FP8 |

**使用範例**

```
/llm-finetuning:finetune 把 Qwen 8B 調成會用我們內部 SQL 方言寫查詢
/llm-finetuning:promote-checkpoint runs/2026-10-20-sql-writer
```

---

### machine-learning-ops

**用途**：傳統 ML 建模、正式環境 ML 系統、MLOps 管線，以及推薦／排序系統架構。

**Command**

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/machine-learning-ops:ml-pipeline` | `<需求描述>` | 多 agent 協作建立 ML 管線，分 4 階段 |

`ml-pipeline` 的階段：① 資料與需求分析 → ② 模型開發與訓練 → ③ 部署與 serving → ④ 監控與持續改進。

**它會派 7 個 agent，其中 4 個來自其他 plugin**：

| 階段 | Agent | 來源 plugin |
|---|---|---|
| Phase 1 | `data-engineer` | data-engineering |
| Phase 1 | `data-scientist` | machine-learning-ops（自己的） |
| Phase 2 | `ml-engineer` | machine-learning-ops（自己的） |
| Phase 2 | `python-pro` | python-development |
| Phase 3 | `mlops-engineer` | machine-learning-ops（自己的） |
| Phase 3 | `kubernetes-operations-kubernetes-architect` | kubernetes-operations |
| Phase 4 | `observability-monitoring-observability-engineer` | observability-monitoring |

> ⚠️ 少裝任何一個來源 plugin，對應的步驟就沒有 agent 可派，原文也沒寫退回辦法。kubernetes-operations 和 observability-monitoring 就是為此補裝的。
> 另外，`ml-pipeline` 沒有 checkpoint 也沒有狀態檔，4 個階段會一路跑完，不會停下來等你核准，中斷後也無法接續。

可在描述中指定的設定：

| 設定 | 選項 |
|---|---|
| experiment_tracking | mlflow／wandb／neptune／clearml |
| feature_store | feast／tecton／databricks／custom |
| serving_platform | kserve／seldon／torchserve／triton |
| orchestration | kubeflow／airflow／prefect／dagster |
| cloud_provider | aws／azure／gcp／oci／multi-cloud |
| deployment_mode | realtime／batch／streaming／hybrid |
| monitoring_stack | prometheus／datadog／newrelic／custom |

**Agents**

| Agent | Model | 專長 |
|---|---|---|
| `data-scientist` | inherit | 進階分析、統計建模、預測模型 |
| `ml-engineer` | inherit | PyTorch 2.x／TensorFlow、model serving、特徵工程 |
| `mlops-engineer` | inherit | MLflow／Kubeflow、實驗追蹤、model registry |

**Skills**

| Skill | 用途 |
|---|---|
| `ml-pipeline-workflow` | 從資料準備到部署的 MLOps 管線（見下方說明） |
| `recsys-pipeline-architect` | 六階段推薦框架：Source → Hydrator → Filter → Scorer → Selector → SideEffect；也適用於搜尋排序、RAG reranker |

**`ml-pipeline-workflow` 的定位**：ws 裡唯一把整條流程（資料 → 訓練 → 驗證 → 部署 → 監控）寫在同一個 skill 裡的；其他 plugin 都把完整流程放在 command。但它只是知識文件，不會派 agent，也沒有關卡，真正動手的是 `/machine-learning-ops:ml-pipeline`。

> ⚠️ 它內文提到的 `references/`（4 份）、`assets/`（3 份），以及 Related Skills 列的 `hyperparameter-tuning`、`experiment-tracking-setup`、`model-deployment-patterns` 都不存在，能用的只有 `SKILL.md` 本身。

**使用範例**

```
/machine-learning-ops:ml-pipeline 流失預測模型，experiment_tracking=mlflow, orchestration=airflow, deployment_mode=batch
```

---

### multi-platform-apps

**用途**：同一個功能要在 Web、iOS、Android、桌面同時開發時使用，採 API-first 架構。沒有 skill。

**Command**

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/multi-platform-apps:multi-platform` | `<功能描述> [--platforms web,ios,android,desktop] [--shared-code evaluate\|kotlin-multiplatform\|typescript]` | 跨平台功能開發，3 階段 |

流程（產出寫在 `.multi-platform/`）：

1. **架構與 API 設計**：需求與 API contract → 設計系統與 UX 一致性 → 共用商業邏輯 → ⏸
2. **各平台平行實作**：Web（React／Next.js）、iOS（SwiftUI）、Android（Kotlin／Compose）、桌面（Electron／Tauri，選用）→ ⏸
3. **整合與驗證**：API 文件與測試 → 跨平台功能一致性測試 → 各平台優化

**Agents**

| Agent | Model | 專長 |
|---|---|---|
| `flutter-expert` | inherit | Flutter／Dart 3 多平台 |
| `ios-developer` | inherit | Swift／SwiftUI、iOS 18 |
| `ui-ux-designer` | sonnet | wireframe、設計系統、使用者流程 |
| `multi-platform-apps-backend-architect` | inherit | 同 backend-development 版本 |
| `multi-platform-apps-frontend-developer` | inherit | 同 frontend-mobile-development 版本 |
| `multi-platform-apps-mobile-developer` | inherit | 同 frontend-mobile-development 版本 |

---

### observability-monitoring

**用途**：可觀測性，包含 metrics、log、分散式 tracing、SLO 與 Grafana dashboard，另外附效能、資料庫、網路三個專家 agent。
`/machine-learning-ops:ml-pipeline` 的 Phase 4 會用到這裡的 `observability-engineer`。

**Commands**（都在主對話直接執行，不派 agent）

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/observability-monitoring:monitor-setup` | `<需求描述>` | 建立監控：Prometheus metrics、Grafana dashboard、分散式 tracing、log 彙整、告警 |
| `/observability-monitoring:slo-implement` | `<需求描述>` | 實作 SLO：選 SLI、error budget、burn-rate 告警、dashboard、報告 |

這兩個 command 的原始檔沒有參數格式，只是把你輸入的文字整段當需求。`slo-implement` 很長，觸發一次約 12.8k tokens。

**Agents**

| Agent | Model | 專長 |
|---|---|---|
| `observability-monitoring-observability-engineer` | inherit | 監控、log、tracing 系統、SLI／SLO、事故應變流程 |
| `observability-monitoring-performance-engineer` | inherit | OpenTelemetry、load testing、多層快取、Core Web Vitals |
| `observability-monitoring-database-optimizer` | inherit | 索引、N+1、查詢優化、分區、雲端資料庫調校 |
| `observability-monitoring-network-engineer` | sonnet | 多雲網路、service mesh、zero-trust、TLS、負載平衡 |

**Skills**

| Skill | 用途 |
|---|---|
| `prometheus-configuration` | Prometheus 收集、儲存與告警設定 |
| `grafana-dashboards` | 正式環境用的 Grafana dashboard |
| `distributed-tracing` | 用 Jaeger／Tempo 追蹤跨服務請求 |
| `slo-implementation` | SLI／SLO 定義、error budget、告警 |

**使用範例**

```
/observability-monitoring:monitor-setup 推論 API 的延遲、錯誤率、GPU 使用率監控，用 Prometheus + Grafana
用 database-optimizer agent 看這支特徵查詢為什麼慢
```

---

### python-development

**用途**：Python 語言與生態系，含 FastAPI、Django、uv、型別、測試、非同步、可觀測性等。skill 數量最多（16 個）。

**Command**

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/python-development:python-scaffold` | `<專案描述>` | 建立 Python 專案骨架（FastAPI／Django／library／CLI），使用 uv 並含型別、測試與開發工具 |

**Agents**

| Agent | Model | 專長 |
|---|---|---|
| `python-pro` | opus | Python 3.12+、效能、uv／ruff／pydantic |
| `python-development-fastapi-pro` | opus | FastAPI、SQLAlchemy 2.0、Pydantic v2、async |
| `python-development-django-pro` | opus | Django 5.x、DRF、Celery、Channels |

**Skills**

| 類別 | Skill | 用途 |
|---|---|---|
| 專案與工具 | `python-project-structure` | 模組組織、`__all__`、公開 API |
| | `python-packaging` | pyproject.toml、發布到 PyPI |
| | `uv-package-manager` | uv 依賴與虛擬環境管理 |
| | `python-configuration` | 環境變數、pydantic-settings、secrets |
| 程式品質 | `python-code-style` | 命名、lint、格式、docstring |
| | `python-type-safety` | type hint、泛型、Protocol、mypy／pyright |
| | `python-design-patterns` | KISS、單一職責、組合優於繼承 |
| | `python-anti-patterns` | review 用的反模式 checklist |
| 執行期行為 | `python-error-handling` | 輸入驗證、例外階層、部分失敗處理 |
| | `python-resilience` | retry、exponential backoff、timeout |
| | `python-resource-management` | context manager、清理、串流 |
| | `async-python-patterns` | asyncio 與並行 |
| | `python-background-jobs` | 任務佇列、worker、事件驅動 |
| 品質與維運 | `python-testing-patterns` | pytest、fixture、mock、TDD |
| | `python-performance-optimization` | cProfile、記憶體 profiling |
| | `python-observability` | 結構化 log、metrics、tracing |

**使用範例**

```
/python-development:python-scaffold FastAPI 服務，提供模型推論 API
用 python-pro agent 檢查 etl/ 底下有沒有效能瓶頸
```

---

### ui-design

**用途**：UI 設計、設計系統、無障礙（WCAG）與互動設計。4 個 command 都有互動式設定，狀態存在 `.ui-design/`。

**Commands**

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/ui-design:design-system-setup` | `[--preset minimal\|standard\|comprehensive]` | 初始化設計系統：產生 token（色彩、字體、間距）與檔案；comprehensive 會加產文件 |
| `/ui-design:create-component` | `[元件名稱]` | 引導式建立元件，Storybook 整合可選 |
| `/ui-design:design-review` | `[檔案路徑\|元件名稱]` | 審查既有 UI，依 Critical／Major／Minor 分級列出問題 |
| `/ui-design:accessibility-audit` | `[檔案路徑\|元件名稱\|--level AA\|AAA]` | WCAG 合規稽核，有 Guided Fix Mode 可逐項修正 |

**Agents**

| Agent | Model | 專長 |
|---|---|---|
| `ui-designer` | inherit | 元件、版面、視覺設計實作 |
| `design-system-architect` | inherit | design token、多品牌主題、元件庫 |
| `accessibility-expert` | inherit | WCAG、螢幕報讀器、鍵盤導覽 |

**Skills**

| Skill | 用途 |
|---|---|
| `visual-design-foundations` | 字體、色彩、間距、圖示原則 |
| `design-system-patterns` | design token、主題切換、元件架構 |
| `web-component-design` | React／Vue／Svelte 元件模式、CSS-in-JS |
| `responsive-design` | container query、流體字級、CSS Grid |
| `interaction-design` | 微互動、轉場、loading 狀態 |
| `accessibility-compliance` | WCAG 2.2、行動裝置無障礙 |
| `mobile-ios-design` | iOS HIG 與 SwiftUI |
| `mobile-android-design` | Material Design 3 與 Jetpack Compose |
| `react-native-design` | React Native 樣式、導覽、Reanimated 動畫 |

---

## claude.ai 同步 plugin

這兩個 plugin 是從 claude.ai 帳號同步過來的，不是透過 `claude plugin install` 安裝。

### data

**用途**：讓 Claude 擔任資料分析師，協助寫 SQL、探索資料、統計分析、視覺化、做 dashboard，以及在分享前檢查分析結果。主要為 Cowork 設計，在 Claude Code 也能使用。

**手動呼叫的 skill**（用法跟 command 一樣）

| 指令 | 參數 | 做什麼 |
|---|---|---|
| `/data:analyze` | `<問題>` | 回答資料問題，從單一指標查詢到完整分析報告 |
| `/data:explore-data` | `<資料表或檔案>` | 剖析資料：形狀、null 比例、分布、可疑值 |
| `/data:write-query` | `<需要什麼資料>` | 把自然語言需求寫成指定方言的最佳化 SQL |
| `/data:create-viz` | `<資料來源> [圖表類型]` | 用 Python 產生正式報告等級的圖表 |
| `/data:build-dashboard` | `<描述> [資料來源]` | 產生單一 HTML 互動 dashboard（KPI 卡、篩選器、表格） |
| `/data:validate-data` | `<要審查的分析>` | 分享前 QA：方法、計算正確性、偏誤 |
| `/data:data-context-extractor` | — | 訪談分析師、萃取公司特有的資料知識，生成專屬的資料分析 skill；也可以改進已存在的 skill |

**只會自動載入的 skill**（`user-invocable: false`，不能手動呼叫）

- `sql-queries`：各家倉儲 SQL 方言與效能寫法
- `statistical-analysis`：敘述統計、趨勢、離群值、假設檢定
- `data-visualization`：matplotlib／seaborn／plotly 選圖與設計原則

**資料來源**：plugin 內建 MCP 連線設定，包含 bigquery、hex、amplitude、amplitude-eu、atlassian、definite、snowflake、databricks。沒有接資料倉儲時，可以直接貼查詢結果或上傳 CSV／Excel。

> README 寫的 `/validate` 跟實際 skill 名稱不一致，實際名稱是 `validate-data`。

**使用範例**

```
/data:explore-data data/orders.parquet
/data:write-query 依註冊月份分群，算 1、3、6、12 個月留存率，BigQuery 方言
```

### cowork-plugin-management

**用途**：在 **Cowork 桌面版**建立或客製 plugin。

| Skill | 做什麼 |
|---|---|
| `create-cowork-plugin` | 從零開始引導建立新 plugin，產出 `.plugin` 檔 |
| `cowork-plugin-customizer` | 依組織的工具與流程客製既有 plugin（connector、skill 設定） |

> ⚠️ 兩個 skill 的 `compatibility` 都寫明需要 Cowork 環境（掛載的 plugin 目錄與 outputs 目錄），在 Claude Code CLI 裡大多無法正常運作。

---

## 情境速查

| 我想要… | 首選 |
|---|---|
| 微調一個 LLM | `/llm-finetuning:finetune` |
| 判斷該微調還是做 RAG | skill `finetuning-method-selection` 或 agent `llm-finetuning-architect` |
| 建 RAG／向量檢索 | agent `ai-engineer` ＋ skill `rag-implementation`、`embedding-strategies` |
| 做推薦／排序系統 | skill `recsys-pipeline-architect` |
| 傳統 ML 從資料到上線 | `/machine-learning-ops:ml-pipeline` |
| 建資料管線（ETL／ELT） | `/data-engineering:data-pipeline` 或 agent `data-engineer` |
| 調慢的 Spark job | skill `spark-optimization` |
| 寫 Airflow DAG／dbt 模型 | skill `airflow-dag-patterns`／`dbt-transformation-patterns` |
| 快速看懂一份新資料 | `/data:explore-data` |
| 寫分析 SQL | `/data:write-query` |
| A/B 測試驅動的功能 | `/data-engineering:data-driven-feature` |
| 起新的 Python 專案 | `/python-development:python-scaffold` |
| 包一個推論 API | agent `python-development-fastapi-pro` |
| 後端功能從需求到部署 | `/backend-development:feature-development` |
| 安全審查 | agent `backend-development-security-auditor` |
| 一個功能要做 Web＋App | `/multi-platform-apps:multi-platform` |
| 檢查 UI 無障礙 | `/ui-design:accessibility-audit` |
| 把模型部署到 K8s | agent `kubernetes-operations-kubernetes-architect` ＋ skill `k8s-manifest-generator`、`helm-chart-scaffolding` |
| 建監控／告警 | `/observability-monitoring:monitor-setup` |
| 定 SLO 與 error budget | `/observability-monitoring:slo-implement` |

---

## 注意事項

1. **重複的 agent**：以下 agent 在多個 plugin 各有一份，內容只差在 `name` 欄位，挑哪一個都一樣：
   - `backend-architect`：backend-development、data-engineering、multi-platform-apps
   - `frontend-developer`、`mobile-developer`：frontend-mobile-development、multi-platform-apps

   另外，`performance-engineer` 雖然同名，**內容不同**：backend-development 版是短版、固定 sonnet，偏功能開發時的效能審查；observability-monitoring 版是長版、model 為 inherit，偏可觀測性和全系統調校。
2. **Orchestrator 會在專案根目錄寫檔**：`.feature-dev/`、`.data-driven-feature/`、`.multi-platform/`、`.ui-design/`，`llm-finetuning` 則是 `eval/` 與 `runs/`。需要的話記得加進 `.gitignore`，或決定要不要 commit。
3. **固定模型的 agent**：有 11 個 agent 固定用 opus、7 個固定用 sonnet（見各表 Model 欄），主對話切換模型不會影響它們。
4. **data plugin 的連線狀態**：`definite` MCP 這次 session 連不上（ENDPOINT_NOT_FOUND）；`snowflake`、`databricks` 在 `.mcp.json` 裡的 URL 是空的，要自己填才能用。其他倉儲則需要先執行 `authenticate` 授權。
