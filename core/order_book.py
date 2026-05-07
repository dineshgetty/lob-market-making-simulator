from sortedcontainers import SortedDict
from collections import deque


class OrderBook:
    def __init__(self):
        self.buy_book = SortedDict(lambda x: -x)
        self.sell_book = SortedDict()
        self.last_traded_price = None
        self.mm_trades = deque()
        self.active_bid_ask_id = []
        self.verbose = False
        self.trade_log = []

    def best_bid(self):
        return next(iter(self.buy_book)) if self.buy_book else None

    def best_ask(self):
        return next(iter(self.sell_book)) if self.sell_book else None

    def mid_price(self):
        if self.best_bid() is None or self.best_ask() is None:
            return None
        return (self.best_bid() + self.best_ask()) / 2

    def handle_trade(self, buy_order, sell_order, price, quantity):

        if buy_order.owner == "mm":
            self.mm_trades.append({"side": buy_order.side, "price": price, "qty": quantity})

        if sell_order.owner == "mm":
            self.mm_trades.append({"side": sell_order.side, "price": price, "qty": quantity})

        for order in [buy_order, sell_order]:
            if order.owner == "mm" and order.quantity == 0:
                if order.order_id in self.active_bid_ask_id:
                    self.active_bid_ask_id.remove(order.order_id)

        self.trade_log.append({
            "price": price,
            "qty": quantity,
            "buy_owner": buy_order.owner,
            "sell_owner": sell_order.owner
        })

    def cancel_order(self, order_id):
        for book in (self.buy_book, self.sell_book):
            for price in list(book):
                queue = book[price]
                new_q = deque(o for o in queue if o.order_id != order_id)
                if new_q:
                    book[price] = new_q
                else:
                    del book[price]

    def add_order(self, order):
        if order.order_type == "market":
            if order.side == "buy":
                self._market_buy(order)
            else:
                self._market_sell(order)
        else:
            if order.side == "buy":
                self._limit_buy(order)
            else:
                self._limit_sell(order)

    def _add_limit(self, order, book):
        if order.price not in book:
            book[order.price] = deque()
        book[order.price].append(order)

    def _market_buy(self, order):
        while order.quantity > 0 and self.sell_book:
            price = self.best_ask()
            queue = self.sell_book[price]
            top = queue[0]

            qty = min(order.quantity, top.quantity)
            order.quantity -= qty
            top.quantity -= qty

            
            if self.verbose:
                print(f"MARKET BUY {qty} @ {price}")
                
            self.last_traded_price = price
            self.handle_trade(order, top, price, qty)

            if top.quantity == 0:
                queue.popleft()
            if not queue:
                del self.sell_book[price]

    def _market_sell(self, order):
        while order.quantity > 0 and self.buy_book:
            price = self.best_bid()
            queue = self.buy_book[price]
            top = queue[0]

            qty = min(order.quantity, top.quantity)
            order.quantity -= qty
            top.quantity -= qty

            if self.verbose:
                print(f"MARKET SELL {qty} @ {price}")
            self.last_traded_price = price
            self.handle_trade(top, order, price, qty)

            if top.quantity == 0:
                queue.popleft()
            if not queue:
                del self.buy_book[price]

    def _limit_buy(self, order):
        while order.quantity > 0 and self.sell_book and order.price >= self.best_ask():
            price = self.best_ask()
            queue = self.sell_book[price]
            top = queue[0]

            qty = min(order.quantity, top.quantity)
            order.quantity -= qty
            top.quantity -= qty

            if self.verbose:
                print(f"TRADED {qty} @ {price}")
            self.last_traded_price = price
            self.handle_trade(order, top, price, qty)

            if top.quantity == 0:
                queue.popleft()
            if not queue:
                del self.sell_book[price]

        if order.quantity > 0:
            self._add_limit(order, self.buy_book)

    def _limit_sell(self, order):
        while order.quantity > 0 and self.buy_book and order.price <= self.best_bid():
            price = self.best_bid()
            queue = self.buy_book[price]
            top = queue[0]

            qty = min(order.quantity, top.quantity)
            order.quantity -= qty
            top.quantity -= qty

            if self.verbose:
                print(f"TRADED {qty} @ {price}")
            self.last_traded_price = price
            self.handle_trade(top, order, price, qty)

            if top.quantity == 0:
                queue.popleft()
            if not queue:
                del self.buy_book[price]

        if order.quantity > 0:
            self._add_limit(order, self.sell_book)
