import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import ScalarFormatter
from collections import deque

class CircularChart:
    def __init__(self, master, title, color="#1f538d"):
        self.fig, self.ax = plt.subplots(figsize=(1.5, 1.5), dpi=80)
        self.fig.patch.set_facecolor('#2b2b2b')
        self.color = color
        self.title = title
        
        # Tworzymy canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.update(0)

    def update(self, percent):
        self.ax.clear()
        values = [max(0.1, percent), 100 - percent]
        self.ax.pie(values, colors=[self.color, "#333333"], startangle=90, 
                    counterclock=False, wedgeprops={'width': 0.4, 'edgecolor': '#2b2b2b'})
        self.ax.text(0, 0, f"{int(percent)}%", color='white', ha='center', va='center', fontsize=10, fontweight='bold')
        self.ax.set_title(self.title.upper(), color="white", fontsize=8, fontweight='bold', pad=5)
        self.canvas.draw()

class LiveChart:
    def __init__(self, master, title, color="#1f538d"):
        self.data = deque([0]*20, maxlen=20)
        self.fig, self.ax = plt.subplots(figsize=(2.5, 1.5), dpi=80)
        self.fig.patch.set_facecolor('#2b2b2b')
        self.ax.set_facecolor('#1e1e1e')
        
        self.line, = self.ax.plot(self.data, color=color, linewidth=2, antialiased=True)
        self.ax.set_title(title.upper(), color="white", fontsize=8, fontweight='bold')
        
        y_fmt = ScalarFormatter(useOffset=False)
        y_fmt.set_scientific(False)
        self.ax.yaxis.set_major_formatter(y_fmt)
        
        self.ax.tick_params(axis='both', colors='gray', labelsize=7)
        self.ax.grid(True, linestyle='--', alpha=0.1, color='white')
        
        self.fig.subplots_adjust(left=0.2, bottom=0.2, right=0.9, top=0.8)
        
        for s in self.ax.spines.values(): s.set_visible(False)

        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas_widget = self.canvas.get_tk_widget()

    def update(self, new_value):
        self.data.append(new_value)
        self.line.set_ydata(self.data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()