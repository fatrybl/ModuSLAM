from matplotlib import pyplot as plt


def plot_trajectory_2d(x, y):
    plt.figure()
    plt.plot(x, y, marker="o")
    plt.title("Trajectory plot")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.show()


def plot_trajectory_3d(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.plot(x, y, z, marker="o")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.show()
