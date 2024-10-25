import ast
import matplotlib.pyplot as plt
import numpy

with open('data.txt') as f:
    lines = ast.literal_eval(f.read())
    #print(lines)
    #x = [line.split()[0] for line in lines]
    #times = [line.split()[1] for line in lines]

vectors = list(zip(*lines))

#print(vectors[0])


# make data
x = vectors[0]
times = vectors[1]

th = 15
u = []
lm = 0
for i in range(len(x)-1):
    current = x[i] - lm
    u.append(current)
    if current > th:
        lm = x[i+1]
print(u)
# plot
fig, ax = plt.subplots()
ax.plot(times, x, linewidth=2.0)
#ax.plot(times, u,'r', linewidth=2.0)
plt.ylabel("Masa acumulada (gramos)")
plt.xlabel("Tiempo (segundos)")

fig2, ax2 = plt.subplots()
ax2.plot(times[:-5], u[:-4], linewidth=2.0)
ax2.hlines(th, times[0], times[-1], colors = 'red', linestyles = 'dotted')
plt.ylabel("Masa acumulada tras avalancha (gramos)")
plt.xlabel("Tiempo (segundos)")

plt.show()