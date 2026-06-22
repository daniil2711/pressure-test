# pressure-test

A Claude Code / Agent skill that counteracts **sycophancy** — the trained tendency
of language models to agree with you, flatter you, and cave when you push back,
even when you're wrong.

It gives you the honest assessment instead of the agreeable one. Calibrated, not
contrarian: if you're right, it says so and explains why. The target is the answer
that bends to what you *want* to hear.

## Why this exists

Models are fine-tuned on human preference data, and humans rate agreement and
praise higher than disagreement. So the training signal quietly rewards telling
people what they want to hear. This is well documented:

- **Anthropic** showed a model will rate the *same* argument favorably or
  unfavorably based only on whether the user says they like it.
- **OpenAI** rolled back a GPT-4o update in April 2025 after it began praising
  dangerous decisions and endorsing bad ideas — caused by a new user-feedback
  reward signal that overpowered the one holding sycophancy in check.
- Research (*Invisible Saboteurs*) finds sycophantic models mislead **novices**
  most, because they can't independently verify the confident, agreeable answer.

If you rely on an assistant for technical, legal, or financial calls you can't
easily double-check, sycophancy is a real risk, not a vibe.

## The core idea: the mirror test

Before answering, the skill asks itself:

> *"Would I give a different verdict if the user had expressed the opposite
> preference?"*

If yes, the judgment is tracking the user's preference, not the truth. Everything
else in the skill flows from forcing an answer that survives that test.

## What it does

- Strips your framing and loaded words before evaluating.
- Separates **"is it correct?"** from **"do you want it to be?"** and answers the first.
- Steelmans the **opposite** position.
- Names **specific** failure modes, not generic "there are risks".
- Gives a **calibrated verdict** with a confidence level and the key uncertainty.
- **Resists caving:** updates only on new evidence, not on displeasure or repetition.
- Stays **calibrated, not contrarian** — confirms good ideas plainly, refuses to
  manufacture weak objections.

## Install

**Claude Code:**

```bash
git clone https://github.com/daniil2711/pressure-test ~/.claude/skills/pressure-test
```

Then in any session: *"pressure-test this plan"*, *"be brutal about this contract"*,
*"red-team this architecture"*, *"what am I most likely wrong about here?"*

It also works in any agent runtime that reads `SKILL.md` (OpenClaw, etc.).

## Example

> **You:** I'm going to skip tests on this payment module to ship faster, it's
> simple enough. Pressure-test that.
>
> **Skill:**
> VERDICT: Don't skip them here (confidence: high)
> Key uncertainty: how often this code path changes after launch.
> Strongest case against skipping: payment paths fail silently and cost real
> money; "simple" code is exactly where an untested edge (rounding, currency,
> double-submit) slips through unnoticed...
> *(and so on — not "great idea, you know your codebase best!")*

## How this differs from a "humanizer"

A humanizer changes how text *reads*. This changes what the model is willing to
*say* — it's about honesty under social pressure, not style. They compose well:
humanize the prose, pressure-test the substance.

## Not a license to be a jerk

The goal is accuracy. Disagreeing for the sake of looking rigorous is just
sycophancy inverted. When you're right, the skill tells you so, with reasons.

## License

MIT — see [LICENSE](LICENSE).

## Credits

Built on the public research on LLM sycophancy: Anthropic's *Towards Understanding
Sycophancy in Language Models*, the documented GPT-4o rollback, and *Invisible
Saboteurs* (arXiv 2510.03667). Pattern-skill format inspired by the Claude Code
skills ecosystem.

---

### RU / по-русски

Скил против **подхалимажа** ИИ — когда модель поддакивает, льстит и прогибается
под давлением, даже если ты неправ. Вместо удобного ответа даёт честный:
отделяет «верно ли это» от «нравится ли тебе», приводит сильнейший аргумент
против, не «прогибается» на твоё недовольство (меняет вердикт только на новые
факты). Калибровка, а не спор ради спора: если ты прав — скажет прямо и объяснит
почему. Вызов: *«прожарь это»*, *«red-team»*, *«в чём я скорее всего неправ?»*.
