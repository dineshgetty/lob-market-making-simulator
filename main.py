from core.order import Order
from core.order_book import OrderBook
from strategies.heuristic_mm import HeuristicMM
from strategies.avellaneda_stoikov import AvellanedaStoikovMM
from simulation.simulator import run_simulation
from analysis.metrics import compute_metrics
from analysis.plots import compare_pnl
from analysis.plots import compare_inventory


# ✅ DEMO (controlled prints)
def demo():
    print("\n===== DEMO: Order Book + MM Interaction =====")

    ob = OrderBook()
    ob.verbose = True

    mm = HeuristicMM()

    # ----------------------------
    # Step 1: Realistic wide market
    # ----------------------------
    ob.add_order(Order(1, "buy", 10, 99.5))
    ob.add_order(Order(2, "sell", 10, 101.5))

    print("\nInitial Market:")
    print("Best Bid:", ob.best_bid())
    print("Best Ask:", ob.best_ask())
    print("Mid:", ob.mid_price())

    # MM quotes
    mm.quote(ob)

    print("\nAfter MM Quotes:")
    print("MM Bid Price:", ob.best_bid())
    print("MM Ask Price:", ob.best_ask())

    # ----------------------------
    # Trade 1: hit ASK
    # ----------------------------
    print("\n--- Market BUY hits MM ASK ---")
    ob.add_order(Order(3, "buy", 10, order_type="market"))

    mm.update_inventory_and_cash(ob)

    print("Inventory after SELL:", mm.inventory)
    print("PnL:", mm.pnl(ob))

    # ----------------------------
    # Trade 2: hit BID (NO REQUOTE)
    # ----------------------------
    print("\n--- Market SELL hits MM BID ---")
    ob.add_order(Order(4, "sell", 10, order_type="market"))

    mm.update_inventory_and_cash(ob)

    print("Inventory after BUY:", mm.inventory)
    print("PnL:", mm.pnl(ob))
    
def run_strategy(strategy_class, seed):

    ob = OrderBook()
    strategy = strategy_class()

    # initial market
    ob.add_order(Order(1, "buy", 10, 100))
    ob.add_order(Order(2, "sell", 10, 101))

    results = run_simulation(ob, strategy, steps=200, seed=seed)

    metrics = compute_metrics(results["pnl_series"])

    return results, metrics

def main():

    demo()  # 👈 show working engine ONCE

    seed = 42

    results_h, m_h = run_strategy(HeuristicMM, seed)
    results_as, m_as = run_strategy(AvellanedaStoikovMM, seed)

    print("\n===== COMPARISON =====\n")

    print("Heuristic MM:")
    for k, v in m_h.items():
        print(f"{k}: {v:.4f}")

    print("\nAvellaneda-Stoikov:")
    for k, v in m_as.items():
        print(f"{k}: {v:.4f}")

    # plot comparison
    compare_pnl(
        results_h["pnl_series"],
        results_as["pnl_series"]
    )

    compare_inventory(
        results_h["inventory_series"],
        results_as["inventory_series"]
    )

if __name__ == "__main__":
    main()
