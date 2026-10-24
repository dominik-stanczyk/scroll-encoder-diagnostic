import time
import matplotlib.pyplot as plt
from pynput import mouse

amount_scrolled = 0
x_array = []
y_array = []

amount_anomaly = 0
amount_sample = 0
raw_direction_history = []
EXPECTED_DIRECTION = -1

def scroll_use(x, y, dx, dy):
    global amount_scrolled, y_array
    amount_scrolled += dy
    y_array.append(amount_scrolled)
    raw_direction_history.append(dy)

listener = mouse.Listener(on_scroll=scroll_use)

listener.start()
print("Measurement Acquisition: Started (Scroll down for 5 seconds...)")

time.sleep(5)

listener.stop()

print("Measurement Acquisition: Stopped")

if len(y_array) == 0:
    print("Error: No encoder input detected.")
else:
    x_array = list(range(len(y_array)))
    total_samples = len(x_array)

    direction_faults = sum(1 for dy in raw_direction_history if dy != EXPECTED_DIRECTION)
    fault_percentage = round((direction_faults / total_samples) * 100, 1)

    # Background color
    plt.rcParams['figure.facecolor'] = '#2e2e2e'
    # Chart background color
    plt.rcParams['axes.facecolor'] = '#f5f5f5'
    # Text, axis, frame color
    plt.rcParams['text.color'] = '#ffffff'
    plt.rcParams['axes.labelcolor'] = '#ffffff'
    plt.rcParams['xtick.color'] = '#ffffff'
    plt.rcParams['ytick.color'] = '#ffffff'
    plt.rcParams['axes.edgecolor'] = '#cccccc'

    plt.plot(x_array, y_array, color="blue", linewidth=2, label="Measured Trajectory")
    plt.xlabel("Sample Index (n)")
    plt.ylabel("Relative Position (Ticks)")
    plt.title("Scroll Encoder Signal Integrity Test")
    plt.minorticks_on()
    plt.grid(True, linestyle=":", alpha=0.5, color="black")
    plt.legend(loc="upper right", labelcolor="black", edgecolor="black", framealpha=1.0)
    remarks = f" Anomaly count: {direction_faults}/{total_samples}\n Anomaly percentage: {fault_percentage}%"

    plt.text(0.02, 0.12, remarks, 
                transform=plt.gca().transAxes, 
                fontsize=10, 
                color='black',
                verticalalignment='top',
                bbox=dict(facecolor='white', boxstyle='round,pad=0.3'))
    plt.show()
    