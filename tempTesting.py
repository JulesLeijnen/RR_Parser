# import re

# f = open("Source/PickPlaceforBasismodule.txt", "r")
# FRead = f.read().replace("\n", "|").replace("\r", "|")
# #FRead = " ".join(FRead.split())
# # #print(" ".join(f.read().split()))
# array = FRead.split("|")
# print(array)
# emptyarray = []
# for i in array:
#     i.strip()
#     print('\n\n\n')
#     x = re.split(r'\s{2,}', i)
#     emptyarray.append(x)
#     #print(x)
# print(emptyarray)

# for i in emptyarray:
#     while "" in i:
#         i.remove("")
#         print("Found in: {}".format(i))
#     while [] in i:
#         i.remove([])
# print(emptyarray)
# while [] in emptyarray:
#     emptyarray.remove([])
# print(emptyarray)


# list = [[1], [2], [3], [4]]
# print(list[1:])

import tkinter as tk

window = tk.Tk()
window.mainloop()