

cur_order_id = 0


def new_buy_order(stock, price, num_bought):
    global cur_order_id
    order_dict = {'type': 'add', 'order_id': cur_order_id, "symbol": stock, 'dir': 'BUY',
                  'price': price, 'size': num_bought}
    cur_order_id += 1
    return order_dict


def new_sell_order(stock, price, num_bought):
    global cur_order_id
    order_dict = {'type': 'add', 'order_id': cur_order_id, "symbol": stock, 'dir': 'SELL',
                  'price': price, 'size': num_bought}
    cur_order_id += 1
    return order_dict


