import os

cleanup = []

for path in os.listdir("annotations"):
    with open("annotations/" + path) as f:
        xmin, ymin, xmax, ymax = map(int, f.readline().split(','))
        if min(xmax - xmin, ymax - ymin) < 5:
            cleanup.append(path)

inp = input("are you sure, you want to delete {} annotations?".format(len(cleanup)))
if inp == "y":
    for path in cleanup:
        os.remove("annotations/" + path)
    print("deleted {} annotations".format(len(cleanup)))
