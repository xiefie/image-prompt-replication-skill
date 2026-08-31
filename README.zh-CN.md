# 图像复刻提示词工作流 Skill

简体中文 · [English](README.md)

![版本](https://img.shields.io/badge/version-1.0.0-2563eb.svg)
![许可证](https://img.shields.io/badge/license-MIT-16a34a.svg)
![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827.svg)

这是一个面向 Codex 的图像提示词工作流：从参考图反推生图提示词，对比原图和生成图进行定向纠错，或只提取能够迁移到其他主体上的视觉风格。

> 项目目标是通过可控、可诊断的流程获得高度相似的视觉结果，而不是承诺仅靠文字提示词实现像素级 100% 复刻。

## 为什么需要这个项目

“把一张图描述成提示词”看起来很简单，实际包含多个互相耦合的问题：

- 一张图同时受空间布局、透视、主体几何、光线、色彩、材质、渲染方式和细节密度影响。
- 即使提示词完全相同，模型版本、随机种子、画幅、采样器和参考图控制参数不同，也可能生成明显不同的结果。
- 常见纠错方式只是不断追加形容词，最终造成提示词冲突，却没有解决最显眼的构图或镜头问题。
- 风格提取很容易混入人物身份、服装、道具、姿势、场景和具体颜色，导致风格无法迁移。
- 身份一致性、文字、精确几何等内容通常不是纯文字提示词擅长控制的，需要参考图、结构控制、局部重绘或合成。

这个 skill 将这些不稳定因素整理成可重复、可比较、可逐轮收敛的工作流。

## 能解决什么问题

| 模式 | 输入 | 输出 |
| --- | --- | --- |
| 复刻反推 | 一张参考图 | 简洁视觉分析、可复制英文提示词、可选负面提示词与特定生成器控制建议 |
| 双图纠错 | 原图、生成结果和上一版提示词 | 按影响排序的差异、最小修改策略、完整优化提示词 |
| 风格提取 | 一张风格参考图 | 只包含可迁移风格的两到三句中文提示词 |

核心行为：

- 把用户最喜欢的部分或明确指出的“不像”作为最高优先级。
- 按感知影响排序：先解决构图、轮廓和镜头，再处理微小纹理。
- 区分可观察事实和对镜头、渲染器、媒介的推测。
- 每轮只修正影响最大的一个到三个变量，保留已经正确的约束。
- 风格提取默认排除人物、服装、姿势、道具、场景和具体主体颜色。
- 当文字提示词达到控制上限时，推荐最小必要的图生图、姿势/深度/边缘控制、局部重绘或合成方案。

完整的问题模型、设计优先级和非目标请参阅[中文设计说明](docs/DESIGN.zh-CN.md)。

## 项目结构

```text
.
├── image-prompt-replication/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/workflows.md
├── docs/
├── scripts/validate_skill.py
├── dist/image-prompt-replication-skill.zip
└── .github/
```

可安装的 skill 完整位于 `image-prompt-replication/`。仓库说明、自动校验和社区文件放在 skill 目录外，避免占用 skill 的运行上下文。

## 安装

### 方式一：下载 Release

1. 打开最新 GitHub Release。
2. 下载 `image-prompt-replication-skill.zip`。
3. 解压到个人 Codex skills 目录：

```text
${CODEX_HOME:-$HOME/.codex}/skills/
```

解压后的入口文件应位于：

```text
${CODEX_HOME:-$HOME/.codex}/skills/image-prompt-replication/SKILL.md
```

### 方式二：克隆仓库

```bash
git clone https://github.com/xiefie/image-prompt-replication-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R image-prompt-replication-skill/image-prompt-replication "${CODEX_HOME:-$HOME/.codex}/skills/"
```

如果当前任务没有立即识别新安装的 skill，可新建一个 Codex 任务或刷新 skill 发现状态。

## 使用方法

可以用 `$image-prompt-replication` 显式调用，也可以直接描述匹配的任务。

### 1. 反推参考图提示词

上传一张参考图，然后输入：

```text
使用 $image-prompt-replication 反推这张图片的英文生图提示词。我最在意的是戏剧性的侧光和克制的构图，请把它们作为最高优先级。
```

### 2. 对比生成结果并纠错

先上传原图，再上传生成图，并附上使用过的提示词：

```text
使用 $image-prompt-replication 对比图1和图2。我感觉镜头角度和主体比例不像。请找出影响最大的差异，在保留已经匹配部分的前提下修改上一版提示词。
```

### 3. 只提取可迁移风格

上传风格参考图，然后输入：

```text
使用 $image-prompt-replication 只提取可迁移的视觉风格。不要包含人物、服装、姿势、道具、场景、背景或主体的具体颜色。
```

## 提高复刻相似度的建议

- 需要特定语法或参数时，说明你使用的生图工具和模型。
- 纠错过程中固定模型版本、画幅比例和随机种子，减少无关变量。
- 如果图片上传顺序可能产生歧义，明确标注原图和生成图。
- 主动说明“最在意的一个部分”，帮助工作流建立稳定的优先级锚点。
- 身份、姿势、深度、边缘、文字或精确几何不稳定时，优先使用参考图控制或局部编辑，不要无限追加提示词。

## 能力边界与负责任使用

- 随机生图系统中，任何纯文字提示词都无法保证像素级完全一致。
- 仅凭成片无法确定精确镜头、渲染器或媒介；skill 会把不确定推断写成“接近”或“可能”，而不是伪装成元数据。
- 最终结果取决于所用生图工具的能力、版本和平台规则。
- 只复刻或转换你有权使用的图片，并遵守适用的版权、隐私、肖像权及平台要求。

## 校验

本地运行无第三方依赖的校验脚本：

```bash
python3 scripts/validate_skill.py
```

每次推送和拉取请求都会通过 GitHub Actions 执行同一套校验。

## 参与贡献

欢迎提交基于真实失败案例的聚焦修正。发起 Pull Request 前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 安全问题

项目只包含提示词说明，不包含运行时网络代码。如发现提示词注入、打包或供应链风险，请遵循 [SECURITY.md](SECURITY.md)。

## 许可证

本项目使用 [MIT License](LICENSE)。

## OpenAI 官方资料

OpenAI Skills API 支持以目录或 ZIP 压缩包的形式上传 skill 文件：[Create a skill](https://developers.openai.com/api/reference/python/resources/skills/methods/create)。
