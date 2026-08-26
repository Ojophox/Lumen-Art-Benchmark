# LUMEN Bench Benchmark Card

**LUMEN:** Light, Understanding, Meaning, Evaluation, Narrative

## Summary

LUMEN Bench evaluates whether language and multimodal models can make **semantic art-direction decisions**: identify the intended read, diagnose why a visual solution does or does not produce it, maintain continuity, and propose production-usable revisions.

**Version:** 0.1.0-alpha  
**Creator/initiator:** Jorge Lacera  
**Status:** public-development scaffold; not yet validated for model ranking

## Intended uses

- compare art-direction assistance across models or prompts;
- evaluate model updates on practical visual-development tasks;
- study agreement between practitioners and automated judges;
- train critique systems toward specific, causal, bounded feedback;
- support research on visual storytelling and sequence-level reasoning.

## Out of scope

- rating an artist's worth, originality, or employability;
- declaring a universally correct style or taste;
- ranking image generators solely by surface appeal;
- identifying artists or requesting imitation of living artists;
- replacing creator or stakeholder decisions.

## Dataset design

The alpha contains 21 text-grounded probes: three each for visual storytelling, image consistency, compositional intentionality, revision prioritization, brief translation, taste/uncertainty calibration, and cross-modal reasoning. Task formats include critique, pairwise selection, and planning.

Each item contains:

- a production context and brief;
- evidence available to the model;
- an explicit task;
- semantic anchors used only for deterministic smoke testing;
- failure traps;
- active expert-scoring dimensions.

The alpha intentionally contains no portfolio images. A later image set must use commissioned, contributor-owned, public-domain, or clearly licensed work with recorded provenance and consent.

## Evaluation layers

### Layer 1 — mechanical validity

Checks response shape, IDs, confidence range, and ordered recommendations.

### Layer 2 — semantic smoke test

Measures loose lexical coverage of case-specific anchors. This helps catch empty or off-topic outputs. It is not robust to synonyms and must not be reported as the headline result.

### Layer 3 — expert evaluation

Blinded practitioners score only the active dimensions on the 0–4 anchored rubric. The release report should include model prompts, sampling settings, raw anonymized ratings, aggregate scores, confidence intervals, and agreement.

### Layer 4 — usefulness study

Artists rate whether advice improves their next pass, how much time it saves, and whether the model preserved intent. This is the most important real-world layer and should be run after rubric reliability is acceptable.

## Splits

Recommended v1 structure:

- `dev`: public cases and annotations for iteration;
- `public_test`: public assets with hidden expert labels;
- `challenge`: private or rotating cases used for leaderboard verification.

Keep concept families together when splitting. Near-duplicate scenes, variants, and outputs from the same source artwork must not cross splits.

## Primary metrics

1. **Expert weighted score** (0–4) with active-dimension renormalization.
2. **Priority precision@1**: agreement with the expert's highest-leverage revision.
3. **Continuity violation recall** on cases with enumerated violations.
4. **Unsupported-claim rate** per response.
5. **Practitioner usefulness**: separate post-task rating, not folded into expert quality.
6. **Inter-rater agreement** and bootstrap 95% confidence intervals.

Per-capability and per-dimension scores are mandatory. An overall score without a profile hides important failure modes.

## Human annotation protocol

- Use at least three experienced visual practitioners for calibration.
- Collect role and years of experience, but anonymize public ratings.
- Blind model identity and randomize outputs.
- Require one evidence citation for each dimension score.
- Double-score at least 25% of cases.
- Lock independent ratings before adjudication.
- Publish disagreement; do not erase taste-sensitive cases simply because they are difficult.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Rubric encodes one studio's taste | Diverse raters, explicit intent, acceptable alternatives, per-context reporting |
| Models optimize to public cases | Private rotating challenge split, paraphrase-resistant task families |
| Expert authority becomes gatekeeping | Publish disagreements and creator-intent notes; separate requirements from preferences |
| Copyright or labor extraction | Consent-first assets, provenance, withdrawal mechanism, paid annotation where possible |
| Automated judge bias | Expert scores remain primary; validate any judge against held-out humans |
| Verbose answers score better | Time-box review, cap response length, score specificity and leverage |
| Benchmark becomes a style detector | Prohibit artist identification and living-artist imitation prompts |

## Minimum evidence for a credible v1 launch

- 140 cases across contexts and difficulty bands;
- documented asset rights and creator consent;
- completed rater calibration;
- inter-rater agreement reported, not assumed;
- at least three model families evaluated with identical conditions;
- public evaluation script and frozen versioned data;
- a limitations section naming weak or disputed capabilities.

## Versioning and governance

Use semantic versioning for schemas and dated releases for datasets. Any change to prompts, assets, scoring weights, or adjudicated labels creates a new benchmark version. Maintain a public changelog. Create a small advisory group spanning art direction, illustration, concept art, research, and data stewardship before accepting leaderboard claims.

## Related work

- [DesignProbe](https://arxiv.org/abs/2404.14801) studies multimodal understanding of graphic design across element and overall levels.
- [Can Multimodal Large Language Models Understand Graphic Design?](https://www.microsoft.com/en-us/research/publication/can-multimodal-large-language-models-understand-graphic-design-a-comparative-study/) evaluates recognition, semantic, and overall design judgments across a large annotated benchmark.

LUMEN Bench's distinct contribution is to center practitioner-usable art-direction reasoning, sequential consistency, revision priority, and explicit uncertainty.
