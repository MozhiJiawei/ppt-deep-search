# 使用方式

`ppt-deep-search` 是生成 PPT 前的来源理解审阅流程。它不生成 PPT、不规划页数目录、不产出内容简报；做到 `source_understanding_review.html` 并完成审批后结束。

## 适用场景

使用这个 skill 处理以下任务：

- 从论文、网页、Markdown、仓库分析、PDF、笔记或原始材料中整理技术理解。
- 在正式生成 HTML 演示文稿之前，先确认来源证据、关键机制、可用图片和证据边界。
- 把网页 source package、论文解析结果、Source Understanding HTML、截图和视觉 QA 记录留在同一个运行目录中，便于后续人工审阅或另起 PPT-GEN 任务。

不要用它做演示文稿视觉渲染、版式模板、字体配色、导出 PPT、页数规划、目录规划、SCQA 或逐页观点生成。这些属于下游 PPT-GEN。

## 标准流程

默认走 human-in-the-loop：

1. 确认 Source Understanding 的信息来源，包括原始来源和必要的同类方案。
2. 对网页来源调用 `web-article-capture`，对论文来源调用 `grobid-docling-pdf`，把结构化来源产物写入 `<workspace-root>/sources/`。
3. 基于来源产物制作 `review/source_understanding_review.html`。
4. 导出 Source Understanding PNG 到 `review/source-understanding-images/`。
5. 委派独立视觉 QA checker，写入 `review/visual-qa.md`。
6. 请求用户审批 Source Understanding，并保存 `baselines/015-source-understanding.md`。

审批通过后，本 skill 的职责结束。后续是否生成 PPT，由用户另起请求交给 PPT-GEN。

## 工作目录

一次运行只使用一个 `workspace-root`：

- 默认路径：`.tmp/ppt-deep-search/<task-name>/`
- forward-test 路径：`.tmp/forward-tests/<case-id>/<run-id>/`
- 用户指定输出目录时，以用户指定目录为准

所有临时笔记、baseline、资产和 QA 输出都放在这个目录下。

最终要求产物：

- `<workspace-root>/review/source_understanding_review.html`
- `<workspace-root>/review/source-understanding-images/`
- `<workspace-root>/review/visual-qa.md`
- `<workspace-root>/baselines/015-source-understanding.md`
- `<workspace-root>/sources/**`

## 校验命令

Source Understanding HTML 写完后，运行：

```powershell
python scripts/validate_source_understanding_html.py <workspace-root>/review/source_understanding_review.html all <workspace-root>/review/source-understanding-images
```

仓库级依赖与契约检查：

```powershell
python verify_dependencies.py
```
