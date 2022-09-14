f = open("Source/PickPlaceforBasismodule.txt", "r")
FRead = f.read().replace("\n", "|").replace("\r", "|")
FRead = " ".join(FRead.split())
#print(" ".join(f.read().split()))
array = FRead.split("|")
for x in range(0, array.count('')):
    array.remove('')
print(array)