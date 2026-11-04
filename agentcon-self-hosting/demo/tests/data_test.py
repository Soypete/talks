"""Ground truth and scoring come from the real YouTube Analytics export in data/."""

import pytest

from analytics_data import TARGET_ID, Channel, ground_truth, score_report


def test_channel_loads_all_videos_and_the_baseline():
    ch = Channel.load()
    assert len(ch.videos) == 32
    assert ch.baseline["views"] == 15452
    assert ch.baseline["ctr"] == pytest.approx(4.75)
    assert ch.video(" -fvMPKLHgeY".strip()).views == 4258  # ids may start with '-'


def test_long_form_is_over_sixty_seconds():
    ch = Channel.load()
    long_ids = {v.id for v in ch.videos if v.duration_s > 60}
    assert len(long_ids) == 7
    assert TARGET_ID in long_ids


def test_ground_truth_for_the_target_episode():
    t = ground_truth()
    assert t["avd_minutes"] == pytest.approx(9.67, abs=0.01)
    assert t["avd_pct"] == pytest.approx(22.4, abs=0.1)
    assert t["subs_per_1k"] == pytest.approx(34.3, abs=0.1)
    assert "Hardware Should You Buy" in t["best_retention_title"]
    assert "Stop Vibe Coding" in t["top_views_title"]


GOOD = (
    "Average view duration is 9.67 minutes, 22.4% of the episode. "
    "Subscribers per 1,000 views: 34.3. Best retention: What AI Hardware Should You Buy. "
    "Most views: Stop Vibe Coding."
)


def test_a_correct_report_scores_full_marks():
    assert score_report(GOOD, ground_truth()) == 1.0


def test_wrong_numbers_lose_points():
    bad = GOOD.replace("9.67", "6.1").replace("34.3", "12")
    assert score_report(bad, ground_truth()) == pytest.approx(0.6)


def test_empty_report_scores_zero():
    assert score_report("", ground_truth()) == 0.0
