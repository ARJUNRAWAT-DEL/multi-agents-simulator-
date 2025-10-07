import io
import re
from typing import List, Optional
import matplotlib.pyplot as plt
import pandas as pd

# Extract some numeric insight from conversation or report, build a simple plot.
# If no numbers present, generate a deterministic example trend.

NUM_RE = re.compile(r"(\d+(?:\.\d+)?)%")


def _extract_percentages(text: str) -> list[float]:
    return [float(x) for x in NUM_RE.findall(text or "")]


def _fallback_series(seed_text: str) -> pd.DataFrame:
    # Deterministic pseudo-series based on characters
    base = sum(ord(c) for c in (seed_text or "ai")) % 10 + 5
    vals = [base]
    for i in range(1, 8):
        vals.append(vals[-1] * (1.0 + ((i % 3) - 1) * 0.05))
    return pd.DataFrame({"Week": list(range(1, 9)), "Metric": vals})


def build_insight_plot(history: List[dict], report: Optional[str]):
    text_blob = (report or "") + "\n\n" + "\n".join(m.get("content", "") for m in (history or []))
    percents = _extract_percentages(text_blob)

    if len(percents) >= 4:
        df = pd.DataFrame({"Phase": [f"P{i+1}" for i in range(len(percents[:8]))],
                           "%": percents[:8]})
        fig = plt.figure()
        plt.plot(df["Phase"], df["%"], marker="o")
        plt.title("Key Percentage Metrics Across Phases")
        plt.xlabel("Phase")
        plt.ylabel("Percent")
        plt.grid(True, linestyle=":", linewidth=0.5)
        return fig

    # Fallback synthetic trend
    df = _fallback_series(report or "")
    fig = plt.figure()
    plt.plot(df["Week"], df["Metric"], marker="o")
    plt.title("Projected Metric Over Time (Synthetic)")
    plt.xlabel("Week")
    plt.ylabel("Value")
    plt.grid(True, linestyle=":", linewidth=0.5)
    return fig