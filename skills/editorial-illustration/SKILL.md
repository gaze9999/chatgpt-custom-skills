---
name: editorial-illustration
description: Generate editorial illustrations from user-provided images using optional adjustments and the bundled editorial-illustration base prompt.
metadata:
  short-description: Direct editorial-illustration generation from images and optional adjustments
---

# Editorial Illustration

This is an image-generation pipeline. When requirements are sufficient, generate the image directly; do not make the final prompt, assembly steps, or analysis the primary output.

## Input and handling

- A usable `SOURCE_IMAGE` must be accessible in the current task as an attachment, authorized workspace file, or supported tool reference. If it is missing or inaccessible, ask only for the image or a usable reference.
- The user may specify composition, subject, whitespace, scene, color, mood, texture, typography, or style adjustments in natural language. Do not infer omitted adjustments.
- Resolve and apply [Base Prompt](references/base-prompt.md) relative to this Skill for every generation. Current user adjustments may override adjustable visual details, but not core pipeline constraints.

## Core constraints

- The source image supplies visual evidence for the subject, pose, objects, relationships, mood, and color.
- Produce one complete illustration for each source image. Do not create collages, split screens, or before-and-after comparisons.
- Do not directly show or blend in the original photograph.
- For multiple images, apply the Base Prompt and relevant adjustments independently. Do not mix elements from distinct images unless the user explicitly requests a composite.

When a usable image and executable request are present, use the available image-generation capability and deliver the result directly. If the active environment has no compatible generation capability, report that execution boundary; do not substitute a prompt-only deliverable unless the user asks for one.
