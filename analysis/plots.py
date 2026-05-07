import matplotlib.pyplot as plt
import os


# create results folder automatically
os.makedirs("results", exist_ok=True)


def compare_pnl(pnl1, pnl2):

    plt.figure()

    plt.plot(pnl1, label="Heuristic MM")
    plt.plot(pnl2, label="AS Model")

    plt.legend()

    plt.title("PnL Comparison")
    plt.xlabel("Time")
    plt.ylabel("PnL")

    plt.savefig("results/pnl_comparison.png")

def compare_inventory(inv1, inv2):

    plt.figure()

    plt.plot(inv1, label="Heuristic MM")
    plt.plot(inv2, label="AS Model")

    plt.legend()

    plt.title("Inventory Comparison")
    plt.xlabel("Time")
    plt.ylabel("Inventory")

    plt.savefig("results/inventory_comparison.png")
