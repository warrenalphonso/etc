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

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="VW"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = False

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
    count = 0 #how long i should process the info
    print('Received info from server')
    while count < 10:
        info = read_from_exchange(exchange)
        type = info["type"]
        if type == "book":
            symbol = info["symbol"]
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
            bond.append(info["order_id"])
        elif type == "reject":
            print('Failed! Length of array of bonds: ', len(bond))

        count += 1


def trade_bond(exchange):
    write_to_exchange(exchange, new_buy_order('BOND', 999, 10))
    write_to_exchange(exchange, new_buy_order('BOND', 1001, 10))






# ~~~~~============== MAIN LOOP ==============~~~~~
bond = [] #fair value of 1000
valbz = []
vale = [] #ADR of valbz; 10 per conversion
gs = []
ms = []
wfc = []
xlf = [] #.3 bond; .2 gs; .2 ms; .2 wfc  ;  100 per conversion

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
            trade_bond(exchange)
        else:
            print('Need to reconnect because market probably restarted')
            reconnect()




if __name__ == "__main__":
    main()
