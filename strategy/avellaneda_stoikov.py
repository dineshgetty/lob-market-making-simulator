from core.order import Order
from strategies.base_strategy import BaseStrategy
import math


class AvellanedaStoikovMM(BaseStrategy):
    def __init__(self):
        # Model parameters
        self.gamma = 0.1        
        self.sigma = 0.2        
        self.k = 1.5            
        self.T = 1.0            
        self.max_inventory = 50

        # State
        self.inventory = 0
        self.cash = 0
        self.order_id = 2000
        self.t = 0

    def next_id(self):
        self.order_id += 1
        return self.order_id

    def quote(self, ob):

        mid = ob.mid_price()
        if mid is None:
            return

        # time decay (important)
        tau = max(1, (self.T - self.t))

        # --- Reservation price ---
        r = mid - self.inventory * self.gamma * (self.sigma ** 2) * tau

        FAIR_PRICE = 100   # or your reference price

        r = max(
            min(r, FAIR_PRICE + 1),
            FAIR_PRICE - 1
        )

        # --- Optimal spread ---
        spread = (
            self.gamma * (self.sigma ** 2) * tau
            + (2 / self.gamma) * math.log(1 + self.gamma / self.k)
        )

        spread = max(spread, 1.0)

        if self.inventory >= self.max_inventory:
            # only sell allowed
            place_bid = False
            place_ask = True

        elif self.inventory <= -self.max_inventory:
            # only buy allowed
            place_bid = True
            place_ask = False

        else:
            place_bid = True
            place_ask = True

        bid = r - spread / 2
        ask = r + spread / 2

        # tick rounding
        tick = 0.5
        bid = round(bid / tick) * tick
        ask = round(ask / tick) * tick

        if bid >= ask:
            return

        # cancel previous quotes
        for oid in list(ob.active_bid_ask_id):
            ob.cancel_order(oid)
        ob.active_bid_ask_id = []

        if place_bid:
            bid_order = Order(self.next_id(), "buy", 10, price=bid, owner="mm")
            ob.add_order(bid_order)
            ob.active_bid_ask_id.append(bid_order.order_id)

        if place_ask:
            ask_order = Order(self.next_id(), "sell", 10, price=ask, owner="mm")
            ob.add_order(ask_order)
            ob.active_bid_ask_id.append(ask_order.order_id)


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
        if mid is None:
            return None
        return self.cash + self.inventory * mid
