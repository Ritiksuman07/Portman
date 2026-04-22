# QuantFlow

Autonomous agentic framework prototype for quantitative finance.

This implementation is built from the attached QuantFlow PRD (Draft v1.0, April 2026) and ships an end-to-end local pipeline:

- SEC filing scraper agent (10-K / 10-Q / 8-K metadata + risk signals)
- Reddit sentiment scanner agent (`r/wallstreetbets`, `r/stocks`, `r/investing`)
- Strategy orchestrator from natural-language thesis
- Deterministic backtest engine with Sharpe / max drawdown / Calmar / CAGR
- DuckDB analytics layer for filings, sentiment, strategies, and backtests
- Agentic Alpha artifact export (`report.json`, `README.md`, equity curve chart, generated strategy code)
- Rust backtest engine scaffold in `engine-rs/` with Python fallback runtime

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m quantflow run "short small-cap biotech on FDA rejection patterns" --ticker XBI --offline
```

Generated artifacts are written to `runs/<run_id>/`:

- `report.json`
- `README.md`
- `equity_curve.svg`
- `strategy.py`

DuckDB data is written to `quantflow.duckdb`.

## CLI

```bash
python -m quantflow run "<thesis>" [--ticker XBI] [--lookback-days 252] [--offline]
```

Options:

- `--db-path`: custom DuckDB file (default: `quantflow.duckdb`)
- `--output-root`: output folder for artifacts (default: `runs`)
- `--user-agent`: HTTP user-agent for SEC/Reddit calls
- `--offline`: deterministic fixture mode (no network calls)

## Rust Engine Scaffold

The repository includes a Rust-native engine scaffold in `engine-rs/`.

Build it once Rust is installed:

```bash
cd engine-rs
cargo build --release
```

Then wire the binary path into the Python backtest engine if you want Rust execution in local runs.

## Tests

```bash
pytest
```

The provided test runs the full pipeline in offline mode and validates artifact generation.
