lest = ["1", "1.5", "11", "2", "20", "21", "3", "30", "31", "4", "5", "6", "AuCl3"]
a = []
b = []

print(type(lest))
print(type(a))
print(type(b))
for i in range(len(lest)):
    try:
        a.append(float(lest[i]))
        print(a)
    except:
        b.append(lest[i])
a.sort()
a += b
print(a)
