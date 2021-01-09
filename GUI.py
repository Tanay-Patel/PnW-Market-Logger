import tkinter as tk
import json
import matplotlib
import PnWTradeHistoryLogger
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
from matplotlib.figure import Figure

matplotlib.use('TkAgg')

# Creates matplotlib Figure for later use.
f = Figure(figsize=(4, 4), dpi=100)
a = f.add_subplot(111)
style.use('ggplot')

# Initializing variables for use.
foodAVG, uraniumAVG, oilAVG, coalAVG, ironAVG, bauxiteAVG, leadAVG, aluAVG, gasolineAVG, munitionsAVG, steelAVG = ([] for i in range(11))
xList = []
yList = [foodAVG, uraniumAVG, oilAVG, coalAVG, ironAVG, bauxiteAVG, leadAVG, aluAVG, gasolineAVG, munitionsAVG, steelAVG]
legend_names = ['Food', 'Uran', 'Oil', 'Coal', 'Iron', 'Baux', 'Lead', 'Alum', 'Gas', 'Muni', 'Steel']
element_names = ['avgfood','avgoil','avguranium','avgcoal','avgiron','avgbauxite','avglead','avgaluminum','avggasoline','avgmunitions','avgsteel']
colours = ['#f2b55a', '#29b36e', '#736a60', '#2e3342', '#878c82', '#a36500', '#5f109c', '#9ad0ed', '#bf0f21', '#e87400', 'k']
show_resource = [True]*11


# This method is used to toggle which lines are displayed on the graph.
def show_line(number):
    show_resource[number] = not (show_resource[number])
    plot_lines()


# This method will update the canvas and plot the lines of each resource.
def plot_lines():
    a.clear()
    for counter in range(len(show_resource)):
        if show_resource[counter]:
            a.plot(xList, yList[counter], color=colours[counter], label=legend_names[counter])
            a.legend(bbox_to_anchor=(0.09, 1.02, 1, 0.102), ncol=11, fontsize=8)

    f.canvas.draw()


# This function will run every 60000ms to update the information that is displayed on graph in real-time.
def animate(i):
    # Update data to most recent API server data.
    PnWTradeHistoryLogger.update_trade_data()

    # Clears the contents of both lists.
    xList.clear()
    for i in range(len(yList)):
        yList[i].clear()

    # Loads trade history from text file.
    history_file = open('TradeLogger.txt', 'r')
    trade_history = json.load(history_file)
    history_file.close()

    # This loop updates values of the x-axis and y-axis for all resources.
    for data in trade_history:
        day = trade_history[data]

        xList.append(int(data))
        for element in range(len(yList)):
            yList[element].append(int(day[element_names[element]]))

    # Update visual representation of data.
    a.clear()
    plot_lines()


# This class is used to customise and display all elements of the application window.
class Window(tk.Frame):

    # Initialization.
    def __init__(self, frame):
        tk.Frame.__init__(self)
        self.frame = frame

        # Creates a canvas and defines its properties.
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Creates toolbar to interact with graph.
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()

        # Creates background label colors.
        background_label1 = tk.Label(frame, bg='#42bcf5', width=41, height=5, borderwidth=5, relief="solid")
        background_label1.place(x=605, y=-20)
        background_label2 = tk.Label(frame, bg='#fc6453', width=50, height=5, borderwidth=5, relief="solid")
        background_label2.place(x=255, y=-20)
        background_label3 = tk.Label(frame, bg='#0dff7e', width=13, height=5, borderwidth=5, relief="solid")
        background_label3.place(x=158, y=-20)
        background_label4 = tk.Label(frame, bg='#ffc30d', width=12, height=5, borderwidth=5, relief="solid")
        background_label4.place(x=68, y=-20)

        # Creates labels to title types of resources.
        label = tk.Label(frame, text='Manufactored Resources', bg='#42bcf5')
        label.place(x=700, y=5)
        label = tk.Label(frame, text='Raw Resources', bg='#fc6453')
        label.place(x=395, y=5)
        label = tk.Label(frame, text='Power', bg='#0dff7e')
        label.place(x=190, y=5)
        label = tk.Label(frame, text='Consumption', bg='#ffc30d')
        label.place(x=75, y=5)

        # This loop places all buttons onto the window.
        x_placement = 85
        buttons = []
        for i in range(len(legend_names)):
            if (i == 1) or (i == 2) or (i == 7):
                x_placement += 31
            b = tk.Button(frame, text=legend_names[i], width=7, command=lambda i=i: show_line(i))
            b.place(x=x_placement + (65 * i), y=30)
            buttons.append(b)

        # Packing all elements.
        self.pack(side='bottom', fill='both', expand=False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


# Defines window properties and main update loop properties.
root = tk.Tk()
root.geometry('900x500')
root.resizable(False, False)
app = Window(root)
ani = animation.FuncAnimation(f, animate, interval=1800000)
root.iconphoto(False, tk.PhotoImage(file='icon.png'))
root.title('Politics And War Price-Tracking')
root.mainloop()