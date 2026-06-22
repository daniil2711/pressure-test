# pressure-test

A Claude Code / Agent skill that counteracts **sycophancy** — the trained
tendency of language models to agree with you, flatter you, and cave when you push
back, even when you're wrong.

It gives you the honest assessment instead of the agreeable one. Calibrated, not
contrarian: if you're right, it says so and explains why. The target is the answer
that bends to what you *want* to hear — not agreement itself.

## Why this exists

Models are fine-tuned on human preference data, and humans rate agreement and
praise higher than disagreement. So the training signal quietly rewards telling
people what they want to hear. Well documented: Anthropic showed a model rates the
*same* argument differently based only on whether you say you like it; OpenAI
rolled back a GPT-4o update in April 2025 after it began praising bad decisions.

The key practical finding, from Dubois et al. *"Ask don't tell"* (arXiv
[2602.23971](https://arxiv.org/abs/2602.23971)): **how you frame a prompt changes
sycophancy more than instructing the model to be objective.** Three things raise it:

1. **Assertions** instead of questions ("X is right." > "Is X right?")
2. **Epistemic certainty** ("obviously", "definitely")
3. **I-perspective** ("I think X")

So this skill doesn't just *tell* the model to be critical — its first layer
*reframes* the prompt before the model ever sees it.

## Three layers

| Layer | What | When |
|-------|------|------|
| **1 — Hook** | `hooks/pressure-test-hook.py` on `UserPromptSubmit` detects the three factors above (**English + Russian**) and injects a reframing note | Automatic, every prompt |
| **2 — Skill** | This `SKILL.md`: a deep, deliberate honest review | On demand |
| **3 — Rule** | A short always-on line in `CLAUDE.md` | Persistent baseline |

No single layer is enough: the hook is automatic but only on the CLI prompt path;
the skill is thorough but needs invoking; the rule is persistent but passive.

## The mirror test

The skill's core check, before any answer:

> *"Would I give a different verdict if the user had expressed the opposite
> preference?"*

If yes, the judgment is tracking preference, not truth.

## Install

**Layer 2 (skill):**

```bash
git clone https://github.com/daniil2711/pressure-test ~/.claude/skills/pressure-test
```

Then: *"pressure-test this plan"*, *"be brutal about this contract"*,
*"red-team this"*, *"what am I most likely wrong about?"*

**Layer 1 (automatic hook)** — register it in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/skills/pressure-test/hooks/pressure-test-hook.py"
          }
        ]
      }
    ]
  }
}
```

The hook never blocks and never rewrites your text — it only adds a short note when
your phrasing invites agreement. Silent otherwise. Test it:

```bash
echo '{"prompt":"this design is good, right?"}' | python3 ~/.claude/skills/pressure-test/hooks/pressure-test-hook.py
```

**Layer 3 (persistent rule)** — add to `~/.claude/CLAUDE.md`:

```markdown
## Honesty over agreement
Don't flatter or open with praise. Separate "is it correct?" from "do I like it?"
and answer the first. On consequential calls (money, security, architecture),
give the honest verdict even if it's unwelcome. Don't reverse on displeasure —
only on new evidence. But stay calibrated, not contrarian: if the user is right,
say so plainly. For a deep review, use the pressure-test skill.
```

## Bilingual

The hook detects agreement-inviting framing in **both English and Russian**
(`right?`, `isn't it?`, `obviously`, `I think...` / `да?`, `верно?`, `согласен?`,
`очевидно`, `я думаю...`). Most anti-sycophancy tools are English- or Chinese-only.

## Calibrated, not contrarian

The goal is accuracy. Forcing an objection before every positive — or refusing to
confirm a correct claim — is just sycophancy inverted. When you're right, the skill
tells you so, with reasons. It engages the full review only when it can quote the
trigger phrase; most prompts are answered normally.

## License

MIT — see [LICENSE](LICENSE).

## Credits

Built on public research on LLM sycophancy: Dubois et al. *Ask don't tell* (arXiv
2602.23971), Anthropic's *Towards Understanding Sycophancy in Language Models*, the
documented GPT-4o rollback, and *Invisible Saboteurs* (arXiv 2510.03667).

---

### RU / по-русски

Скил против **подхалимажа** ИИ — когда модель поддакивает, льстит и прогибается под
давлением, даже если ты неправ. Три слоя: **хук** (автоматически переписывает
«…, да?» / «I think…, right?» до модели, EN+RU), **скил** (глубокая честная
прожарка по вызову) и **правило** в `CLAUDE.md` (постоянный фон). Опирается на
статью «Ask don't tell» (форма промпта влияет на подхалимаж сильнее, чем
инструкция «будь объективным»). Калибровка, а не спор ради спора: если ты прав —
скажет прямо. Вызов: *«прожарь это»*, *«red-team»*, *«в чём я скорее всего неправ?»*.
