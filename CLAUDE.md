# AI Berkshire — 项目指令

## 项目概述

基于 Claude Code 的价值投资研究 Skill 合集。四大师框架：Warren Buffett(버핏)、Charlie Munger(멍거)、段永平(돤융핑)、李录(리루)。
GitHub: xbtlin/ai-berkshire

## 项目结构

```
skills/          — 投研 Skill 定义（.md），复制到 ~/.claude/commands/ 使用
tools/           — 辅助工具（financial_rigor.py 精确计算）
reports/         — 投资研究报告输出
assets/          — 图片等静态资源
```

## 报告目录结构

所有报告按**公司名**建文件夹，公司相关的所有报告放在对应文件夹内。

> **명명 규칙(앞으로 생성분)**: 신규 보고서 폴더는 **한국어 회사명**을 사용한다(예: `삼성전자/`, `카카오/`, `에코프로비엠/`). 한국 미상장/외국 종목은 한글 통용명 우선, 없으면 영문 티커(예: `엔비디아/` 또는 `NVDA/`). 기존 중국어/영문 폴더(腾讯/, Adobe/ 등)는 그대로 유지한다.

```
reports/
├── AI产业研究/              — AI产业链全景研究（置顶）
│   ├── AI五层蛋糕-产业全景研究-20260605.md
│   └── AI五层蛋糕-公众号-20260605.md
├── 腾讯/                    — 腾讯所有研究报告
│   ├── 腾讯-research-20260408.md
│   ├── 腾讯-earnings-2025Q4.md
│   ├── 腾讯-management-20260409.md
│   └── 腾讯-thesis.md
├── 拼多多/                  — 拼多多所有研究报告
├── 泡泡玛特/                — 泡泡玛特所有研究报告
├── 核电-industry-20260409.md — 行业报告放根目录
├── AI算力-funnel-20260509.md  — 漏斗筛选报告放根目录
├── AI-轮动判断-20260509.md    — 主题级综合判断报告放根目录
├── portfolio-latest.md       — 组合报告放根目录
└── 多公司对比-checklist-20260408.md — 多公司报告放根目录
```

## 报告命名规范

| Skill | 文件命名格式 | 示例 |
|------|---------|------|
| /investment-team | `{公司名}/` 目录内含4个视角+最终报告 | `reports/拼多多/最终报告.md` |
| /investment-research | `{公司名}-research-{YYYYMMDD}.md` | `reports/腾讯/腾讯-research-20260408.md` |
| /investment-checklist | `{公司名}-checklist-{YYYYMMDD}.md` | `reports/腾讯/腾讯-checklist-20260408.md` |
| /industry-research | `{行业名}-industry-{YYYYMMDD}.md`（根目录） | `reports/核电-industry-20260409.md` |
| /industry-funnel | `{行业名}-funnel-{YYYYMMDD}.md`（根目录） | `reports/AI算力-funnel-20260509.md` |
| /private-company-research | `{公司名}-private-{YYYYMMDD}.md` | `reports/字节跳动/字节跳动-private-20260408.md` |
| /earnings-review | `{公司名}-earnings-{期间}.md` | `reports/腾讯/腾讯-earnings-2025Q4.md` |
| /earnings-team | `{公司名}/` 目录内含4个大师视角+研究底稿+公众号文章+读者评审 | `reports/腾讯/腾讯-earnings-2025Q4.md`（公众号定稿） |
| /thesis-tracker | `{公司名}-thesis.md`（长期维护） | `reports/腾讯/腾讯-thesis.md` |
| /portfolio-review | `portfolio-latest.md`（根目录，持续更新） | `reports/portfolio-latest.md` |
| /management-deep-dive | `{公司名}-management-{YYYYMMDD}.md` | `reports/腾讯/腾讯-management-20260409.md` |

## /investment-team 文件结构

```
reports/{公司名}/
├── README.md                         — 研究框架概览+核心结论
├── 01-商业模式分析-段永平(돤융핑)视角.md
├── 02-财务估值分析-Warren Buffett(버핏)视角.md
├── 03-行业竞争分析-Charlie Munger(멍거)视角.md
├── 04-风险管理层评估-李录(리루)视角.md
└── 最终报告.md                       — Team Lead 综合报告
```

## 投研分析核心原则（最高优先级）

- **客观、客观、客观**——所有投研分析必须基于事实和数据，严禁主观臆断
- 严格区分"事实"与"观点"：事实用数据支撑，观点必须明确标注为"观点"或"推测"
- **不预设立场**：不预设看多或看空，先摆数据、再推逻辑、最后得结论。结论必须从数据中自然推出
- 禁止使用"我认为"、"我觉得"、"显然"等主观表述，改用"数据显示"、"证据表明"、"根据XX来源"
- **呈现正反两面**：每个核心判断都必须附带反面论据（"但另一方面..."），让读者自己权衡
- 对不确定的事情诚实说"不确定"或"数据不足"，不要用推测填充确定性
- 所有skill（investment-team、investment-research、earnings-review等）在执行时都必须遵守以上原则

## 报告语言与风格

- **所有报告使用韩语（한국어）**——正文、结论、表格、点评一律用韩语撰写
- Warren Buffett(버핏)/Charlie Munger(멍거)/段永平(돤융핑)/李录(리루)的语录点评用**韩语**呈现（首次出现可附原文，后续用韩语）
- 估计值必须注明"추정"（估计）；不确定时写"불확실 / 데이터 부족"
- 风格：直接、犀利、不说废话（직설적·날카롭게, 군더더기 없이）
- 数据必须标注来源，关键数据至少2个来源交叉验证
- 评分使用★符号（★1-5），不含半星
- 术语首次出现时可附英文/原文，便于跨市场对照（예: 해자(moat), 안전마진(margin of safety)）

## GitHub 操作

- 本地克隆路径：`~/ai-berkshire/`
- 远程仓库：`https://github.com/xbtlin/ai-berkshire.git`
- 推送前先 `git pull --rebase origin main`（远程经常有新提交）
- commit message 用中文，描述清楚改了什么
- 不要推送中间过程文件（如 data_collection.md），只推最终报告

## 常用命令

```bash
# 推送报告到GitHub
cd ~/ai-berkshire
git add reports/xxx.md
git commit -m "添加xxx报告"
git pull --rebase origin main
git push origin main
```

## 注意事项

- 市值必须手算校验：股价 × 总股本，与报告市值对比
- 货币单位要明确（韩元 KRW / 美元 USD / 港币 HKD / 人民币 CNY），防止混淆
- 韩股金额单位用 **억원(亿韩元) / 조원(万亿韩元)**，美股用 USD，注意换算时点
- PE/ROE等指标用 tools/financial_rigor.py 精确计算（--currency 传 KRW/USD 等）
- 报告写完后主动询问是否推送到GitHub

## 市场与数据工具路由

| 市场 | 数据工具 | 备用来源 |
|------|---------|---------|
| 韩股（KOSPI/KOSDAQ） | `py tools/krx_data.py quote\|valuation\|financials\|search {코드}` | 네이버 금융 / DART(dart.fss.or.kr) / KRX |
| 美股（NYSE/NASDAQ） | WebSearch + macrotrends/stockanalysis/SEC EDGAR | 见 skills/financial-data.md |
| A股（沪/深） | `py tools/ashare_data.py quote\|valuation\|financials\|search {代码}` | 东方财富 / 巨潮资讯 |
| 港股 | WebSearch + aastocks/macrotrends ADR | HKEX 披露易 |

> 韩股代码为 6 位数字（例: 삼성전자 005930, 카카오 035720）。Windows 用 `py`，类Unix 用 `python3`。
