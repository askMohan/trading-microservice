from trade_management.trade_manager.order_book_in_error_state import PerCompanyOrderBook
import json
ob = PerCompanyOrderBook()

order_json = {
   "order_id" : 3,
   "quantity" : 20,
   "price": 5,
   "company_code": "company",
   "mode":"sell",
}
order_str = json.dumps(order_json)
ob.new_order(order_str)