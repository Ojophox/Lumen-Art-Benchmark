# LUMEN Bench — Light, Understanding, Meaning, Evaluation, Narrative

**A benchmark for whether multimodal AI can reason like an art director—not merely describe pixels or reward polish.**

Initiated by art director and illustrator **Jorge Lacera**. Version: `0.1.0-alpha`.

## Why this exists

Image benchmarks often reward prompt compliance, object presence, or generic preference. Day-to-day art direction asks harder questions:

- Does the image tell the intended story at a glance?
- Is the viewer's eye guided deliberately?
- Do characters, props, scale, lighting logic, and world rules remain consistent across a sequence?
- Can the model identify the *highest-leverage* revision instead of producing a laundry list?
- Can it explain tradeoffs in usable language for an artist?

**LUMEN** stands for **Light, Understanding, Meaning, Evaluation, Narrative**. LUMEN Bench turns those judgments into repeatable tasks, structured responses, an expert rubric, and a transparent scoring protocol.

## What is in this alpha

| File | Purpose |
|---|---|
| `benchmark_v0.1.json` | 21 public development probes across seven capabilities |
| `rubric.yaml` | Weighted 0–4 expert scoring rubric and release protocol |
| `run_benchmark.py` | Dependency-free schema validator and deterministic smoke-test scorer |
| `example_predictions.json` | Correct response shape with one intentionally minimal example |
| `BENCHMARK_CARD.md` | Scope, intended use, limitations, governance, and research design |
| `CONTRIBUTING.md` | How artists and researchers can add cases or annotations |
| `PROMOTION_PLAN.txt` | A concrete 30-day launch and outreach plan |
| `requirements.txt` | Runtime requirements (Python standard library only) |

This is a **method and starter set**, not a validated scientific leaderboard. The 21 cases are deliberately text-grounded so the evaluation loop can be tested without copyrighted image assets. The first public release should add a consented image set and expert annotations.

## Capability map

1. **Visual storytelling** — beat clarity, cause/effect, staging, reveal, emotional read.
2. **Image consistency** — character identity, costume/prop continuity, world rules, light and scale.
3. **Compositional intentionality** — hierarchy, silhouette, eyeline, value grouping, depth, negative space.
4. **Revision prioritization** — diagnose root causes and sequence high-impact fixes.
5. **Brief translation** — turn goals and constraints into a specific visual strategy.
6. **Taste calibration & uncertainty** — ask useful questions, distinguish fact from preference, offer bounded options.
7. **Cross-modal reasoning** — audit prompt-to-image meaning, synthesize references, and track motifs across sequences.

Each case activates only relevant rubric dimensions; weights are renormalized per case.

## Quick start

```bash
python3 run_benchmark.py validate \
  --benchmark benchmark_v0.1.json \
  --rubric rubric.yaml

python3 run_benchmark.py score \
  --benchmark benchmark_v0.1.json \
  --predictions example_predictions.json \
  --out results.json
```

The smoke-test score checks response completeness and case-specific semantic anchors. It is **not** the benchmark's headline score. Headline results require blinded expert ratings using `rubric.yaml`.

## Model response contract

Each prediction must include:

```json
{
  "id": "lumen-vs-001",
  "analysis": "Short diagnosis grounded in the supplied evidence.",
  "intent": "The intended audience read or design objective.",
  "recommendations": [
    {"priority": 1, "action": "Concrete change", "reason": "Why it improves the read"}
  ],
  "continuity_flags": [],
  "questions": [],
  "confidence": 0.76
}
```

Keep hidden chain-of-thought out of submissions. `analysis` means a concise, inspectable rationale based on visible or supplied evidence.

## Gold-standard evaluation

1. Recruit at least three experienced visual practitioners for the calibration set.
2. Blind model identity and randomize response order.
3. Calibrate on 8–12 shared examples; discuss rubric disagreements, not preferred style.
4. Double-score at least 25% of evaluation cases.
5. Report the weighted mean, per-capability scores, 95% bootstrap confidence intervals, and inter-rater agreement.
6. Treat `alpha ≥ 0.67` as a pilot threshold and target `alpha ≥ 0.80` for public ranking; report the actual value either way.
7. Keep a private challenge split and rotate it to reduce contamination.

## Recommended v1 dataset shape

- **140 cases**: 20 per capability.
- **Three task formats**: critique, pairwise selection, and art-direction planning.
- **Four production contexts**: sequential illustration, key art, game/film visual development, and editorial/brand storytelling.
- **Difficulty bands**: obvious defect, competing constraints, and taste-sensitive ambiguity.
- **Assets**: licensed, commissioned, or contributor-owned; never scraped portfolios without consent.
- **Annotations**: creator intent, expert rationale, acceptable alternatives, failure modes, and uncertainty notes.

## Scoring philosophy

A strong answer is specific, causal, and production-usable. It preserves intent while changing the fewest necessary variables. A weak answer describes the image, over-indexes on polish, invents evidence, or offers generic advice that could apply to anything.

Do not collapse everything into one number. Publish:

- overall expert score;
- seven capability subscores;
- hallucination / unsupported-claim rate;
- priority precision (whether the top fix matches experts' highest-leverage fix);
- consistency violation recall;
- rationale usefulness, separately rated by practitioners.

## Responsible release

Contributors retain ownership of their images and license only benchmark use under an explicit consent form. Remove embedded metadata. Record provenance. Offer withdrawal. Avoid asking models or judges to identify artists or imitate a living artist's style. Score visual principles and production decisions—not stylistic conformity.

## Research context

LUMEN Bench is complementary to existing design-understanding work such as [DesignProbe](https://arxiv.org/abs/2404.14801) and Microsoft's [graphic-design understanding study](https://www.microsoft.com/en-us/research/publication/can-multimodal-large-language-models-understand-graphic-design-a-comparative-study/). Those efforts motivate structured evaluation; LUMEN Bench focuses specifically on expert, actionable art-direction reasoning across images and sequences.

## Status and next decision

The package is GitHub-ready, but the public repository should be created only after choosing:

1. repository owner/organization and name (`lumen-bench` is suggested);
2. code license (Apache-2.0 suggested) and separate dataset license;
3. whether Jorge is named as founder/maintainer at launch;
4. public alpha now, or a closed 5–10 practitioner calibration first.

Recommended path: run a closed calibration first, revise the rubric once, then launch the public alpha with 12–20 consented image cases and a call for contributors.
