import threading
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation
import arduino

def animate(i, xs, ys, y_avg):
    """Function to be iteratively called from matplotlib animation"""
    try:
        print("VALUE: ", sensor_value)
        xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        ys.append(sensor_value)

        y_avg.append(sum(ys)/len(ys))

        # Limit x and y lists to the last 20 items
        xs = xs[-20:]
        ys = ys[-20:]
        y_avg = y_avg[-20:]

        # Plot values
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
    except Exception as e: print(e)

def read_values_on_thread():
    """Function called in a new thread"""
    global sensor_value
    # Continuously read from a serial port
    while True:
        sensor_value = arduino.readArduino3()
       
if __name__ == '__main__':
    #Initialize arduino
    arduino.initArduino()

    # Wait until receiving sensor measurements
    while True:
        try:
            sensor_value = float(arduino.readArduino()) 
            print(f'Reading from Arduino: {sensor_value}')
            break
        except:
            pass

    print('Started Receiving Serial Values')

    # Initiate and start a new thread that will read data from a port
    read_sensor_data = threading.Thread(target= read_values_on_thread)
    read_sensor_data.start()

    # Set interval for replotting
    INTERVAL = 1000 

    # Set plot colors
    TEXT_COLOR = '#FFFFFF'
    FACE_COLOR = '#262626'

    # Set plot dimensions
    WIDTH = 10
    HEIGHT = 5

    mpl.rcParams['text.color'] = TEXT_COLOR
    mpl.rcParams['axes.labelcolor'] = TEXT_COLOR
    mpl.rcParams['xtick.color'] = TEXT_COLOR
    mpl.rcParams['ytick.color'] = TEXT_COLOR

    # Create a figure for plotting
    fig = plt.figure(figsize = (WIDTH, HEIGHT), tight_layout = True, facecolor = FACE_COLOR)
    ax = fig.add_subplot()
    ax.set_facecolor(FACE_COLOR)

    # Initialite lists that will store values for plotting
    xs = []
    ys = []
    y_avg = []

    # Continous plotting of data
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, y_avg), interval=INTERVAL)
    plt.show()
