# import word2emoji
# print(word2emoji("hello"))
from states import *
x=States()
print(x.get_state())
x.change_state(RUNNING)
print(x.get_state())