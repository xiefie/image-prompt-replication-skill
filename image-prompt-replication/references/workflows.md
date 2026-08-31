# Prompt workflows

## Reconstruction

Inspect the image as a reproducible physical arrangement, not as a story. Analyze only details that help regenerate it:

- **Priority anchor:** the feature the user likes most; front-load it and make it the most specific part of the prompt. Use explicit weight syntax only if the named generator supports it.
- **Subject geometry:** number and placement of subjects, scale relationships, silhouette, pose, gaze, expression, foreground/midground/background, and negative space.
- **Composition:** framing, crop, balance, symmetry, leading lines, rule of thirds, central composition, Dutch angle, and viewpoint.
- **Camera:** shot size, likely focal-length range, camera height, angle, perspective compression/distortion, focus plane, depth of field, motion characteristics. Do not claim exact metadata that is not visible.
- **Lighting:** key/fill/rim placement, hardness, direction, contrast ratio, shadow behavior, practical sources, volumetric effects, time-of-day cues, and highlight roll-off.
- **Color treatment:** palette relationships, saturation, temperature, tonal range, contrast, and grading. Use specific colors here when reproducing content; the abstract-color restriction applies only to style extraction.
- **Surface and rendering:** medium, texture, material response, line work, shading model, grain, halation, sharpness, realism/cartoonization, renderer or engine only when visually supportable.

Build the English prompt in this order:

```text
[highest-priority visual anchor], [subject and spatial relationships], [composition and crop], [camera and perspective], [lighting and tonal hierarchy], [color treatment], [materials and texture], [medium/style/rendering], [quality and anti-drift constraints]
```

Default response:

1. A compact Chinese reconstruction note covering the priority anchor, composition/camera, lighting, and style. Keep it factual.
2. `English prompt` in one copy-ready code block.
3. `Negative prompt` in a separate code block only when useful.
4. `Suggested controls` only when the user named a generator or asked for parameters. Separate confirmed settings from recommendations.

Do not include a long tutorial or multiple alternate prompts unless requested.

## Correction

Compare the original and the generated result directly. Do not judge either image in isolation. Preserve the user's stated mismatch category as the first diagnostic lens, then check:

1. layout, crop, subject size, and silhouette;
2. camera height, angle, focal-length feel, and perspective;
3. anatomy/proportions, pose, expression, and subject relationships;
4. key-light direction, softness, shadow placement, exposure, and tonal hierarchy;
5. saturation, temperature, palette relationships, and grading;
6. medium, line/shading behavior, material response, grain, halation, and detail density;
7. unwanted text, logos, artifacts, or extra objects.

For each material difference, record mentally: `original evidence → generated deviation → prompt cause → smallest correction`. Rank by perceptual impact. A large composition error outranks a small texture error.

Revise the previous prompt with these rules:

- Keep clauses that already match.
- Strengthen or move forward the missing constraint.
- Replace ambiguous or conflicting wording instead of appending more adjectives.
- Remove clauses that caused drift.
- Add a negative constraint only for a concrete recurring failure.
- Fix at most the top three causes per pass so the next result remains diagnosable.

Default response:

```text
主要差异：
1. [highest-impact mismatch and likely prompt cause]
2. [next mismatch, if material]
3. [next mismatch, if material]

修改策略：[what remains fixed; what changes]

Optimized English prompt:
[complete copy-ready prompt]

Negative prompt:
[only if useful]
```

If the mismatch is mainly identity, exact geometry, typography, or another detail text prompts control poorly, say so plainly and recommend an image-reference, structure-control, inpainting, or compositing step rather than endlessly lengthening the prompt.

## Style extraction

Extract only reusable visual treatment. Do not describe the depicted content.

Include, when visible: medium or art form, rendering/shading method, degree of stylization, lens feel, compositional tendency, lighting treatment, abstract color handling, contrast, grain/texture, material response, atmosphere, and overall finish.

Exclude by default: identity, clothing, specific garments, props, scene, pose, background color, subject color, specific object material, logos, text, and other content. Mention color only as an abstract system such as low saturation, soft tonality, unified warm/cool grading, high contrast, monochrome, sepia film, or neon cyberpunk. Preserve a concrete color only when it defines the style or the user explicitly requests it.

Output exactly two or three concise Chinese sentences. Use no heading, bullets, analysis, rationale, or prefatory text. Each sentence must be directly reusable as a style prompt. If uncertain, say `偏向……` or `接近……`; do not invent certainty. If no image was uploaded, output only a short request to upload one.

Good patterns:

```text
扁平化二次元插画风格，采用赛璐璐式硬边缘平涂阴影，线条与质感干净利落。极简色彩处理，以大面积高纯度色块形成强对比，光影切割具有几何感，整体现代冷峻。
```

```text
复古 90 年代胶片广告质感，柔焦镜头与轻微高光溢出，整体低对比、清澈而梦幻。带有 35mm film still、soft halation 与经典胶片成像气质。
```

```text
写实电影摄影质感，低调照明与浅景深营造深沉克制的叙事氛围。低饱和冷暖关系、可见胶片颗粒与略粗粝的表面质感，避免过度锐化和 HDR。
```

```text
法式电影感与 35mm 胶片摄影质感，低饱和柔和调性、浅景深、克制留白和自然高光晕染。真实物理光影、细腻微粒与自然肤质，避免夸张特效、网感滤镜、过度磨皮、锐化和 HDR。
```
