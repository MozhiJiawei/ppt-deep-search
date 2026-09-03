# Source Understanding HTML PPT

本文件规定如何编排multi-agent，完成内容解析与source Understanding制作
multi-agent原则：必须按照prompt模板，启动子agent，你需要将prompt里的占位符具象化，但不允许添加任何额外说明

稳定子 agent 角色定义放在本 skill 子仓的 `.codex/agents/*.toml`。TOML 保存原 prompt 中已调好的静态要求；本文件继续保存每次任务的动态占位内容。

每次委派都必须补全三个绝对路径：主工作区根目录 `<absolute-workspace-root>`、本次用户工作的 `<absolute-work-root>`、该子 agent 独占的输出路径。所有后代委派必须原样传递 `<absolute-work-root>`，不得另建工作目录。`<workspace-root>` 专指 `<absolute-work-root>/ppt-deep-search/`。

## 来源准备 HITL（主Agent完成）

先根据用户输入的信源、主题和已知缺口判断输入类型。所有场景都写入 `<workspace-root>/sources/source-selection.md`。
  - 输入类型：`web` 或 `paper`。
  - 原始来源清单。

```text
请先确认 Source Understanding 的信息来源。。

原始页面（最多 3 个）：
1. <标题> — <URL>
   选择理由：<为什么它是原始/高相关来源>
2. <标题> — <URL>
   选择理由：<为什么它是原始/高相关来源>
3. <标题> — <URL>
   选择理由：<为什么它是原始/高相关来源>

1. 批准
```

## 信息爬取（委派子Agent完成）

### 网页

来源按页面分别委派给 Codex custom agent `web_source_capturer`。每个子 agent 只处理一个网页，产出独立 source package，并运行页面 validator。

给子agnet的动态补充：
```text
主工作区根目录：<absolute-workspace-root>
当前工作根目录：<absolute-work-root>

网页：
- 标题：<title>
- URL：<url>
- Source slug：<source-slug>

输出目录：
<workspace-root>/sources/web/<source-slug>/
```

### 论文

来源按论文分别委派给 Codex custom agent `paper_source_parser`。每个子 agent 只处理一篇论文

给子agnet的动态补充：
```text
主工作区根目录：<absolute-workspace-root>
当前工作根目录：<absolute-work-root>

论文：
- 标题：<title>
- URL：<url>
- Source slug：<source-slug>

输出目录：
<workspace-root>/sources/papers/<source-slug>/
```

## 制作 HTML PPT（委派子Agent完成）

委派 Codex custom agent `source_understanding_deck_maker` 制作 Source Understanding HTML deck。

给子agnet的动态补充，信息源仅提供与该子agent相关的：
```text
主工作区根目录：<absolute-workspace-root>
当前工作根目录：<absolute-work-root>

信息源： <path1>, <path2>, <path3>, ...

输出目录：
<workspace-root>/review/source_understanding_review.html

```

## 审批 Gate（主Agent完成）

HTML 生成后，请用户审阅是否批准作为后续证据基线：

```text
请审阅 source-understanding HTML：
<workspace-root>/review/source_understanding_review.html

是否批准该来源理解作为本轮 Source Understanding 结果？

1. 批准
```

审批通过后，保存 `<workspace-root>/baselines/015-source-understanding.md`。
