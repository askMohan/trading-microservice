
import sys


class Order(object):

    def __init__(self, side, id, price, quantity):
        self.side = side
        self.id = id
        self.price = price
        self.quantity = quantity
        # DList: each Order has a next and previous (see OrderList)
        self.next_order = None
        self.prev_order = None
        self.trade_quantity = 0  # Variable to track traded quantity (of matched orders)

    @property
    def is_bid(self):
        """
        Returns if the Order is a bid or not
        :return boolean:
        """
        return self.side == 1
    
    @property
    def get_order_initial_quantity(self):
        """
        Returns if the Order is a bid or not
        :return boolean:
        """
        return self.quantity + self.trade_quantity

    def match(self, other_order):
        """
        Returns true ONLY when other_order matches ALL current quantity
        :param other_order:
        :return boolean:
        """

        if self.quantity <= other_order.quantity:
            new_trade_quantity = self.quantity
            # update both parties
            self.make_trade(new_trade_quantity)
            other_order.make_trade(new_trade_quantity)
            return True
        # partial trade (quantity > other_order.quantity)
        else:
            new_trade_quantity = other_order.quantity
            self.make_trade(new_trade_quantity)
            other_order.make_trade(new_trade_quantity)
            return False

    def make_trade(self, trade_quantity):
        """
        Close a deal of a specific quantity and update remaining order quantitys accordingly
        :param trade_quantity:
        """
        self.trade_quantity += trade_quantity
        self.quantity -= trade_quantity

    def get_trade_result(self, other_order_id):
        if self.trade_quantity > 0:
            quantity = self.trade_quantity
            bid_order_id, ask_order_id = self.id, other_order_id
            if not self.is_bid:
                bid_order_id, ask_order_id = other_order_id, self.id
            self.trade_quantity = 0
            return {
                'bid_order_id': bid_order_id,
                'ask_order_id' : ask_order_id,
                'quantity': quantity,
                'price': self.price
            }

    def to_print(self):
        if self.is_bid:
            sys.stdout.write("{:>10}|{:>13}|{:>7}".format(     # custom line spacing
                    self.id,
                    "{:,}".format(self.quantity),  # thousands separator
                    "{:,}".format(self.price)))
        else:
            sys.stdout.write("{:>7}|{:>13}|{:>10}".format(
                "{:,}".format(self.price),
                "{:,}".format(self.quantity),
                self.id))

    def __str__(self):
        return "Order: side: {} id: {} price: {} quantity {}".format(self.side, self.id, self.price, self.quantity)
