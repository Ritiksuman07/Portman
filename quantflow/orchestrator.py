from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
import json
from pathlib import Path
import re

from quantflow.agents import RedditSentimentAgent, SecFilingScraperAgent, StrategyOrchestratorAgent
from quantflow.backtest import BacktestEngine
from quantflow.config import QuantFlowConfig
from quantflow.data import DuckDBStore, MarketDataProvider
from quantflow.models import PipelineResult
from quantflow.reporting import build_agentic_alpha_readme, render_equity_curve_svg

TICKER_PATTERN = re.compile(r"\b[A-Z]{1,5}\b")
COMMON_WORDS = {"FDA", "ON", "THE", "AND", "WITH", "SHORT", "LONG"}


class QuantFlowOrchestrator:
    def __init__(self, config: QuantFlowConfig):
        self._config = config
        self._sec_agent = SecFilingScraperAgent(config)
        self._reddit_agent = RedditSentimentAgent(config)
        self._strategy_agent = StrategyOrchestratorAgent()
        self._market_data = MarketDataProvider(config)
        self._backtest_engine = BacktestEngine()

    def run(self, thesis: str, ticker: str | None = None, lookback_days: int = 252) -> PipelineResult:
        normalized_ticker = (ticker or self._infer_ticker(thesis)).upper()
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_dir = self._config.output_root / run_id
        output_dir.mkdir(parents=True, exist_ok=True)
        self._config.db_path.parent.mkdir(parents=True, exist_ok=True)

        sec_rows, sec_summary = self._sec_agent.collect(normalized_ticker)
        sentiment_rows, sentiment_summary = self._reddit_agent.collect(normalized_ticker)
        strategy = self._strategy_agent.generate(
            thesis=thesis,
            ticker=normalized_ticker,
            sec_summary=sec_summary,
            sentiment_summary=sentiment_summary,
        )
        prices = self._market_data.get_daily_closes(normalized_ticker, lookback_days=lookback_days)
        backtest = self._backtest_engine.run(ticker=normalized_ticker, side=strategy.side, prices=prices)

        chart_path = output_dir / "equity_curve.svg"
        render_equity_curve_svg(backtest.equity_curve, chart_path)

        strategy_path = output_dir / "strategy.py"
        strategy_path.write_text(strategy.generated_code, encoding="utf-8")

        readme_path = output_dir / "README.md"
        readme_path.write_text(
            build_agentic_alpha_readme(
                thesis=thesis,
                ticker=normalized_ticker,
                strategy=strategy,
                sec_summary=sec_summary,
                sentiment_summary=sentiment_summary,
                backtest=backtest,
            ),
            encoding="utf-8",
        )

        report_path = output_dir / "report.json"
        report_payload = {
            "run_id": run_id,
            "thesis": thesis,
            "ticker": normalized_ticker,
            "sec_summary": sec_summary,
            "sentiment_summary": sentiment_summary,
            "strategy": asdict(strategy),
            "backtest": asdict(backtest),
            "artifacts": {
                "chart": str(chart_path),
                "strategy": str(strategy_path),
                "readme": str(readme_path),
            },
        }
        report_path.write_text(json.dumps(report_payload, indent=2), encoding="utf-8")

        with DuckDBStore(self._config.db_path) as store:
            store.insert_filings(run_id=run_id, rows=sec_rows)
            store.insert_sentiment(run_id=run_id, rows=sentiment_rows)
            store.insert_strategy(run_id=run_id, strategy=strategy)
            store.insert_backtest(run_id=run_id, backtest=backtest)

        return PipelineResult(
            run_id=run_id,
            ticker=normalized_ticker,
            output_dir=str(output_dir),
            report_path=str(report_path),
            readme_path=str(readme_path),
            chart_path=str(chart_path),
            strategy_path=str(strategy_path),
            backtest=backtest,
        )

    @staticmethod
    def _infer_ticker(thesis: str) -> str:
        matches = TICKER_PATTERN.findall(thesis.upper())
        for match in matches:
            if match in COMMON_WORDS:
                continue
            return match
        lowered = thesis.lower()
        if "biotech" in lowered:
            return "XBI"
        if "small-cap" in lowered or "small cap" in lowered:
            return "IWM"
        return "SPY"
