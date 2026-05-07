class Order:
    def __init__(self, order_id, side, quantity, price=None, order_type="limit", owner="external"):
        self.order_id = order_id
        self.side = side
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
        self.owner = owner
