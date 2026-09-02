from datetime import date
from pathlib import Path

from options_research.fixtures import load_fixture_bundle
from options_research.report import generate_report


def test_report_generation_emits_ranked_strategy_results(tmp_path: Path):
    bundle = load_fixture_bundle()
    output = tmp_path / "report.md"

    report = generate_report(
        bundle=bundle,
        tickers=["NVDA", "TSLA"],
        start=date(2023, 1, 1),
        end=date(2024, 12, 31),
        output_path=output,
    )

    assert output.exists()
    text = output.read_text()
    assert "# Options Research Report" in text
    assert "Ranked Opportunities" in text
    assert "NVDA" in text
    assert "TSLA" in text
    assert "fixture data" in text.lower()
    assert report.results
