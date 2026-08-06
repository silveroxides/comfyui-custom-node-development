# Custom Node Development Rules

## Contract and source hierarchy

- Establish the intended public behavior before selecting an implementation. Use, in order: the user's current instructions and corrections; repository-local contracts and relevant preserved history; the installed ComfyUI implementation and model-native protocol; then existing repository conventions.
- Inspect the configured ComfyUI checkout before relying on remembered Core APIs, node schemas, model behavior, or frontend conventions. Trace the actual tokenizer arguments, conditioning metadata, tensor representations, model inputs, and output contract involved.
- If a plan, handoff, test, existing helper, or current implementation conflicts with a higher-authority source, stop and state the contradiction before editing. Do not silently reconcile it toward the smallest or easiest patch.
- Use `comfy_api.latest`, Core node types, `folder_paths`, and existing ComfyUI helpers only when their semantics match the required contract. Similar names, tensor shapes, or outputs do not establish equivalence.
- Use dependencies already provided by the configured ComfyUI installation when practical. Add dependencies only when required by the feature.
- Match the repository's existing organization. Extract substantial reusable logic into focused helper modules when that avoids bloating node registration files.

## Before editing

- State the intended end-to-end data flow in task-relevant terms: public controls and ordering, input grouping/batching, preprocessing, tokenizer or model presentation, conditioning metadata, tensor consumers, and outputs.
- Identify model-specific or node-specific protocol boundaries. Do not reuse generic prompt placeholders, aliases, fusion paths, reference payloads, masks, or metadata across those boundaries without verifying wire-level and semantic equivalence.
- Audit every affected representation and consumer when a shared helper or public schema is involved. A repeated failure across nodes requires a shared-contract audit, not a local symptom patch.
- Keep visible controls, schema input order, execution argument mapping, tooltips, serialized widget values, and backend behavior consistent. Check the installed frontend/Core implementation when autogrow naming or widget serialization is relevant.

## Compatibility

- Preserve node IDs, backend socket IDs, custom socket types, output order, serialized widgets, and workflow compatibility unless the request explicitly changes them.
- Use `display_name` for frontend labels without renaming backend identifiers.
- Do not invent hidden fallbacks, optionality, defaults, aliases, or compatibility behavior. Expose user-significant choices explicitly and preserve old behavior only when it does not contradict the requested contract.
- Use `io.Autogrow` only after checking its generated socket IDs, visible numbering, batch behavior, execution mapping, and workflow compatibility against the node's documented indexing contract.
- Keep warnings and errors short, actionable, and specific to invalid user state.

## Models, tensors, and execution

- Use ComfyUI model loading, patching, device, dtype, offload, and Dynamic VRAM management paths. Do not add competing model lifecycle management.
- Preserve model-native tokenizer and conditioning protocols. Arguments such as `images`, model-specific reference items, keyframes, reference metadata, and modality tags are not interchangeable merely because they carry the same pixels.
- Avoid unnecessary device transfers, CPU readbacks, dtype conversions, synchronization, persistent tensor caches, and blocking I/O in execution paths.
- Keep allocations on the intended device and dtype. Preserve native tensor layouts unless a documented interface requires conversion.
- Do not patch model internals at runtime from node code. Use the model patcher or the established extension interface.
- Do not run model inference unless the user explicitly requests it.

## Frontend behavior

- Inspect the installed frontend and the repository's existing web code before changing LiteGraph or Vue behavior.
- Keep frontend-managed widgets, queue behavior, serialized data versions, and legacy workflow parsing compatible.
- Keep interaction geometry local and test pure geometry or queue selection with Node when possible.
- Avoid UI controls that duplicate configuration sockets or unnecessarily expand node dimensions.

## Change discipline

- Make the smallest change that satisfies the audited end-to-end contract. Do not localize a repeated or shared-contract defect merely to minimize the diff.
- Preserve unrelated dirty and untracked files.
- Diagnose before implementing when the user requests diagnosis only.
- Remove obsolete branches when current Core behavior makes them incorrect and compatibility does not require them.
- Do not treat passing tests, compilation, or clean diffs as evidence of semantic correctness until the tests are shown to encode the intended external behavior independently of the implementation.
