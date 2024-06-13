import ast
import matplotlib.pyplot as plt
import numpy

with open('data.txt') as f:
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
plt.ylabel("Masa acumulada (gramos)")
plt.xlabel("Tiempo (segundos)")

fig2, ax2 = plt.subplots()
ax2.plot(y[:-5], dx[:-4], linewidth=2.0)
ax2.hlines(10, y[0], y[-1], colors = 'red', linestyles = 'dotted')
plt.ylabel("Variación de masa acumulada (Delta gramos)")
plt.xlabel("Tiempo (segundos)")

plt.show()