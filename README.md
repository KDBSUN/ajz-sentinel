# 降智哨兵 · AI 降智检测器（ajz-sentinel）

[English README](README_EN.md)

一个**单文件、零依赖、浏览器本地运行**的 AI 能力检测工具。它的定位是**能力选品工具**：帮普通用户判断「哪个模型在我要做的任务上表现最好、性价比最高」，而不是服务真伪鉴定或权威学术评测。

- 打开即用：`index.html` 双击即可运行，无需安装任何东西
- 隐私安全：API Key 只存在于页面内存，检测历史只存浏览器 localStorage，永不上传
- 题库可核验：32 题，含 AIME 2026 真题、ARC-AGI-2 官方评测任务等近一年新题，每题标注来源

## 功能一览

| 模块 | 说明 |
| --- | --- |
| 组卷台 | 33 种职业预设 + 五维权重滑块（逻辑/指令/知识/代码/多模态），快速·标准·完整三档 |
| 权重驱动组卷（v8） | 快速/标准档题数按维度权重比例分配（缺口最大优先），不再是固定题数；某维题池分满后余量自动流向其他维度 |
| 模型预设（v8） | 内置 OpenAI / Claude / DeepSeek / Grok / 豆包 / 通义千问 / 小米 MiMo / GLM / Kimi / Gemini 常用模型的接口格式，选中自动填入，型号可手改 |
| 行为探针 | 思考痕迹检测、工具清单核对、计算锚点（369），辅助判断服务端降级 |
| 判分引擎 | 9 种判分器（数值/严格匹配/JSON/网格/代码运行/人工 rubric/拒答探针等），全部本地执行 |
| 基准记分卡 | 15 行基准映射，仿主流模型跑分表逐项打分 + 综合指数 |
| 历史与趋势（v8） | 按「来源域名 + 模型名」自动分组，每组独立基线与趋势图；同一来源与模型的多次检测直接对比，抓间歇掺假 |
| 社区性价比榜（v8） | 零后端多人对比：榜单数据托管在本仓库，工具内拉取；上报走 GitHub Issue + Action 自动聚合 |
| 题库热更新 | 支持从 URL 拉取题库 JSON（如本仓库的 `questions.json`），或粘贴 JSON 导入 |

## 快速开始

### 方式一：本地使用
下载 `index.html`，双击用浏览器打开。

### 方式二：GitHub Pages 部署（推荐，免费）

1. Fork 或新建仓库，把本仓库文件推送到 `main` 分支
2. 仓库 **Settings → Pages → Build and deployment**
3. Source 选 **Deploy from a branch**，Branch 选 **main / (root)**，保存
4. 等 1~2 分钟，访问 `https://<你的用户名>.github.io/<仓库名>/`

> GitHub Pages 是纯静态托管，恰好匹配本工具「全部逻辑在浏览器内」的架构；它不能运行服务器代码，因此跨用户的榜单聚合走「Issue + GitHub Action」（见下），不需要任何后端。

### 配置工具指向你的仓库

部署后在工具内填两个地址（把 `<用户>/<仓库>` 换成你的）：

- **题库 URL**（组卷台）：`https://raw.githubusercontent.com/<用户>/<仓库>/main/questions.json`
- **榜单 JSON 地址**（06 社区榜）：`https://raw.githubusercontent.com/<用户>/<仓库>/main/community/leaderboard.json`

## 社区榜数据流（零后端）

```
你的浏览器                          GitHub 仓库
──────────                        ──────────────────────────
完成检测并保存
  ↓ 「生成我的匿名上报」
复制脱敏 JSON ──粘贴到──> 「数据上报」Issue
                              ↓ 触发
                          GitHub Action（scripts/aggregate.py）
                          校验 schema → 按 host+model 聚合
                              ↓ 自动提交
                          community/leaderboard.json
                              ↓
任何人的浏览器 ←──「拉取榜单」── raw.githubusercontent.com
```

- 上报内容只有：来源**域名**（不含路径）、模型名、模式、总分、五维分、题数、时间戳
- **绝不含** API Key、完整 Base URL、题目回答或个人标识
- 聚合脚本会校验字段范围，不合规的 JSON 直接忽略

> 也可以在仓库 Insights 之外手动维护榜单：直接编辑 `community/leaderboard.json`，格式见 `schema: ajz-board-v1`。

## 隐私与安全

- API Key 只用于当前页面发起的请求，不写入 localStorage，不上传到任何地方
- 检测历史存于浏览器本地；清空浏览器数据即删除
- 上报为**手动复制粘贴**动作，工具本身不发起任何上报请求

## 免责声明

本工具用于个人能力评估与选品参考。题目与判分来自公开基准与社区题库（题面已标注来源），得分受提示词、采样、判分粒度影响，**不构成对任何模型厂商的评价结论，也不构成采购建议**。

## License

MIT，见 [LICENSE](LICENSE)。题库中各题的来源与版权归属原基准/作者所有（题面 `src` 字段已标注）。
