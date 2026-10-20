"""Channel analytics loaded from a real YouTube Studio export (data/), plus scoring.

Ground truth is computed from the CSVs, never hand-typed, so the accuracy metric
cannot drift from the data.
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path

DATA = Path(__file__).parent / "data"
TARGET_ID = "HTTxE7Y1sko"  # "Your AI Isn't Secure (Here's How It Gets Hacked)", published Apr 24
SHORT_MAX_S = 60


@dataclass(frozen=True)
class Video:
    id: str
    title: str
    published: str
    duration_s: int
    views: int
    watch_hours: float
    subs: int
    impressions: int
    ctr: float

    @property
    def avd_s(self) -> float:
        return self.watch_hours * 3600 / self.views

    @property
    def avd_pct(self) -> float:
        return self.avd_s / self.duration_s * 100


@dataclass
class Channel:
    videos: list[Video]
    baseline: dict[str, float]
    daily_rows: list[dict[str, str]]

    @classmethod
    def load(cls) -> Channel:
        videos: list[Video] = []
        baseline: dict[str, float] = {}
        with open(DATA / "videos.csv", newline="") as f:
            for r in csv.DictReader(f):
                if r["Content"] == "Total":
                    baseline = {
                        "views": int(r["Views"]),
                        "watch_hours": float(r["Watch time (hours)"]),
                        "subs": int(r["Subscribers"]),
                        "impressions": int(r["Impressions"]),
                        "ctr": float(r["Impressions click-through rate (%)"]),
                    }
                    continue
                videos.append(
                    Video(
                        id=r["Content"].strip(),
                        title=r["Video title"],
                        published=r["Video publish time"],
                        duration_s=int(r["Duration"]),
                        views=int(r["Views"]),
                        watch_hours=float(r["Watch time (hours)"]),
                        subs=int(r["Subscribers"]),
                        impressions=int(r["Impressions"]),
                        ctr=float(r["Impressions click-through rate (%)"]),
                    )
                )
        with open(DATA / "daily.csv", newline="") as f:
            daily = [{**r, "Content": r["Content"].strip()} for r in csv.DictReader(f)]
        return cls(videos, baseline, daily)

    def video(self, video_id: str) -> Video:
        for v in self.videos:
            if v.id == video_id:
                return v
        raise KeyError(video_id)

    def long_form(self) -> list[Video]:
        return [v for v in self.videos if v.duration_s > SHORT_MAX_S]

    def daily(self, video_id: str) -> list[tuple[str, int]]:
        return [(r["Date"], int(r["Views"])) for r in self.daily_rows if r["Content"] == video_id]


def ground_truth(channel: Channel | None = None) -> dict[str, object]:
    ch = channel or Channel.load()
    t = ch.video(TARGET_ID)
    long = ch.long_form()
    return {
        "avd_minutes": t.avd_s / 60,
        "avd_pct": t.avd_pct,
        "subs_per_1k": t.subs / t.views * 1000,
        "best_retention_title": max(long, key=lambda v: v.avd_pct).title,
        "top_views_title": max(long, key=lambda v: v.views).title,
    }


_NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _numbers(text: str) -> list[float]:
    return [float(m.replace(",", "")) for m in _NUMBER.findall(text)]


def _squash(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _lead(title: str) -> str:
    return _squash(re.split(r"[?:|(,]", title)[0])


def score_report(report: str, truth: dict[str, object]) -> float:
    """Fraction of the five checked facts present in the report (numbers within tolerance)."""
    nums = _numbers(report)
    squashed = _squash(report)

    def near(value: object, tol: float) -> bool:
        return any(abs(n - float(value)) <= tol for n in nums)  # type: ignore[arg-type]

    facts = [
        near(truth["avd_minutes"], 0.1),
        near(truth["avd_pct"], 0.3),
        near(truth["subs_per_1k"], 0.3),
        _lead(str(truth["best_retention_title"])) in squashed,
        _lead(str(truth["top_views_title"])) in squashed,
    ]
    return sum(facts) / len(facts)
