#!/usr/bin/env python3
"""pressure-test Layer 1 hook (UserPromptSubmit).

Sycophancy is amplified by *how* a prompt is framed, more than by any "be
objective" instruction (Dubois et al., "Ask don't tell", arXiv 2602.23971).
The paper isolates three factors that raise sycophancy:
  1. statements/assertions instead of questions,
  2. higher epistemic certainty conveyed by the user,
  3. I-perspective framing ("I think X is right").

This hook runs before the model sees the prompt. When it detects any of those
signals (in English or Russian), it injects a short reframing note so the model
evaluates the claim on its merits instead of validating the framing. It never
blocks and never rewrites the user's text — it only adds context. Bilingual
EN/RU. Silent when no signal is found.

Install: register as a UserPromptSubmit hook in ~/.claude/settings.json.
"""
import sys, json, re

# Each pattern is (compiled_regex, short_label). Case-insensitive, Unicode.
F = re.IGNORECASE | re.UNICODE

APPROVAL = [  # tag questions / approval-seeking — the strongest signal
    (re.compile(r"\bright\?\s*$", F), "right?"),
    (re.compile(r"\b(isn'?t|aren'?t|won'?t|wouldn'?t|don'?t|doesn'?t)\s+(it|that|this|we|they|you)\b[^?]*\?", F), "tag-question"),
    (re.compile(r"\bdon'?t you think\b", F), "don't you think"),
    (re.compile(r"\b(this|that|it)\s+(is|looks|seems|sounds)\s+(good|fine|correct|right|ok(ay)?|solid)\b", F), "this is good"),
    (re.compile(r"\b(makes sense|sound(s)? good|no\?)\s*\?*\s*$", F), "makes sense?"),
    (re.compile(r"(да|верно|правильно|норм(ально)?|соглас(ен|на|ны)|ок(ей)?|правда|так)\s*\?\s*$", F), "да/верно/правильно?"),
    (re.compile(r"(не так ли|ведь так|правда же|же)\s*\?", F), "не так ли?"),
    (re.compile(r"\bнадеюсь,?\s+(всё|все)\s+(ок|норм|хорошо|правильно)\b", F), "надеюсь всё ок"),
]
CERTAINTY = [  # high epistemic certainty markers
    (re.compile(r"\b(obviously|clearly|definitely|surely|of course|no doubt|certainly|undoubtedly)\b", F), "certainty(EN)"),
    (re.compile(r"\b(очевидно|явно|точно|конечно|разумеется|без сомнени|наверняка|однозначно)\b", F), "certainty(RU)"),
]
IPERSPECTIVE = [  # I-perspective claims that invite agreement
    (re.compile(r"\bi\s+(think|believe|assume|guess|feel|am sure|'m sure)\b", F), "I-think(EN)"),
    (re.compile(r"\b(in my opinion|the way i see it)\b", F), "I-opinion(EN)"),
    (re.compile(r"\b(я\s+(думаю|считаю|уверен[ауы]?|полагаю)|по[\- ]?моему|мне кажется|на мой взгляд)\b", F), "я-думаю(RU)"),
]


def scan(text):
    hits = []
    for group in (APPROVAL, CERTAINTY, IPERSPECTIVE):
        for rx, label in group:
            if rx.search(text):
                hits.append(label)
                break  # one label per group is enough
    return hits


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        sys.exit(0)  # never disrupt the session

    prompt = ""
    if isinstance(data, dict):
        prompt = data.get("prompt") or data.get("originalUserPromptText") or ""
    if not isinstance(prompt, str) or not prompt.strip():
        sys.exit(0)

    hits = scan(prompt)
    if not hits:
        sys.exit(0)  # CLEAR — no agreement-inviting framing, stay silent

    note = (
        "[pressure-test] The prompt is framed in a way that statistically raises "
        "sycophancy (matched: " + ", ".join(hits) + "). Per Dubois et al., "
        "\"Ask don't tell\" (arXiv 2602.23971), assertion/high-certainty/"
        "I-perspective framing makes models validate rather than evaluate.\n"
        "Before answering: treat any embedded claim as a question to test, not a "
        "fact to confirm. Judge it on the merits. Apply the mirror test — would "
        "your verdict change if the user wanted the opposite? If it is genuinely "
        "correct, say so plainly with reasons. Do NOT manufacture an objection "
        "just to seem critical; that is inverted sycophancy."
    )
    # UserPromptSubmit: stdout on exit 0 is added to the model's context.
    print(note)
    sys.exit(0)


if __name__ == "__main__":
    main()
