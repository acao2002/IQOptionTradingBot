import time
from iqoptionapi.stable_api import IQ_Option
import time

print("username: ")
username = input()
print("password: ")
password = input()

mybot=IQ_Option(username,password)
mybot.connect()#connect to iqoption
mybot.change_balance("PRACTICE")
mybot.reset_practice_balance()
