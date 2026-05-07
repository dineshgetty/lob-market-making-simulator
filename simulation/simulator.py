import random
from core.order import Order


def run_simulation(ob, strategy, steps=100, seed=42):

    random.seed(seed)

    pnl_series = []
    inv_series = []

    # reset logs if reused
    if hasattr(ob, "trade_log"):
        ob.trade_log = []

    for t in range(steps):

        strategy.quote(ob)

        side = random.choice(["buy", "sell", None])

        if side == "buy":
            ob.add_order(Order(1000+t, "buy", 10, order_type="market"))
        elif side == "sell":
            ob.add_order(Order(2000+t, "sell", 10, order_type="market"))

        FAIR = 100

        if ob.best_bid() is None:
            ob.add_order(Order(9991, "buy", 10, FAIR - 1))

        if ob.best_ask() is None:
            ob.add_order(Order(9992, "sell", 10, FAIR + 1))

        strategy.update_inventory_and_cash(ob)

        pnl = strategy.pnl(ob)
        if pnl is not None:
            pnl_series.append(pnl)
            inv_series.append(strategy.inventory)

    return {
        "pnl_series": pnl_series,
        "inventory_series": inv_series,
        "final_pnl": pnl_series[-1] if pnl_series else 0,
        "final_inventory": strategy.inventory,
        "trade_log": getattr(ob, "trade_log", [])
    }
