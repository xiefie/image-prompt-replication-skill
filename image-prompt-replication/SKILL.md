---
name: image-prompt-replication
description: Reverse-engineer, compare, and refine image-generation prompts from reference images, or extract only transferable visual style. Use for 图片复刻、反推提示词、原图与生成图纠错、风格提取；not for ordinary image descriptions.
---

# Image Prompt Replication

Turn reference images into controlled prompts that maximize perceptual similarity. Never promise pixel-perfect or “100%” reproduction from text alone: model, version, seed, aspect ratio, sampling, and reference-image controls can materially change the output.

## Route the request

- **Reconstruction:** one reference image and a request to reverse-engineer or reproduce it. Read [references/workflows.md](references/workflows.md#reconstruction).
- **Correction:** an original plus a generated result, or a complaint that a previous prompt is inaccurate. Read [references/workflows.md](references/workflows.md#correction).
- **Style extraction:** a request for reusable style without copying the depicted content. Read [references/workflows.md](references/workflows.md#style-extraction).

If the request is ambiguous, use the user's wording to choose the mode; default to reconstruction rather than mixing style extraction into it. If a required image is missing, ask the user to upload it. In correction mode, treat the first image as the original and the second as the generated result only when the user has not labeled them differently. If the previous prompt is absent, ask for it rather than pretending to revise it.

## Shared rules

1. Preserve the user's stated attraction or mismatch as the highest-priority target. If a placeholder such as `【】` is blank and the choice would materially alter the result, ask one short question; otherwise infer the dominant focal feature and state the assumption briefly.
2. Separate observable facts from uncertain inference. Use “appears to,” “likely,” or “接近” for uncertain lens, renderer, medium, or style attribution.
3. Prioritize similarity in this order unless the user says otherwise: spatial layout and silhouette; camera and perspective; subject proportions, pose, and relationships; light and tonal hierarchy; color treatment; material and rendering; micro-detail.
4. Write prompts as concrete visual instructions, not literary interpretation. Avoid contradictory adjectives, synonym piles, invented scene details, and unsupported technical claims.
5. Use neutral English prompt syntax by default. Adapt weighting and parameter syntax only when the target generator is known. Do not invent model-specific parameters.
6. Keep the positive prompt focused on desired evidence. Put exclusions in a separate negative prompt only when they prevent likely drift.
7. Do not silently carry content from a style reference into a new subject. Identity, clothing, pose, props, scene, background, logos, text, and object colors are content unless the user explicitly asks to preserve them.

## Iteration discipline

For each newly uploaded result, diagnose before rewriting. Change only the one to three variables most responsible for the visible mismatch and keep successful constraints stable. Do not trigger another paid or external generation unless the user asks; return the revised prompt for the next attempt.

When prompt-only iteration stalls, explain the limiting control and recommend the smallest relevant upgrade: fixed model/version and seed, matching aspect ratio, image-to-image/reference conditioning, pose/depth/edge control, inpainting, or direct compositing. Recommend only controls actually available in the user's tool when known.
