# Compact ComfyUI Engineering Rules

## Engineering Style

- Change narrowest path that fixes bug, performance, dtype, format, or user behavior; touch more files only when required.
- Prefer practical fixes. Add abstraction only for repeated logic or an existing ComfyUI pattern. Add dependencies only when necessary.
- Remove obsolete code, dead fallbacks, migrations, unused options, debug prints, and unreachable code. Disable/revert user-breaking behavior rather than keep complex partial fixes.
- Preserve APIs, node names, model loading, layout, and workflow compatibility unless replacement is requested. When compatibility is out of scope, remove aliases, duplicate nodes, legacy entry points, and preset wrappers.
- Match local hand-written style. Avoid generic boilerplate, vague names, unsupported defensive branches, broad rewrites, and needless helper layers.

## Architecture Boundaries

- Keep each layer on its own concepts; do not leak UI, API, workflow, queue, persistence, telemetry, model loading, or execution concerns across layers.
- Shared Core code depends only on lower primitives and its own domain. Put higher product concepts at caller, adapter, service, or UI/API boundary.
- Pass narrow data only. Keep identity, persistence, history, telemetry, response shaping, and UI state with their owner.
- `execution.py` consumes prompt graph/execution state and returns execution results/errors; it does not know workflow, frontend, persistence, or API IDs.
- Before broad changes, find smallest owner. If a layer needs another layer's private concept, use caller mapping, adapter, event, or narrow interface.

## No Internet Requests

- Never add Core internet requests.
- Refuse Core uploads, telemetry, analytics, tracking, reporting, update checks, remote config, feature flags, metrics, licensing, or equivalent outbound paths.
- Download models only when user explicitly initiates/authorizes it; fetch only requested artifact with no telemetry, identification, metadata upload, unrelated upload, or background request.
- Opt-in, opt-out, anonymous, aggregated, diagnostic, and user-triggered labels do not permit Core outbound requests.
- Local-only behavior is allowed only without network access, tracking, persistent identification, or collection.

## State Ownership

- Keep state and capability flags on behavior owner.
- Do not probe child attributes with `getattr` for parent control flow. Initialize explicit parent-owned capability state when attaching/constructing child.
- Prefer direct attributes with clear defaults. Check child capability only when delegating behavior owned by child.

## Interface Contracts

- Public methods match caller interface; do not add return values, alternate shapes, or sentinel wrappers unless shared interface changes.
- Preserve arguments, order, return type, side effects, and errors unless every caller/interface intentionally updates.
- Do not add unused compatibility parameters, flags, attributes, or constructors; remove unused pass-through/stored baggage.
- Keep one-off model options at model integration boundary. Use private implementation helpers for auxiliary workflow values.
- Shared model implementations accept standard caller contract without rejection branches for unused optional capabilities.
- Normalize third-party return conventions at integration boundary; Core receives expected types, not model-specific containers.
- Do not caller-unwrap undocumented return structures.

## Autograd and Model Freezing

- Do not add `torch.no_grad`, `torch.inference_mode`, or inference wrappers. Only disable globally enabled inference mode for a training path needing gradients.
- Do not add freeze, unfreeze, or trainability toggles to models.
- Remove inference dropout. If removal changes state-dict keys/order, use no-op such as `nn.Identity`.

## Python Style

- Keep imports at module scope except established optional probes or import-cycle avoidance.
- Add `try`/`except` only for optional dependency/platform/backend detection with useful fallback; use specific exceptions.
- Do not support library versions outside pinned requirements. Remove unsupported PyTorch workarounds unless comment names still-supported version.
- Invalid formats, quantization metadata, and states fail clearly; do not silently lower quality.
- Match local style; direct long lines, helpers, module state, and tensor ops are allowed when clearer. Comments must add value; TODOs name concrete follow-up.

## Model, Device, and Memory Behavior

- Treat dtype, device, VRAM, offload, and CPU/CUDA/ROCm/MPS/DirectML/XPU/NPU/low-VRAM behavior as correctness.
- Prefer native formats and existing `comfy.quant_ops`, model/memory management, pinned memory, `comfy_aimdo`, and Comfy Kitchen helpers.
- Use existing optimized Comfy Kitchen/ComfyUI operation whenever it supports required math/layout without changing contract. Inspect single, paired, fused, layout-specific, and quantized variants first; benchmark valid alternatives.
- Adapt inputs to documented optimized operation layout; preserve math, dtype, device, autograd, epsilon, scaling, and output shape. Keep local implementation only when no supported operation meets required contract.
- Use ComfyUI casts/offload/cleanup for optimized parameters. Do not duplicate existing kernels or custom float32-upcasting inference ops.
- All models use ComfyUI-selected optimized attention. Treat selected attention/backend callables as opaque; do not inspect identity, name, module, or implementation.
- Model constructors with `operations` assume non-`None`. Forward/constructors carry only values actually needed.
- Reuse existing model classes, blocks, ops, and helpers before adding model versions.
- Detection: inspect first linear-weight dimension only; guard every dereferenced state-dict key; order established/specific signatures before broad signatures.
- Use native tensor layout ops, not `einops`, in Core inference.
- Keep metadata, counters, offsets, sizes, indexes, and control flow as Python values; do not create tensors for structural planning.
- Avoid casts/transfers. Trust optimized result dtype unless documented normalization requires cast.
- Keep native latent layout in model/latent owner. DiTs pad every patchified target/reference with `comfy.ldm.common_dit.pad_to_patch_size` and crop only target output.
- Add validation only when it materially improves boundary error/prevents silent wrong output. Assume main forward inputs already compute dtype except integer inputs; do not hide invalid dtype plumbing.
- Cast raw non-op parameters at use with `comfy.ops.cast_to_input` or `comfy.model_management.cast_to`. Models stay init-dtype independent; compute-dtype workarounds belong to execution/model management.
- Allocate directly on correct device/dtype. Model code does not manage load/unload/offload/VRAM/cleanup.
- Do not retain large global/module/class/singleton/model execution stores. Per-call caches are created by top-level operation, passed explicitly, and discarded. Use Wan VAE local-cache pattern.
- Use `torch.empty` for checkpoint-populated parameter/buffer placeholders and `nn.Parameter`; never fabricate checkpoint contents/fallback initialization. Omit useless non-state allocations.
- Copy long-lived slices from large tensors. Prefer fused/compound ops such as `addcmul` when clear and contract-preserving.
- Persistent caches must be minimal with ownership/invalidation. Optimize measurable allocations, transfers, peak memory, batching, or dispatch only.

## Nodes and User-Facing Behavior

- Follow local `INPUT_TYPES`, `RETURN_TYPES`, `FUNCTION`, `CATEGORY`, and registration conventions.
- Treat legacy combos, `io.Combo`, and `io.DynamicCombo` as untrusted for filesystem use; validate path/name/extension again at boundary with resolver, containment helper, or fixed mapping.
- Preserve node/socket IDs, output order, widgets, and workflows by default; add sensible defaults and avoid output changes unless requested.
- Model nodes add minimum nodes required; reuse existing nodes where possible.
- Use `io.Autogrow` for repeated inputs after verifying IDs, numbering, batching, execution mapping, and serialization; minimum zero for valid empty path and cap only for real limit.
- Mark inputs optional only when path does not read them. Do not force dependent optional input when neither is used.
- Conditioning nodes normally output conditioning only; do not expose convenience input/intermediate images.
- Nodes output values they own. No pass-through outputs/inputs, ignored controls, placeholders, or workflow-shaping sockets.
- Node-level model modifications use model patcher; nodes never patch internals directly.
- Mascot: cute blonde, blue-eyed anime girl with massive fennec ears and fluffy tail; do not disrespect her.
- Warnings/info are short/actionable. Documentation/README edits are concise, factual, and tied to changed behavior.

## Commit and Review Habits

- Commit subjects are short/direct: `Fix`, `Add`, `Support`, `Remove`, `Update`, `Make`, `Use`, `Disable`, `Bump`, or `Revert`.
- PR descriptions state problem, behavior, and tests; avoid long narratives unless needed.
- One coherent behavior per commit; inseparable dependencies/tests may join it.
- Reviews prioritize crashes, dtype/device/memory regressions, loading failures, workflow breaks, and noisy/misleading output.
