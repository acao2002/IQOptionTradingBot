import time
from iqoptionapi.stable_api import IQ_Option
import time

def compare(prev, curr):
    if curr>prev:
        return "high"
    elif curr < prev: 
        return "low"
    else:
        return 0

history = []
order = False 
mybot=IQ_Option(input("username:"),input("password"))
mybot.connect()#connect to iqoption

mybot.change_balance("PRACTICE")
#order,id1 = mybot.buy_order("crypto", "BTCUSD","buy",1, 2,"market")

opcode_data=mybot.get_all_ACTIVES_OPCODE()

#invest = float(mybot.get_async_order(id1)["position-changed"]["msg"]['invest_enrolled'])
mybot.subscribe_top_assets_updated("crypto")

def opcode_to_name(opcode_data,opcode):
    return list(opcode_data.keys())[list(opcode_data.values()).index(opcode)] 


def percent_change(compare_price, current_price):
    change = (current_price - compare_price)/compare_price*100 *2
    change = '%.2f'%change
    return float(change)

def reset():
    for id in positions:
        mybot.close_position(id)


    order1,id1 = mybot.buy_order("crypto", "BTCUSD","buy",50, 2,"market",None, None,)
    positions.append(id1)
    compare_price = float(mybot.get_position(id1)[1]["position"]["open_underlying_price"])



positions =[]
order1,id1 = mybot.buy_order("crypto", "BTCUSD","buy",50, 2,"market",None, None,)

positions.append(id1)
compare_price = float(mybot.get_position(id1)[1]["position"]["open_underlying_price"])
current_price = compare_price
invest = 50
orders = 1
win = False
win_percent = 0

lossdca = -2
profit_margin = 0.5
profit = 2
dca_factor = 1.5

f = open("dcav2.txt", "a")
f.write("\n")
f.write("buy " + str(invest) + " at " +str(current_price))
f.write("\n")
f.close()

while True:
    assets = mybot.get_top_assets_updated("crypto")
    if assets:
        BTC = assets[0]
        current_price = BTC["cur_price"]["value"]

    print("BTC: ")
    print("compare price: "+ str(compare_price))
    print("current price: "+ str(current_price))
    percent = percent_change(compare_price,current_price)
    print(str(percent)+ " %")
    
    if percent < lossdca and not win and orders < 6:
        orders += 1
        invest = invest*dca_factor
        compare_price = current_price
        lossdca -= 0.5
        profit + 0.7
        order1,id1 = mybot.buy_order("crypto", "BTCUSD","buy",invest, 2,"market",None, None,)
        f = open("dcav2.txt", "a")
        f.write("\n")
        f.write("buy " + str(invest) + " at " +str(current_price))
        f.write("\n")
        f.close()
        positions.append(id1)
    
    elif percent > profit and not win:
        win_percent = percent
        win = True
    
    elif win:
        print("ath: "+ str(win_percent))
        if compare(win_percent, percent) == "high":
            win_percent = percent
        elif (win_percent - percent) >= profit_margin:
            win = False
            f = open("dcav2.txt", "a")
            f.write("\n")
            f.write("close order")
            f.write("\n")
            f.write("profit from lowest trade: "+ str(percent))
            f.write("\n")
            f.close()
            reset()
            invest = 50
            orders = 1
            lossdca = -2
            profit = 2
            compare_price = current_price
    
    
    time.sleep(30)
    
    