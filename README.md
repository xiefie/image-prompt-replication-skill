# Image Prompt Replication Skill

[简体中文](README.zh-CN.md) · English

![Version](https://img.shields.io/badge/version-1.0.0-2563eb.svg)
![License](https://img.shields.io/badge/license-MIT-16a34a.svg)
![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827.svg)

A Codex skill for reverse-engineering image-generation prompts, diagnosing differences between a reference and a generated image, and extracting only the visual style that can safely transfer to a new subject.

> The goal is high perceptual similarity through a controlled workflow—not a false promise of pixel-perfect reproduction from text alone.

## Why this project exists

“Describe this image as a prompt” looks simple, but it hides several hard problems:

- A visual result has many coupled variables: layout, perspective, subject geometry, lighting, color, material, rendering, and fine detail.
- Models may produce different images from the same prompt because the model version, seed, aspect ratio, sampler, and reference controls vary.
- Prompt revisions often grow into contradictory adjective lists instead of fixing the largest visible error.
- Style extraction easily leaks scene content, clothing, props, poses, or concrete colors into a supposedly reusable style prompt.
- Exact identity, typography, or geometry may be poorly controlled by text and require image conditioning, structure control, inpainting, or compositing.

This skill turns those failure modes into a repeatable, diagnosable workflow.

## What it does

| Mode | Input | Output |
| --- | --- | --- |
| Reconstruction | One reference image | Compact visual analysis, copy-ready English prompt, optional negative prompt and generator-specific controls |
| Correction | Original image, generated result, and previous prompt | Ranked visual differences, minimal correction strategy, optimized complete prompt |
| Style extraction | One style reference | Exactly two or three concise Chinese sentences containing transferable style only |

Key behaviors:

- Preserves the user's favorite feature or stated mismatch as the highest-priority target.
- Ranks similarity by perceptual impact: composition and silhouette before micro-detail.
- Separates observed evidence from uncertain guesses about lenses, renderers, or media.
- Changes only the top one to three causes in each correction pass.
- Keeps content out of style-only prompts unless the user explicitly asks to preserve it.
- Recommends the smallest appropriate control upgrade when text prompting reaches its limit.

See [Design rationale](docs/DESIGN.md) for the full problem model, priorities, and non-goals.

## Repository structure

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

The installable skill is self-contained inside `image-prompt-replication/`. Repository documentation and automation stay outside the skill package so they do not consume skill context.

## Installation

### Option A: Download a release

1. Open the latest GitHub Release.
2. Download `image-prompt-replication-skill.zip`.
3. Extract it into your personal Codex skills directory:

```text
${CODEX_HOME:-$HOME/.codex}/skills/
```

After extraction, the entrypoint should be:

```text
${CODEX_HOME:-$HOME/.codex}/skills/image-prompt-replication/SKILL.md
```

### Option B: Clone the repository

```bash
git clone https://github.com/xiefie/image-prompt-replication-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R image-prompt-replication-skill/image-prompt-replication "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Start a new Codex task or refresh skill discovery if the newly installed skill is not visible in the current task.

## Usage

You can invoke the skill explicitly with `$image-prompt-replication`, or describe a matching task naturally.

### 1. Reverse-engineer a reference image

Upload one reference image, then ask:

```text
Use $image-prompt-replication to reverse-engineer this image into a high-similarity English generation prompt. The part I care about most is the dramatic side lighting and restrained composition.
```

### 2. Correct a generated result

Upload the original first and the generated image second, and include the prompt used:

```text
Use $image-prompt-replication to compare image 1 with image 2. The camera angle and subject proportions feel wrong. Diagnose the largest differences and revise my previous prompt without changing the parts that already match.
```

### 3. Extract transferable style only

Upload a style reference, then ask:

```text
Use $image-prompt-replication to extract only the transferable visual style. Do not include the person, clothing, pose, objects, scene, background, or concrete subject colors.
```

## Practical tips

- Name your target generator when you want generator-specific syntax or controls.
- Keep the model/version, aspect ratio, and seed fixed while diagnosing prompt changes.
- Label the original and generated images if their upload order is unclear.
- State the one feature that matters most; this gives the skill a stable priority anchor.
- For identity, pose, depth, edges, typography, or exact geometry, expect to use reference conditioning or local editing rather than prompt expansion alone.

## Limitations and responsible use

- No text prompt can guarantee a pixel-identical result across stochastic image generators.
- Lens, renderer, and medium identification from a finished image may be uncertain; the skill labels uncertain inferences instead of presenting them as metadata.
- Results depend on the capabilities and policies of the image-generation tool you use.
- Only reproduce or transform images you have the right to use, and respect applicable copyright, privacy, likeness, and platform rules.

## Validation

Run the dependency-free validator locally:

```bash
python3 scripts/validate_skill.py
```

GitHub Actions runs the same validation for every push and pull request.

## Contributing

Focused corrections based on real prompt failures are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Security

This project contains prompt instructions and no runtime network code. If you find a prompt-injection, packaging, or supply-chain concern, follow [SECURITY.md](SECURITY.md).

## License

Released under the [MIT License](LICENSE).

## Related official documentation

OpenAI's Skills API accepts skill files as a directory upload or a ZIP bundle: [Create a skill](https://developers.openai.com/api/reference/python/resources/skills/methods/create).
