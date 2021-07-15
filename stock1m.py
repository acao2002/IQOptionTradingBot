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

print("username: ")
username = input()
print("password: ")
password = input()

history = []

order = False 
mybot=IQ_Option(username,password)

mybot.connect()#connect to iqoption

mybot.change_balance("PRACTICE")
#order,id1 = mybot.buy_order("crypto", "BTCUSD","buy",1, 2,"market")

opcode_data=mybot.get_all_ACTIVES_OPCODE()

#invest = float(mybot.get_async_order(id1)["position-changed"]["msg"]['invest_enrolled'])
mybot.subscribe_top_assets_updated("cfd")

def opcode_to_name(opcode_data,opcode):
    return list(opcode_data.keys())[list(opcode_data.values()).index(opcode)] 

previous_price = 0
count = 0
id1 = 0
invest = 0
position =""
ath = 0
profit_take = 1.5
stop_loss = -1
profit_margin = 0.2
win = 0 
loss = 0

def closePosition(id,percent, position, entry, close, ath, profit_take, profit_margin, stop_loss):
    global win
    global loss
    if percent < stop_loss or (ath!= 0 and (ath - percent >= profit_margin)):
        if percent < stop_loss:
            loss+=1
        else:
            win+=1

        mybot.close_position(id)
        print("closed " + str(percent))
        f = open("stock1m.txt", "a")
        f.write("\n")
        f.write("Volswagen")
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
        f.write("win: " + str(win)+ " loss: "+ str(loss))
        f.write("\n")
        f.write("\n")
        f.close()
        ath = 0
        return False,ath

    if percent > profit_take:
        if percent > ath:
            ath = percent
        return True,ath
    else:
        return True,ath


while True:
    assets = mybot.get_top_assets_updated("cfd")
    current_price = 0
    if assets:
        V = assets[304]
        current_price = V["cur_price"]["value"]

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
        
            order1,id1 = mybot.buy_order("cfd", "VOW3D-CHIX","sell",100, 5,"market",None, None,)
            invest = float(mybot.get_position(id1)[1]["position"]["open_underlying_price"])-0.05
            position = "sell"
            order = True


        elif count == 3:
            count = 0
            print("buy")
            order1,id1 = mybot.buy_order("cfd", "VOW3D-CHIX","buy",100, 5,"market",None, None,)
            invest = float(mybot.get_position(id1)[1]["position"]["open_underlying_price"])+0.05
            position = "buy"
            order = True

        time.sleep(60)
        
    elif order:
        if position == "sell":
                current = float(current_price) + 0.05
                print(position +": "+ str(invest))
                print("current: " + str(current))
                profit = -(current - invest)/invest*100 *5
                print("profit: "+ ('%.2f' %profit) + "%")
                print("ath: " + str(ath))
                order,ath = closePosition(id1,profit,position,invest,current,ath,profit_take,profit_margin,stop_loss)
        else:

                current = float(current_price) - 0.05
                print(position +": "+ str(invest))
                print("current: " + str(current))
                profit = (current - invest)/invest*100*5
                print("profit: "+ ('%.2f' %profit) + "%")
                print("ath: " + str(ath))
                order,ath = closePosition(id1,profit,position,invest,current,ath,profit_take,profit_margin,stop_loss)

        previous_price = current_price
        time.sleep(30)


    else:
        time.sleep(30)
        previous_price = current_price


    


