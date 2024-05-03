import ast
import matplotlib.pyplot as plt

with open('pesos.txt') as f:
    lines = ast.literal_eval(f.read())
    print(lines)
    #x = [line.split()[0] for line in lines]
    #y = [line.split()[1] for line in lines]

vectors = list(zip(*lines))

print(vectors[0])


# make data
x = vectors[0]
y = vectors[1]

# plot
fig, ax = plt.subplots()

ax.plot(y, x, linewidth=2.0)
plt.show()