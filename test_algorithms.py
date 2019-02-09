def mean(list):
    return sum(list) / len(list)

def master_trade(exchange, BOND, VALBZ, VALE, GS, MS, WFC, XLF):
    #should decide which algorithms to call
    #has access to arrays in main.py global
    print('master')


#pennying for trade bond
def trade_bond(exchange):
    bond_buy.append(cur_order_id)
    write_to_exchange(exchange, new_buy_order('BOND', 999, 10))
    write_to_exchange(exchange, new_sell_order('BOND', 1000, 10))

def ETFArbitrage(exchange, XLF, BOND, GS, MS, WFC):
    
