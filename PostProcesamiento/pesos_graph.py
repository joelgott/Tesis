import ast
import matplotlib.pyplot as plt
import numpy

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

dx = numpy.diff(x)

# plot
fig, ax = plt.subplots()
ax.plot(y, x, linewidth=2.0)

fig2, ax2 = plt.subplots()
ax2.plot(y[:-1], dx, linewidth=2.0)

plt.show()