
import sys

from django.conf import settings

from .common.price_tree import PriceTree
from .common.ptree_iterator import ComplexIterator
from common.rabbitmq import producer
from .common.schemas import OrderInputSchema

from trade_manager import dal as trade_manager_dal

class OrderBook(object):
    def __init__(self):
        self.bids = PriceTree('Bids')
        self.asks = PriceTree('Asks')

    def create_order(self, data):
        order_schema = OrderInputSchema()
        order = order_schema.loads(data)
        self.process_order(order)

    def update_order(self, id, curr_price, new_price, side):
        matching_tree = self.bids if side == 1 else self.asks
        order = matching_tree.update_order_price_and_order_price_list(id, curr_price, new_price)
        print(order)
        if order:
            self.process_order(order, new_order=False)

    def delete_order(self, id, curr_price, side):
        matching_tree = self.bids if side == 1 else self.asks
        matching_tree.remove_order_from_price_tree_and_order_price_list(id, curr_price)


    def process_order(self, curr_order, new_order=True):
        """
        Generic method to process a Bid or Ask order
        :param curr_order:
        """
        opposite_tree = self.bids if not curr_order.is_bid else self.asks
        # Try first to match this order with the opposite tree
        trades = opposite_tree.match_price_order(curr_order)
        # If there is remaining order quantity add it to the matching tree if order is a new one not modified.
        if curr_order.quantity != 0 and new_order:
            matching_tree = self.bids if curr_order.is_bid else self.asks
            matching_tree.insert_price_order(curr_order)
        
        if curr_order.trade_quantity > 0:
            # add database entries for trades
            self.create_entry_for_trades(curr_order, trades)
            # put trades information in queue
            self.send_trade_updates_in_queue_for_order(curr_order.id)
        curr_order.trade_quantity = 0
        # And then the OB state
        # self.print_book()
        return trades

    def print_book(self):
        print("+-----------------------------------------------------------------+")
        print("| BUY                            | SELL                           |")
        print("| Id       | Volume      | Price | Price | Volume      | Id       |")
        print("+----------+-------------+-------+-------+-------------+----------+")
        bids_it = ComplexIterator(self.bids.tree.values(reverse=True))
        asks_it = ComplexIterator(self.asks.tree.values())
        while bids_it.hasnext() and asks_it.hasnext():
            sys.stdout.write("|")
            bids_it.next().to_print()
            sys.stdout.write("|")
            asks_it.next().to_print()
            sys.stdout.write("|\n")

        while asks_it.hasnext():
            sys.stdout.write("|                                |")
            asks_it.next().to_print()
            sys.stdout.write("|\n")

        while bids_it.hasnext():
            sys.stdout.write("|")
            bids_it.next().to_print()
            sys.stdout.write("|                                |\n")

        print("+-----------------------------------------------------------------+")

    def create_entry_for_trades(self, curr_order, trades):
        for order in trades:
            data = order.get_trade_result(curr_order.id)
            if data:
                # create entry in trade table
                trade_manager_dal.create_trade(**data)
                self.send_trade_updates_in_queue_for_order(order.id)
               
    def send_trade_updates_in_queue_for_order(self, order_id):
        trade_info = trade_manager_dal.get_average_traded_price_and_traded_quantity(order_id)
        producer.publish(
            settings.OUTGOING_QUEUE_TO_SEND_TRADE_UPDATE_TO_ORDER_MANAGER,
            {
                "id":order_id,
                "traded_quantity":trade_info['traded_quantity'],
                "average_traded_price":float(trade_info['average_traded_price'])
            },
            content_type='trade_update'
        )
