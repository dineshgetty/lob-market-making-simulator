class BaseStrategy:
    def quote(self, order_book):
        raise NotImplementedError

    def update_inventory_and_cash(self, order_book):
        raise NotImplementedError

    def pnl(self, order_book):
        raise NotImplementedError
