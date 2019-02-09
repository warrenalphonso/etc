cur_order_id = 0

def new_buy_order(stock, price, num_bought):
    global cur_order_id
    cur_order_id += 1
    order_dict = {'type': 'add', 'order_id': cur_order_id, "symbol": stock, 'dir': 'BUY',
                  'price': price, 'size': num_bought}
    return cur_order_id, order_dict

def new_sell_order(stock, price, num_bought):
    global cur_order_id
    cur_order_id += 1
    order_dict = {'type': 'add', 'order_id': cur_order_id, "symbol": stock, 'dir': 'SELL',
                  'price': price, 'size': num_bought}
    return cur_order_id, order_dict

#stock must be XLF or ADR
#dir must be "BUY" or "SELL"
def new_convert_order(stock, dir, num_bought):
    global cur_order_id
    cur_order_id += 1
    order_dict = {'type': 'convert', 'order_id': cur_order_id, 'symbol': stock, 'dir': dir,
                    'size': num_bought}
    return cur_order_id, order_dict
