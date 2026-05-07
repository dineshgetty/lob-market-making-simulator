from core.order import Order
from strategies.base_strategy import BaseStrategy


class HeuristicMM(BaseStrategy):
    def __init__(self):
        self.spread = 1
        self.inventory = 0
        self.cash = 0
        self.k = 0.1
        self.order_id = 1000
        self.last_mid = None

    def next_id(self):
        self.order_id += 1
        return self.order_id

    def quote(self, ob):

        FAIR_PRICE = 100
        mid = ob.mid_price()
        if mid is None:
            return

        mid = max(min(mid, FAIR_PRICE + 0.5), FAIR_PRICE - 0.5)

        if self.last_mid is not None:
            if abs(mid - self.last_mid) < 0.1 and abs(self.inventory) == 0:
                return

        for oid in list(ob.active_bid_ask_id):
            ob.cancel_order(oid)
        ob.active_bid_ask_id = []

        self.last_mid = mid

        skew = self.inventory * self.k

        bid = round((mid - self.spread/2 - skew) / 0.5) * 0.5
        ask = round((mid + self.spread/2 - skew) / 0.5) * 0.5

        if bid >= ask:
            return

        b = Order(self.next_id(), "buy", 10, bid, owner="mm")
        a = Order(self.next_id(), "sell", 10, ask, owner="mm")

        ob.add_order(b)
        ob.active_bid_ask_id.append(b.order_id)

        ob.add_order(a)
        ob.active_bid_ask_id.append(a.order_id)

    def update_inventory_and_cash(self, ob):
        while ob.mm_trades:
            f = ob.mm_trades.popleft()
            if f["side"] == "buy":
                self.inventory += f["qty"]
                self.cash -= f["price"] * f["qty"]
            else:
                self.inventory -= f["qty"]
                self.cash += f["price"] * f["qty"]

    def pnl(self, ob):
        mid = ob.mid_price()
        return None if mid is None else self.cash + self.inventory * mid
