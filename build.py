"""Build the single-file KB AI Agent quiz."""
import json
from pathlib import Path

import bank
import bank2
import bank3
import bank4
import bank5
import bank6
import bank7

ROOT = Path(__file__).resolve().parent
SRC = Path(r"c:\Users\ctd32\OneDrive\Documents\sap-quiz\index.html")
OUT = ROOT / "index.html"

CHAPTERS = [
    (1, 42, "챕터 1 LLM·AI 개론"),
    (43, 85, "챕터 2 프롬프트"),
    (86, 128, "챕터 3 RAG"),
    (129, 171, "챕터 4 Tool Use"),
    (172, 214, "챕터 5 Agent 아키텍처"),
    (215, 257, "챕터 6 프레임워크"),
    (258, 300, "챕터 7 운영·거버넌스"),
]


def chapter_of(n: int) -> str:
    for a, b, name in CHAPTERS:
        if a <= n <= b:
            return name
    raise ValueError(n)


def main():
    items = bank.Q
    if len(items) != 300:
        raise SystemExit(f"expected 300 questions, got {len(items)}")
    stems = [t for t, *_ in items]
    if len(set(stems)) != 300:
        raise SystemExit("duplicate question stems")
    letters = "ABCD"
    questions = []
    for i, (text, choices, ans, expl) in enumerate(items, 1):
        if ans not in letters or len(choices) != 4 or len(set(choices)) != 4:
            raise SystemExit(f"bad item {i}")
        # Spread the correct choice across A-D. Source order stays readable.
        rot = (i - 1) % 4
        choices = choices[rot:] + choices[:rot]
        ans = letters[(letters.index(ans) - rot) % 4]
        questions.append(
            {
                "id": i,
                "text": text,
                "choices": choices,
                "answer": ans,
                "multi": False,
                "explanation": f"{chapter_of(i)}. {expl}",
            }
        )
    src = SRC.read_text(encoding="utf-8")
    start = src.find("var ALL_QUESTIONS = [")
    end = src.find("\n];\n", start)
    if start < 0 or end < 0:
        raise SystemExit("template markers not found")
    head, tail = src[:start], src[end + len("\n];\n") :]
    head = head.replace("<title>SAP-C02 모의고사</title>", "<title>KB AI Agent 모의고사</title>")
    head = head.replace('<span class="logo-badge">AWS</span>', '<span class="logo-badge">KB</span>')
    head = head.replace(
        '<span class="logo-text">SAP-C02 모의고사</span>',
        '<span class="logo-text">KB AI Agent 모의고사</span>',
    )
    head = head.replace(
        '<div class="start-title">AWS Solutions Architect Professional 모의고사</div>',
        '<div class="start-title">AI Agent 개발 모의고사</div>',
    )
    head = head.replace(
        '<div class="start-sub">SAP-C02-KR · 938문제 기출 덤프 · 랜덤 출제 · 즉시 해설</div>',
        '<div class="start-sub">2026 KB디지털역량진단 · 4지선다 300문제 · 랜덤 출제 · 즉시 해설</div>',
    )
    head = head.replace(">Pro<", ">7장<")
    head = head.replace("938", "300")
    lines = ["var ALL_QUESTIONS = ["]
    for item in questions:
        lines.append("  " + json.dumps(item, ensure_ascii=False) + ",")
    lines.append("];")
    OUT.write_text(head + "\n".join(lines) + "\n" + tail, encoding="utf-8")
    print(f"wrote {OUT} ({len(questions)} questions)")


if __name__ == "__main__":
    main()
