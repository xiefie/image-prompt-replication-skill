# Design rationale

[简体中文](DESIGN.zh-CN.md) · English

## Design purpose

Image prompt reconstruction is an inverse problem: the user provides a finished result, while the system must infer a useful set of generation controls from pixels alone. Many different prompts and model settings can produce similar images, and a visually plausible description is not necessarily a reproducible prompt.

This skill is designed to make that inverse problem more controllable. It translates images into observable constraints, ranks those constraints by perceptual impact, and keeps prompt revisions small enough to diagnose.

## Problems addressed

### 1. Description is not reconstruction

A normal image caption tells the reader what is depicted. A reconstruction prompt must also encode spatial relationships, crop, perspective, subject scale, light direction, tonal hierarchy, surface response, and rendering behavior.

The skill therefore treats the image as a physical arrangement rather than a story.

### 2. Important differences are not equally important

A small texture mismatch rarely matters when the camera angle or silhouette is wrong. Unranked analysis wastes prompt budget and makes correction unstable.

The default priority order is:

1. spatial layout and silhouette;
2. camera and perspective;
3. subject proportions, pose, and relationships;
4. lighting and tonal hierarchy;
5. color treatment;
6. materials and rendering;
7. micro-detail.

The user can override this order by naming the feature they care about most.

### 3. Prompt accumulation hides causal relationships

Appending adjectives after every failed generation creates contradictions and makes it impossible to know what caused an improvement or regression.

Correction mode ranks visible differences and changes only the top one to three causes per pass. Clauses that already work remain stable.

### 4. Style and content are routinely mixed

A reusable style should describe visual treatment—not the depicted person, clothing, pose, props, scene, or object colors. Mixing these categories makes style transfer brittle.

Style extraction therefore uses an explicit inclusion/exclusion boundary and expresses color as an abstract treatment unless a concrete color is itself essential to the style.

### 5. Text prompting has a real control ceiling

Exact identity, typography, pose, depth, edges, and geometry can be underdetermined by text. Longer prompts do not necessarily add control.

When iteration stalls, the skill recommends the smallest relevant upgrade: fixed model and seed, matching aspect ratio, reference conditioning, pose/depth/edge control, inpainting, or direct compositing.

## Architecture

The skill uses progressive disclosure:

- `SKILL.md` contains routing, shared invariants, and iteration discipline.
- `references/workflows.md` contains the detailed procedure and output contract for each mode.
- `agents/openai.yaml` supplies user-facing metadata and an invocation example.

Repository documentation, validation, and release files stay outside the installable skill directory. This keeps the loaded skill context focused.

## Mode design

### Reconstruction

Reconstruction converts one image into a structured English prompt. The prompt is ordered from the highest-priority visual anchor through subject geometry, composition, camera, lighting, color, materials, rendering, and anti-drift constraints. Negative prompts are optional and used only for likely failure modes.

### Correction

Correction compares an original and a generated result directly. Each material mismatch is reasoned about as:

```text
original evidence → generated deviation → likely prompt cause → smallest correction
```

The output includes ranked differences, a concise modification strategy, and a complete revised prompt.

### Style extraction

Style extraction intentionally has a strict output contract: exactly two or three concise Chinese sentences, with no heading, list, analysis, or explanation. This makes the result directly copyable and reduces content leakage.

## Design principles

- **Perceptual similarity over vocabulary density.** More words are not automatically more control.
- **Observable evidence over confident guessing.** Uncertain lens, medium, and renderer attributions are labeled as uncertain.
- **Stable invariants over full rewrites.** Successful clauses persist across correction passes.
- **Tool-agnostic first.** Neutral English syntax is the default; generator-specific weights or parameters appear only when the generator is known.
- **Content/style separation.** Style-only mode does not silently preserve scene content.
- **Honest limits.** The workflow never promises deterministic or pixel-identical reproduction from text alone.

## Non-goals

This project does not:

- generate images by itself;
- guarantee identical results across models or runs;
- infer hidden camera metadata with certainty;
- replace image-to-image, structural controls, local editing, or compositing;
- grant permission to copy protected, private, or unauthorized source images;
- prescribe one vendor's prompt dialect as a universal standard.

## Success criteria

The skill is working as intended when:

- the generated prompt is copy-ready and has no internal contradictions;
- the user's priority feature is clearly preserved;
- correction output identifies a small number of high-impact changes;
- successful constraints remain stable between iterations;
- style extraction can be applied to a different subject without importing the reference scene;
- the assistant stops expanding the prompt when another control method is more appropriate.

