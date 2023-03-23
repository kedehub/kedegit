import matplotlib.pyplot as plt
import numpy as np

# Set up the figure and axes
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-1, 5)
ax.set_ylim(-1, 5)

# Draw the circles representing the random variables
x, y, z, u = np.array([[1, 3], [3, 3], [3, 1], [1, 1]])
ax.scatter(x, y)
ax.scatter(z, u)
ax.add_patch(plt.Circle((1, 3), 1, fill=False))
ax.add_patch(plt.Circle((3, 3), 1, fill=False))
ax.add_patch(plt.Circle((3, 1), 1, fill=False))
ax.add_patch(plt.Circle((1, 1), 1, fill=False))

# Draw the lines representing the conditional entropies and mutual informations
ax.plot([1, 3], [3, 3], color='red')
ax.plot([3, 1], [3, 1], color='red')
ax.plot([3, 3], [3, 1], color='red')
ax.plot([1, 3], [1, 3], color='red')
ax.plot([1, 3], [3, 3], color='blue')
ax.plot([3, 1], [1, 3], color='blue')
ax.plot([1, 3], [1, 1], color='blue')
ax.plot([3, 3], [1, 1], color='blue')

# Add labels to the figure
ax.text(1, 3.5, "$X$", fontsize=14)
ax.text(3, 3.5, "$Y$", fontsize=14)
ax.text(3, 0.5, "$Z$", fontsize=14)
ax.text(1, 0.5, "$U$", fontsize=14)
ax.text(2.25, 2.75, "$H(Y|X,Z,U)$", fontsize=12, color='red')
ax.text(1.75, 0.75, "$H(U|X,Y,Z)$", fontsize=12, color='red')
ax.text(2.75, 0.75, "$H(X|Y,Z,U)$", fontsize=12, color='red')
ax.text(2.25, 1.75, "$H(Z|X,Y,U)$", fontsize=12, color='red')
ax.text(1.5, 2.5, "$I(X;Y|Z,U)$", fontsize=12, color='blue')
ax.text(2.5, 2.5, "$I(X;Z|Y,U)$", fontsize=12, color='blue')
ax.text(2, 1.5, "$I(X;U|Y,Z)$", fontsize=12, color='blue')
ax.text(1, 1.5, "$I(Y;Z|X,U)$", fontsize=12, color='blue')

