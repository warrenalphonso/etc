#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
import time
from utils import *
from test_algorithms import *

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="VW"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index = 0
prod_exchange_hostname="production"
server_status = 0 #0 means it's disconnected

# the JSON ports are 25000, 25001 and 25002.
port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
#connect to server
def connect():
    global server_status
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Starting connection... ')
    s.connect((exchange_hostname, port))
    print('Connection secured. ')
    server_status = 1
    return s.makefile('rw', 1)

def reconnect():
    global server_status
    while server_status == 0:
        print('Attempting to reconnect...')
        try:
            exchange = connect()
            write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
            hello_from_exchange = read_from_exchange(exchange)
            print('Reconnect message: ', hello_from_exchange)
            if hello_from_exchange["type"] == "hello":
                server_status = 1
                print('Reconnect successful!!!!!!')
            else:
                print('Error reconnecting ')
        except:
            print('Error... trying again in .1 seconds')
            time.sleep(0.1)





def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())


# ~~~~~============== SERVER INFO ==============~~~~~
def get_info(exchange):
    global server_status
    global bond_own, pnl, valbz_own, vale_own, gs_own, ms_own, wfc_own, xlf_own
    count = 0 #how long i should process the info
    print('Received info from server')
    while count < 100:
        info = read_from_exchange(exchange)
        type = info["type"]
        if type == "trade":
            symbol = info["symbol"]
            if symbol == "BOND":
                price = info["price"]
                bond.extend([price for i in range(info["size"])])
            elif symbol == "VALBZ":
                price = info["price"]
                valbz.extend([price for i in range(info["size"])])
            elif symbol == "VALE":
                price = info["price"]
                vale.extend([price for i in range(info["size"])])
            elif symbol == "GS":
                price = info["price"]
                gs.extend([price for i in range(info["size"])])
            elif symbol == "MS":
                price = info["price"]
                ms.extend([price for i in range(info["size"])])
            elif symbol == "WFC":
                price = info["price"]
                wfc.extend([price for i in range(info["size"])])
            elif symbol == "XLF":
                price = info["price"]
                xlf.extend([price for i in range(info["size"])])



            # if symbol == "BOND":
                # print('bid prices')
                # buy = info["buy"]
                # for i in buy:
                #     print(i[0])
                # print('sell prices')
                # sell = info["sell"]
                # for i in sell:
                #     print(i[0])
        elif type == "ack":
            print('order successful -------------')

        elif type == 'fill':
            symbol = info["symbol"]
            dir = info["dir"]
            if dir == "BUY":
                if symbol == "BOND":
                    bond_own += info["size"]
                    pnl -= info["size"] * info["price"]
                elif symbol == "VALBZ":
                    valbz_own += info["size"]
                    pnl -= info["size"] * info["price"]
                elif symbol == "VALE":
                    vale_own += info["size"]
                    pnl -= info["size"] * info["price"]
                elif symbol == "GS":
                    gs_own += info["size"]
                    pnl -= info["size"] * info["price"]
                elif symbol == "MS":
                    ms_own += info["size"]
                    pnl -= info["size"] * info["price"]
                elif symbol == "WFC":
                    wfc_own += info["size"]
                    pnl -= info["size"] * info["price"]
                elif symbol == "XLF":
                    xlf_own += info["size"]
                    pnl -= info["size"] * info["price"]
            else:
                if symbol == "BOND":
                    bond_own -= info["size"]
                    pnl += info["size"] * info["price"]
                elif symbol == "VALBZ":
                    valbz_own -= info["size"]
                    pnl += info["size"] * info["price"]
                elif symbol == "VALE":
                    vale_own -= info["size"]
                    pnl += info["size"] * info["price"]
                elif symbol == "GS":
                    gs_own -= info["size"]
                    pnl += info["size"] * info["price"]
                elif symbol == "MS":
                    ms_own -= info["size"]
                    pnl += info["size"] * info["price"]
                elif symbol == "WFC":
                    wfc_own -= info["size"]
                    pnl += info["size"] * info["price"]
                elif symbol == "XLF":
                    xlf_own -= info["size"]
                    pnl += info["size"] * info["price"]
        elif type == "reject":
            print(info["error"])
            # "OUT": this only gives us id so maybe just remove stocks from own lists when we call cancel???
        count += 1
    print("PNL:", pnl)


def trade_bond(exchange):
    global bond_own
    order_id, cur_buy_order = new_buy_order('BOND', 999, 10)
    bond_buy_orders.append(order_id)
    write_to_exchange(exchange, cur_buy_order)
    print(bond_buy_orders)
    print(bond_own)
    if bond_own > 0:
        order_id, cur_sell_order = new_sell_order('BOND', 1000, 10)
        bond_sell_orders.append(order_id)
        write_to_exchange(exchange, cur_sell_order)


def master_trade(exchange, BOND, VALBZ, VALE, GS, MS, WFC, XLF):
    #should decide which algorithms to call
    #has access to arrays in main.py global
    print(pnl)

    if pnl < -10000:
        return None

    #check if buying ETF or its constituents is a good idea
    #NEED TO IMMEDIATELY convert and sell so we don't have to keep track of price at which we bought it
    if XLF and WFC and MS and GS and BOND:

        XLF_p = mean(XLF)
        BOND_p = mean(BOND)
        GS_p = mean(GS)
        MS_p = mean(MS)
        WFC_p = mean(WFC)
        etf_strat = checkETF(XLF_p, BOND_p, GS_p, MS_p, WFC_p)
        if etf_strat == "buyxlf":
            write_to_exchange(exchange, new_buy_order('XLF', XLF_p + 1, 20)[1]) #we need to think about how sell order works do i need to store the id??
            write_to_exchange(exchange, new_convert_order('XLF', 'SELL', xlf_own // 10)[1])
            write_to_exchange(exchange, new_sell_order('BOND', BOND_p - 1, bond_own)[1])
            write_to_exchange(exchange, new_sell_order('GS', GS_p - 1, gs_own)[1])
            write_to_exchange(exchange, new_sell_order('MS', MS_p - 1, ms_own)[1])
            write_to_exchange(exchange, new_sell_order('WFC', WFC_p - 1, wfc_own)[1])
        elif etf_strat == "buysum":
            write_to_exchange(exchange, new_buy_order('BOND', BOND_p + 1, 6)[1])
            write_to_exchange(exchange, new_buy_order('GS', GS_p + 1, 4)[1])
            write_to_exchange(exchange, new_buy_order('MS', MS_p + 1, 6)[1])
            write_to_exchange(exchange, new_buy_order('WFC', WFC_p + 1, 4)[1])
            num_XLF_to_buy = min(bond_own / .3, gs_own / .2, ms_own / .3, wfc_own / .2) // 1
            write_to_exchange(exchange, new_convert_order('XLF', 'BUY', num_XLF_to_buy)[1])
            write_to_exchange(exchange, new_sell_order('XLF', XLF_p - 1, xlf_own)[1])

        elif etf_strat == "buynone":
            print('dont do etf')

        #check if selling ETF or its constituents






# ~~~~~============== MAIN LOOP ==============~~~~~
bond = [] #fair value of 1000
valbz = []
vale = [] #ADR of valbz; 10 per conversion
gs = []
ms = []
wfc = []
xlf = [] #.3 bond; .2 gs; .2 ms; .2 wfc  ;  100 per conversion

bond_buy_orders = []
bond_sell_orders = []
bond_own = 0
valbz_own = 0
vale_own = 0
gs_own = 0
ms_own = 0
wfc_own = 0
xlf_own = 0

pnl = 0

def main():
    exchange = connect()
    print('Initialize successful')
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)

    while True:
        get_info(exchange)
        if server_status == 1:
            print('stuff to do when everythings working after we get info')
            master_trade(exchange, bond, valbz, vale, gs, ms, wfc, xlf)
        else:
            print('Need to reconnect because market probably restarted')
            reconnect()




if __name__ == "__main__":
    main()
