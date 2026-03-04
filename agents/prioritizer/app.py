import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("prioritizer")

INPUT_FILE = "/data/summary.txt"
OUTPUT_FILE = "/data/prioritized.txt"

PRIORITY_KEYWORD = [
    "urgent", "today", "asap", "important",
    "deadline", "critical", "action required"
]

def score_line(line: str):
    """Count how many priority keywords appear in a line."""
    lower = line.lower()
    return sum(1 for kw in PRIORITY_KEYWORD if kw in lower)

def prioritize():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [cleared for line in f if (cleared := line.strip())]

    scored = [(line, score_line(line)) for line in lines]
    scored.sort(key=lambda x: x[1], reverse=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for line, score in scored:
            out.write(f"[{score}] {line} \n")

    logger.info(f"Prioritized {len(scored)} items -> {OUTPUT_FILE}")

if __name__ == "main":
    prioritize()