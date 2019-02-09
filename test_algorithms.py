def mean(list):
    return sum(list) / len(list)

#pennying for trade bond
def trade_bond(exchange):
    bond_buy.append(cur_order_id)
    write_to_exchange(exchange, new_buy_order('BOND', 999, 10))
    write_to_exchange(exchange, new_sell_order('BOND', 1000, 10))

def check_buy_ETF(XLF_p, BOND_p, GS_p, MS_p, WFC_p):
    #need to implement prioritizing liquid one higher
    xlf_minus_sum = XLF_p - (.3 * BOND_p + .2 * GS_p + .3 * MS_p + .2 * WFC_p)
    if xlf_minus_sum > 30:
        return "buysum"
    elif xlf_minus_sum < -20:
        return "buyxlf"
    else:
        return "buynone"
