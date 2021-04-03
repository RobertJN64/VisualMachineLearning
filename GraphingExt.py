from matplotlib import pyplot

#TODO - make this a sep library

def Graph3D(x, y, z, color, xlabel="", ylabel="", zlabel="", title="", block=True, plt=None, s=None):
    if plt is None:
        fig = pyplot.figure()
        plt = fig.add_subplot(111, projection='3d')
    if s is None:
        plt.scatter(x, y, z, color=color)
    else:
        plt.scatter(x, y, z, color=color, s=s)
    plt.set_xlabel(xlabel)
    plt.set_ylabel(ylabel)
    plt.set_zlabel(zlabel)
    plt.set_title(title)
    if plt is None:
        pyplot.show(block=block)

def multiGraph3D(xs, ys, zs, colors, xlabel='', ylabel='', zlabel='', title='', block=True, plt=None, ss=None):
    if plt is None:
        fig = pyplot.figure()
        plt = fig.add_subplot(111, projection='3d')

    for i in range(0, len(xs)):
        if ss is None:
            plt.scatter(xs[i], ys[i], zs[i], color=colors[i])
        else:
            plt.scatter(xs[i], ys[i], zs[i], color=colors[i], s=ss[i])
    plt.set_xlabel(xlabel)
    plt.set_ylabel(ylabel)
    plt.set_zlabel(zlabel)
    plt.set_title(title)
    if plt is None:
        pyplot.show(block=block)



