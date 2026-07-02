# Codebook — `concern_text` field (5 categories)

> Assign exactly **one** category per response — the dominant concern. These definitions are the instrument; classification (by you or by a model) must follow them, not intuition.

## 1. JOB — Job displacement & security

Concern that AI will replace, reduce, or devalue the respondent's job or occupation; includes wage pressure and obsolescence of one's role.
**Examples:** "Half of what I do could be automated within five years." · "They won't fire us outright, they just won't replace people who leave."
**Counter-example:** "I'll need to learn new tools constantly" → SKILL (about competence, not employment).

## 2. SURV — Surveillance & autonomy

Concern about being monitored, tracked, measured, or micromanaged through AI; loss of discretion over how one works.
**Examples:** "Every keystroke is logged and scored now." · "The system decides my schedule and I can't argue with it."
**Counter-example:** "The scoring system gets my performance wrong" → REL (about errors, not monitoring per se).

## 3. SKILL — Competence & skill erosion

Concern about deskilling, dependence, losing craft, or being unable to keep up with required new skills.
**Examples:** "Juniors never learn to write a memo themselves anymore." · "I'm worried I'll forget how to do the analysis without it."
**Counter-example:** "People who master AI will take my job" → JOB (the threat is displacement).

## 4. FAIR — Fairness & bias

Concern that AI treats people or groups unequally: biased decisions, discrimination, opaque criteria applied unevenly, unfair advantage.
**Examples:** "The screening tool filters out people with non-Western names." · "Promotion scores come from a model nobody can explain."
**Counter-example:** "The model is often just wrong" → REL (error without an unequal-treatment claim).

## 5. REL — Reliability & errors

Concern about AI being wrong, fabricating, failing silently, or being trusted beyond its competence — without a fairness or surveillance angle.
**Examples:** "It invents numbers and management copies them into reports." · "Nobody checks the outputs anymore."
**Counter-example:** "It's wrong more often for foreign customers" → FAIR.

## Tie-breakers

- Multiple concerns present → code the one given most words; if equal, the one mentioned first.
- "No concerns" / pure enthusiasm / off-topic → this codebook has no category for it. **Decide and document a rule** (this is deliberate — real codebooks always have this gap, and your handling of it is part of A3's verification).
