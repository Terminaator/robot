values = "60 1280 229\n" + \
         "90 1300 169\n" + \
         "100 1320 162\n" + \
         "130 1380 132\n" + \
         "160 1500 113\n" + \
         "165 2150 410"

distances = {}

for part in values.split("\n"):
    x = part.split(" ")
    distances[int(x[2])] = int(x[1])
print(distances)
print(min(distances, key=lambda x: abs(x - 3)))
