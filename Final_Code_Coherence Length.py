import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.gridspec as gridspec

# Constants
wavelength = 6000e-10
N = 500
D = 0.5
d = 0.001
L_c = 0.3

# Grid (±5 µm)
x = np.linspace(-5e-6, 5e-6, N)
y = np.linspace(-5e-6, 5e-6, N)
X, Y = np.meshgrid(x, y)

# Data for visibility plot
d_list = []
V_list = []

# === Create Layout with GridSpec ===
fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.2])
ax_vis = fig.add_subplot(gs[0])
ax_image = fig.add_subplot(gs[1])
plt.subplots_adjust(bottom=0.25)

# === Intensity image ===
I = np.zeros_like(X)
image = ax_image.imshow(I, cmap='inferno',
                        extent=[x[0]*1e3, x[-1]*1e3, y[0]*1e3, y[-1]*1e3],
                        origin='lower')
plt.colorbar(image, ax=ax_image, label="Intensity")
ax_image.set_xlabel("x (mm)")
ax_image.set_ylabel("y (mm)")
ax_image.set_title("Michelson Interferometer")

# === Visibility plot ===
vis_line, = ax_vis.plot([], [], 'bo-')
ax_vis.set_xlabel("Path Difference (mm)")
ax_vis.set_ylabel("Visibility")
ax_vis.set_title("Visibility vs Path Difference")
ax_vis.set_xlim(0, 2 * d * 1e6 + 10)
ax_vis.set_ylim(0, 1.1)

# === Intensity Calculation ===
def calculate_intensity(d):
    delta = 2 * d * (1 - (np.sqrt(X**2 + Y**2) / D**2))
    delta_phi = (2 * np.pi / wavelength) * delta
    I_0 = 2 * (1 + np.cos(delta_phi))
    V = 1 - (np.abs(delta) / L_c)
    V = np.clip(V, 0, 1)
    return V * I_0, V

# === Update Plots ===
def update_plot(_=None):
    global d
    I, V = calculate_intensity(d)
    image.set_data(I)
    fringe_counter = int((2 * d) / wavelength)
    avg_vis = np.mean(V)

    # Update title
    ax_image.set_title(f"Michelson Interferometer\nPath Difference: {2*d*1e3:.2f} mm | Fringes: {fringe_counter}\nVisibility: {avg_vis:.2f}")

    # Update visibility plot
    d_list.append(2 * d * 1e3)  # Total path diff in µm
    V_list.append(avg_vis)
    vis_line.set_data(d_list, V_list)
    ax_vis.set_xlim(0, max(d_list)+10)
    ax_vis.set_ylim(0, 1.1)
    ax_vis.relim()
    ax_vis.autoscale_view(True, True, True)

    fig.canvas.draw_idle()

# === Button Functions ===
def increase_path(event):
    global d
    d += 1e-3
    update_plot()

def decrease_path(event):
    global d
    d = max(0, d - 1e-3)
    update_plot()

# === Buttons ===
ax_dec = plt.axes([0.52, 0.05, 0.1, 0.075])
ax_inc = plt.axes([0.72, 0.05, 0.1, 0.075])
b_dec = Button(ax_dec, '- d')
b_inc = Button(ax_inc, '+ d')
b_dec.on_clicked(decrease_path)
b_inc.on_clicked(increase_path)

# === Initial Plot ===
update_plot()
plt.show()
