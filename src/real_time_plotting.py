import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl

# Create figure for plotting
COLOR = '#FFFFFF'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR

fig = plt.figure(figsize = (10,5),tight_layout=True, facecolor='#262626')
ax = fig.add_subplot(1, 1, 1)
ax.set_facecolor("#262626")

xs = []
ys = []
y_avg = []

# This function is called periodically from FuncAnimation
def animate(i, xs, ys, y_avg):

    zz = float(input())
    print(zz)

    xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    ys.append(zz)

    y_avg.append(sum(ys)/len(ys))

    # Limit x and y lists to the last 20 items
    xs = xs[-20:]
    ys = ys[-20:]
    y_avg = y_avg[-20:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, label='mV', marker='o', color='#08F7FE')
    ax.plot(xs, y_avg, label ='Moving average [mV]', color='#FE53BB')

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('RoGlove input measurements [mV]')
    plt.legend(loc='upper right', framealpha=0)
    plt.grid(color='#454545', linestyle='-', linewidth=0.3)
    plt.ylabel('mV')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, y_avg), interval=1000)
plt.show()
