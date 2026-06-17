# PPT Brief HITL

只负责两件事：

1. PPT Content Brief 的 HITL 交互过程和回复格式模板。
2. `ppt_content_brief.md` 的最终落盘协议，避免前置阶段没说清楚，写完后再被 QA 牵着返工。

内容表达方式、证据优先级、金字塔逻辑、页面标题质量和边界表述原则，统一遵循 `references/evidence-principle.md`。

## 对话规则

- 遵循 `SKILL.md` 中的顶层 HITL 交互规则。
- 请求用户审批可见 slide copy 时，必须使用最终会进入 `ppt_content_brief.md` 的字段；不要让用户审批之后还要重新解释的松散段落。
- 所有 Summary Page 和内容页候选在给人类审批前，都可以先运行轻量 visible-copy QA，检查 `页面标题`、`标题说明` 和 `分析总结` 是否过长或不合格，避免最终大 QA 返工：

```powershell
python scripts/validate_ppt_content_brief.py --visible-copy-check --summary-page --title "<页面标题>" --subtitle "<标题说明>" --analysis-bullet "小标题：解释"
```

- 每个审批请求都必须使用本文件对应 gate 写出的回答模板。
- 多候选 gate 有几个候选，就只列几个编号选项；不要额外添加 `自定义`、`修改后继续` 或解释性选项文字。
- 单候选 gate 只列 `1. 批准`；用户需要修改时，直接按同一个 gate 模板改写。

## 阶段 Gates

每个阶段都有两个 gate：

1. 请求用户审批或修正阶段输出。
2. 将已审批结果更新到 `<workspace-root>/baselines/ppt_brief_hitl.json` 的对应字段。

不要静默改写已审批字段。如果后续发现需要修改，先询问是否修订，再更新 JSON 中对应字段。

统一 HITL JSON 只保存已审批结果，不保存候选草稿。schema：

```json
{
  "topic": "string",
  "source_set": ["string"],
  "scqa": {
    "situation": "string",
    "complication": "string",
    "question": "string",
    "answer": "string"
  },
  "page_count": {
    "total_pages": 7,
    "counting_rule": "string",
    "page_structure": ["Page 1 cover", "Page 2 summary"]
  },
  "summary_page": {
    "page_number": "Page 2",
    "title": "string",
    "subtitle": "string",
    "analysis": ["小标题：解释"],
    "notes": "string"
  },
  "table_of_contents": [
    {"index": "01", "title": "string", "description": "string"}
  ],
  "content_pages": [
    {
      "page_number": "Page 4",
      "section": "string",
      "title": "string",
      "subtitle": "string",
      "analysis": ["小标题：解释"],
      "claims_to_support": ["string"],
      "boundaries": ["string"],
      "notes": "string"
    }
  ]
}
```

## 工作流程

在 `SKILL.md` 的受众 gate 审批并保存后开始。

### 1. 确认 SCQA 和 Summary Page

给出 SCQA 与 3 个具体 summary-page 候选：

```text
SCQA：
- 情境：...
- 冲突：...
- 问题：...
- 答案：...
【A】
页面标题：...
标题说明：...
分析总结（1~3个）：
- 小标题：解释
- ...
- ...
【B】
页面标题：...
标题说明：...
分析总结（1~3个）：
- 小标题：解释
- ...
- ...
【C】
页面标题：...
标题说明：...
分析总结（1~3个）：
- 小标题：解释
- ...
- ...
```

审批通过后，更新 HITL JSON 的 `scqa` 和 `summary_page` 字段：

```text
<workspace-root>/baselines/ppt_brief_hitl.json
```

### 2. 确认页数

给出 3 个页数候选：

```text
1. <总页数> 页
页数口径：<是否包含 cover / summary / contents>
页面结构：<Page 1 ...，Page 2 ...>
适用场景：<什么情况下适合这个页数>

2. <总页数> 页
页数口径：<是否包含 cover / summary / contents>
页面结构：<Page 1 ...，Page 2 ...>
适用场景：<什么情况下适合这个页数>

3. <总页数> 页
页数口径：<是否包含 cover / summary / contents>
页面结构：<Page 1 ...，Page 2 ...>
适用场景：<什么情况下适合这个页数>
```

单页输出只生成 `Summary Page`。

审批通过后，更新 HITL JSON 的 `page_count` 字段：

```text
<workspace-root>/baselines/ppt_brief_hitl.json
```

### 3. 确认目录

只在页数审批后创建目录。目录是章节层，不是逐页清单。

三层目录约束：

- 第 1 层是 deck 页数结构：cover、summary、contents、content pages。
- 第 2 层是 `Table of Contents` 章节项，最多 3 项。
- 第 3 层是 `Page Content` 页面；每个内容页的 `所属章节` 必须精确匹配一个目录 `小标题`。

内容页数量可以多于目录项数量；多个内容页可以归属同一个目录项。不要为了匹配 Page 4-7 而生成 4 个目录项。

```text
01 小标题：...
说明：...

02 小标题：...
说明：...

03 小标题：...
说明：...
```

审批通过后，更新 HITL JSON 的 `table_of_contents` 字段：

```text
<workspace-root>/baselines/ppt_brief_hitl.json
```

### 4. 确认页面观点

目录审批后，一次确认一个实际 PPT 页面。除非用户明确要求快捷流程，不要一次审批所有页面或整章页面。

每页审批提案必须使用这个模板：

```text
Page N
所属章节：<必须精确匹配某个目录小标题>
页面标题：...
标题说明：...
分析总结（1~3个）：
- 小标题：解释
- ...
- ...
```

每页审批通过后，将该页追加或更新到 HITL JSON 的 `content_pages` 字段：

```text
<workspace-root>/baselines/ppt_brief_hitl.json
```

### 5. 生成骨架并扩写

写 `ppt_content_brief.md` 前，先从 HITL JSON 生成骨架：

```powershell
python scripts/hitl_json_to_brief_skeleton.py <workspace-root>/baselines/ppt_brief_hitl.json <workspace-root>/ppt_content_brief.md
```

如需将受众信息写入骨架，传入主流程保存的受众 baseline：

```powershell
python scripts/hitl_json_to_brief_skeleton.py <workspace-root>/baselines/ppt_brief_hitl.json <workspace-root>/ppt_content_brief.md --audience-baseline <workspace-root>/baselines/01-audience.md
```

AI 只基于骨架扩写 `正文内容`、`参考图片` 和 `备注`，不要改写已审批的 metadata、Summary Page、目录、页面标题、标题说明和 `分析总结`。

扩写规则：

- `正文内容` 是 PPT 制作者的主内容池，不是审计记录。写成可直接改写成页面正文、图注、解释段和 speaker notes 的中文材料。
- Summary Page 密度最高，要同时压缩顶层结论、章节逻辑、关键数字/机制、决策含义、视觉线索和边界提醒。
- 内容页正文围绕该页 `分析总结` 展开。每个 `分析总结` label 必须在 `正文内容` 中再次出现，作为支撑 anchor，并跟随机制、事实、比较、例子、影响或边界。
- 正文不要 padding。用源材料中的 named components、actors、metrics、process steps、comparisons、constraints、adoption implications 来增加信息密度。
- `参考图片` 优先使用源图、表格、截图或图示。每个本地图片用 Markdown 图片引用，路径使用绝对路径，例如 `![Figure 1: 方法总览](D:\absolute\path\image.png)`。
- 图片说明只写图展示了什么、支撑了什么 claim；不要规定版式、模板、字体、颜色、列数或强制插入方式。
- `备注` 只放短 speaker note、脚注或不适合放正文里的克制边界。
- 不要新增顶层字段，例如 `页面角色`、`Source Locator`、`visual_strategy`、`证据边界`、`Claim/Evidence/Implication`。需要保留的边界要改写进 `正文内容` 或 `备注`。
- 字数目标：Summary Page 至少 1200 counted content characters；每个内容页至少 900 counted content characters。强技术/决策内容页通常应达到 1200-1800 counted content characters。

扩写后运行：

```powershell
python scripts/validate_ppt_content_brief.py <workspace-root>/ppt_content_brief.md --min-page-content-chars 900 --min-summary-content-chars 1200 --allow-absolute-paths
```

固定页数输出要添加 `--expected-pages <n>`，其中 `<n>` 是 total PPT pages。
