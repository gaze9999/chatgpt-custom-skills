# AGENTS.md instruction layering

Use this reference when reorganizing agent instructions for a repository or moving the same governance pattern to another computer or project.

## Resolve the active hierarchy

- Verify the target agent's current official discovery, precedence, filename, size, and configuration behavior before editing. Do not assume every tool implements `AGENTS.md` or nested files identically.
- For Codex, check the global layer and every applicable file from the repository root to the working directory. Later, nearer files override broader earlier guidance; keep the combined size limit in mind.
- Inventory root and nested instruction files, tool-specific configuration, role definitions, task guides, live references, and ignored files. Inspect ignored governance files directly because a normal Git diff may omit them.

## Place rules at the narrowest durable scope

- Keep global instructions limited to stable cross-project preferences, authorization boundaries, safety, evidence honesty, and execution principles.
- Keep the repository root tool- and model-neutral. It should contain only rules that apply across the repository, such as cross-module architecture, public boundaries, shared safety, generic ownership, and common verification.
- Put framework, runtime, package-manager, directory layout, build/serve commands, local conventions, public interfaces, and focused checks in the nearest nested instruction file whose subtree they govern.
- Keep tool-specific role names, model/reasoning defaults, invocation parameters, and orchestration mechanics in that tool's configuration or conditional guide. Do not require every `AGENTS.md` consumer to read Codex-only behavior.
- Put transaction-, feature-, or workflow-specific procedures in a task guide or Skill with an explicit loading trigger. Keep current progress, temporary exceptions, blockers, and stop conditions in the current task.

## Restructure safely

1. Classify every existing rule by scope and identify exact duplicates, broader summaries, and unique contracts.
2. Create the narrower destination before removing a unique rule from the broader file.
3. Preserve cross-boundary contracts in the closest common ancestor. A nested file may refine local implementation but must not silently weaken repository-wide authorization, safety, or public-interface rules.
4. Replace tool-specific syntax in root guidance with portable intent only when the behavior remains enforceable; keep exact tool settings in maintained configuration.
5. Update live references and role files that point to moved sections. Avoid parallel copies that can drift.
6. Keep the final hierarchy concise enough that an agent working in one subtree receives only relevant local context.

## Verify the migration

- From the repository root and each affected subtree, enumerate the effective instruction chain in load order and check for contradictions or gaps.
- Search for moved headings, role names, model names, invocation parameters, runtime versions, and stale links. Confirm each surviving occurrence belongs at that layer.
- Validate syntax and metadata, compare synchronized copies byte-for-byte when requested, and inspect Git status. Report ignored or untracked governance files explicitly.
- Do not claim that shorter instructions reduce tokens, cost, latency, or errors without measurement. Confirm file content immediately; treat runtime reload by an already-open client as unverified unless observed.

## Portable outcome

A reusable governance setup should leave project facts in the project and only the restructuring method in the portable Skill. On another computer, rediscover the repository and tool configuration, then apply this method instead of copying framework versions, paths, role names, models, or commands from the previous project.
