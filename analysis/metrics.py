import numpy as np


def compute_metrics(pnl_series):

    pnl = np.array(pnl_series)
    returns = np.diff(pnl)

    sharpe = 0
    if len(returns) > 0:
        sharpe = np.mean(returns) / (np.std(returns) + 1e-9)

    max_drawdown = np.max(np.maximum.accumulate(pnl) - pnl)

    return {
        "final_pnl": pnl[-1],
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "mean_pnl": np.mean(pnl)
    }
