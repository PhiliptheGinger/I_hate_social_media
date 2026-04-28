#!/usr/bin/env python3
"""Extract likely comedy event mentions from social post text.

This is intentionally API-agnostic so we can validate extraction behavior first.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

COMEDY_KEYWORDS = {
    "comedy",
    "standup",
    "stand-up",
    "open mic",
    "improv",
    "laugh",
    "showcase",
}

VENUE_PATTERNS = [
    r"\bat\s+([A-Z][A-Za-z0-9'&\-. ]{2,})",
    r"\bvenue\s*:\s*([A-Z][A-Za-z0-9'&\-. ]{2,})",
    r"\blocation\s*:\s*([A-Z][A-Za-z0-9'&\-. ]{2,})",
]

DATE_PATTERN = re.compile(
    r"\b(?:"
    r"mon(?:day)?|tue(?:sday)?|wed(?:nesday)?|thu(?:rsday)?|"
    r"fri(?:day)?|sat(?:urday)?|sun(?:day)?|"
    r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
    r"jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?|"
    r"tonight|tomorrow|this\s+week(?:end)?"
    r")\b",
    flags=re.IGNORECASE,
)


@dataclass
class CandidateEvent:
    platform: str | None
    text: str
    created_time: str | None
    permalink: str | None
    source_location: str | None
    inferred_venue: str | None
    date_hint: str | None


def _is_comedy_related(text: str) -> bool:
    haystack = text.lower()
    return any(keyword in haystack for keyword in COMEDY_KEYWORDS)


def _extract_venue(text: str) -> str | None:
    for pattern in VENUE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip(" .,!;:-")
    return None


def _extract_date_hint(text: str) -> str | None:
    match = DATE_PATTERN.search(text)
    return match.group(0) if match else None


def extract_events(posts: Iterable[dict]) -> list[CandidateEvent]:
    events: list[CandidateEvent] = []
    for post in posts:
        text = (post.get("text") or "").strip()
        if not text or not _is_comedy_related(text):
            continue

        events.append(
            CandidateEvent(
                platform=post.get("platform"),
                text=text,
                created_time=post.get("created_time"),
                permalink=post.get("permalink"),
                source_location=post.get("location"),
                inferred_venue=_extract_venue(text),
                date_hint=_extract_date_hint(text),
            )
        )
    return events


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to JSON file with post list")
    parser.add_argument("--output", required=True, help="Path to write extracted events JSON")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    posts = json.loads(input_path.read_text(encoding="utf-8"))
    events = extract_events(posts)

    output_path.write_text(
        json.dumps([asdict(event) for event in events], indent=2),
        encoding="utf-8",
    )

    print(f"Extracted {len(events)} candidate comedy events -> {output_path}")


if __name__ == "__main__":
    main()
