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
mybot=IQ_Option("acao2020@macduffie.org",input())
mybot.connect()#connect to iqoption

mybot.change_balance("PRACTICE")
#order,id1 = mybot.buy_order("crypto", "BTCUSD","buy",1, 2,"market")

opcode_data=mybot.get_all_ACTIVES_OPCODE()

#invest = float(mybot.get_async_order(id1)["position-changed"]["msg"]['invest_enrolled'])
mybot.subscribe_top_assets_updated("crypto")

def opcode_to_name(opcode_data,opcode):
    return list(opcode_data.keys())[list(opcode_data.values()).index(opcode)] 

previous_price = 0
count = 0
id1 = 0
invest = 0
position =""

def closePosition(id,percent, position, entry, close):

    if percent > 2.5 or percent < -2:
        mybot.close_position(id)
        print("closed " + str(percent))
        f = open("btc2m.txt", "a")
        f.write("\n")
        f.write("position: "+ str(position))
        f.write("\n")
        f.write("entry: "+ str(entry))
        f.write("\n")
        f.write("close: "+ str(close))
        f.write("\n")
        percent = ('%.2f' %percent)
        f.write("profit: " + str(percent)+"%")
        f.write("\n")
        f.write("\n")
        f.close()
        return False
    else:
        return True


while True:
    assets = mybot.get_top_assets_updated("crypto")
    current_price = 0
    if assets:
        BTC = assets[0]
        current_price = BTC["cur_price"]["value"]

    if not order and previous_price != 0:
        #candle manipulation
        if compare(previous_price,current_price) =="high" and count>=0:
            print("green")
            count +=1
            previous_price = current_price
        elif compare(previous_price,current_price)=="high" and count< 0:
            print("green")
            count = 1
            previous_price = current_price
        elif compare(previous_price,current_price)=="low" and count <=0:
            print("red")
            count-=1
            previous_price = current_price
        elif compare(previous_price,current_price)=="low" and count > 0:
            print("red")
            count = -1
            previous_price = current_price
        
        if count == -3:
            count = 0
            print("sell")
        
            order1,id1 = mybot.buy_order("crypto", "BTCUSD","sell",100, 2,"market",None, None,)
            invest = float(current_price) - 77
            position = "sell"
            order = True


        elif count == 3:
            count = 0
            print("buy")
            order1,id1 = mybot.buy_order("crypto", "BTCUSD","buy",100, 2,"market",None, None,) 
            invest = float(current_price) + 77
            position = "buy"
            order = True

        time.sleep(120)
        
    elif order:
        if position == "sell":
                current = float(current_price) + 77
                print(position +": "+ str(invest))
                print("current: " + str(current))
                profit = -(current - invest)/invest*100 *2
                print("profit: "+ ('%.2f' %profit) + "%")
                order = closePosition(id1,profit,position,invest,current)
        else:

                current = float(current_price) - 77
                print(position +": "+ str(invest))
                print("current: " + str(current))
                profit = (current - invest)/invest*100*2
                print("profit: "+ ('%.2f' %profit) + "%")
                order = closePosition(id1,profit,position,invest,current)

        previous_price = current_price
        time.sleep(30)


    else:
        time.sleep(30)
        previous_price = current_price


    


print(mybot.get_balance())