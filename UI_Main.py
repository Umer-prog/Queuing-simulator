import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
from threading import Thread
from Formulas import simulation_main


# Global variables for the timer
timer_running = False
timer_seconds = 0

# Function to update the parameter input fields dynamically based on the distribution selected

def restart_simulation():
    result_window.destroy()
    # Clear all input fields or reset widgets on the main screen
    for widget in root.winfo_children():
        if isinstance(widget, ttk.Entry):  # If it's an entry field
            widget.delete(0, tk.END)  # Clear the content
        elif isinstance(widget, tk.Frame):  # If it's a frame
            for sub_widget in widget.winfo_children():
                if isinstance(sub_widget, ttk.Entry):  # Clear entries within frames
                    sub_widget.delete(0, tk.END)
    # Redisplay the main window
    root.deiconify()



def end_simulation():
    root.quit()


def show_result_screen():
    global result_window
    simulation_window.destroy()
    result_window = tk.Toplevel()
    result_window.title("Simulation Results")
    result_window.geometry("1250x800")

    # Table Frame
    table_frame = ttk.Frame(result_window)
    table_frame.pack(pady=20)

    columns = ("ID", "Inter-Arrival Time", "Arrival Time", "Service Time", "Start", "End", "Wait", "Response", "Server")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for i in data:
        if i["arr"] < timer_seconds:
            ID = i["ID"]
            inter_arrival = i["IA"]
            arrival = i["arr"]
            service = i["exe"]
            #priority = i["PR"]
            start = i["start"]
            end = i["end"]
            wait = i["WT"]
            response = i["RT"]
            server = i["server"]
            tree.insert("", "end", values=(ID, inter_arrival, arrival, service,  start, end, wait, response
                                           , server))
    tree.pack()


    # Gantt Chart
    gantt_frame = ttk.Frame(result_window)
    gantt_frame.pack(pady=20)

    # Create the Gantt chart
    fig, ax = plt.subplots(figsize=(8, 4))

    # Colors for alternating distinction
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]

    # Plot patients on the Gantt chart
    for idx, patient in enumerate(data):
        if patient["arr"] < timer_seconds:  # Include patients within the timer limit
            server_index = patient["server"] - 1  # Server index (adjust for 0-based indexing)
            start_time = patient["start"]
            service_duration = patient["exe"]
            patient_id = patient["ID"]

            # Choose a color based on patient index
            bar_color = colors[idx % len(colors)]

            # Plot the patient's service time as a bar with a border
            ax.broken_barh(
                [(start_time, service_duration)],
                (server_index * 10, 9),
                facecolors=bar_color,
                edgecolor="black",  # Add border to the bar
                linewidth=1.5  # Border thickness
            )

            # Add a label for the patient ID
            ax.text(
                start_time + service_duration / 2,
                server_index * 10 + 4.5,
                f"{patient_id}",
                ha="center",
                va="center",
                color="white",
                fontsize=8,
                weight="bold",
            )

    # Configure the chart
    server_count = max(patient["server"] for patient in data)  # Determine the number of servers
    ax.set_yticks([10 * i + 5 for i in range(server_count)])
    ax.set_yticklabels([f"Server {i + 1}" for i in range(server_count)])
    ax.set_xlabel("Time (seconds)")
    ax.set_title("Gantt Chart of Patients")

    # Add a timeline below
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(0.5))
    ax.grid(True, which="both", axis="x", linestyle="--", linewidth=0.5)

    # Display the Gantt chart
    canvas = FigureCanvasTkAgg(fig, gantt_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()

    # Restart and End Buttons
    button_frame = ttk.Frame(result_window)
    button_frame.pack(pady=20)

    restart_button = ttk.Button(button_frame, text="Restart", command=restart_simulation)
    restart_button.pack(side="left", padx=10)

    end_button = ttk.Button(button_frame, text="End", command=end_simulation)
    end_button.pack(side="left", padx=10)


# -------------------------------------- simulation window -------------------------------------------------
def stop_simulation():
    global timer_running
    timer_running = False
    result_button.config(state="normal")


# def show_simulation_screen():
#     global simulation_window, timer_label, result_button
#     simulation_window = tk.Toplevel()
#     simulation_window.title("Running Simulation")
#     simulation_window.geometry("1000x1000")
#
#     # Timer Label
#     timer_label = ttk.Label(simulation_window, text="Time: 0 sec", font=("Helvetica", 14))
#     timer_label.pack(pady=20)
#
#     # Animation Placeholder
#     canvas = tk.Canvas(simulation_window, width=800, height=800, bg="white")
#     canvas.pack(pady=20)
#     canvas.create_text(250, 100, text="simulation running", font=("Helvetica", 16))
#
#     # Buttons
#     stop_button = ttk.Button(simulation_window, text="Stop", command=stop_simulation)
#     stop_button.pack(pady=10)
#
#     result_button = ttk.Button(simulation_window, text="Show Results", command=show_result_screen, state="disabled")
#     result_button.pack(pady=10)
#
#     # Start the timer thread
#     timer_thread = Thread(target=run_timer)
#     timer_thread.start()

def show_simulation_screen():
    global simulation_window, timer_label, result_button, canvas, patient_objects
    simulation_window = tk.Toplevel()
    simulation_window.title("Running Simulation")
    simulation_window.geometry("1000x1000")

    # Timer Label
    timer_label = ttk.Label(simulation_window, text="Time: 0 sec", font=("Helvetica", 14))
    timer_label.pack(pady=20)

    # Animation Canvas
    canvas = tk.Canvas(simulation_window, width=800, height=800, bg="white")
    canvas.pack(pady=20)

    # Draw Start and Exit Areas
    canvas.create_rectangle(50, 350, 150, 450, fill="lightblue", outline="black")
    canvas.create_text(100, 400, text="Start", font=("Helvetica", 12))
    canvas.create_rectangle(650, 350, 750, 450, fill="lightgreen", outline="black")
    canvas.create_text(700, 400, text="Exit", font=("Helvetica", 12))

    # Draw Servers
    server_count = int(server_entry.get())  # Number of servers
    server_positions = []
    for i in range(server_count):
        y = 100 + i * 100
        canvas.create_rectangle(300, y - 25, 400, y + 25, fill="lightyellow", outline="black")
        canvas.create_text(350, y, text=f"Server {i + 1}", font=("Helvetica", 12))
        server_positions.append((350, y))  # Store server center positions

    # Initialize Patients
    patient_objects = []
    for patient in data:
        patient_id = patient["ID"]
        patient_x, patient_y = 100, 400  # Start position
        patient_circle = canvas.create_oval(patient_x - 10, patient_y - 10, patient_x + 10, patient_y + 10, fill="red")
        patient_label = canvas.create_text(patient_x, patient_y, text=str(patient_id), font=("Helvetica", 10))
        patient_objects.append({
            "circle": patient_circle,
            "label": patient_label,
            "data": patient,
            "state": "waiting"  # Possible states: waiting, moving_to_server, at_server, moving_to_exit
        })

    # Buttons
    stop_button = ttk.Button(simulation_window, text="Stop", command=stop_simulation)
    stop_button.pack(pady=10)

    result_button = ttk.Button(simulation_window, text="Show Results", command=show_result_screen, state="disabled")
    result_button.pack(pady=10)

    # Start the timer and animation thread
    timer_thread = Thread(target=run_timer)
    timer_thread.start()
    animation_thread = Thread(target=animate_patients, args=(canvas, server_positions))
    animation_thread.start()


def animate_patients(canvas, server_positions):
    global timer_seconds, timer_running, patient_objects

    animation_speed = 25# Pixels per frame for movement
    while timer_running:
        for patient_obj in patient_objects:
            patient_data = patient_obj["data"]
            patient_circle = patient_obj["circle"]
            patient_label = patient_obj["label"]
            patient_state = patient_obj["state"]

            # Patient properties
            arrival_time = patient_data["arr"]
            service_time = patient_data["exe"]
            server_index = patient_data["server"] - 1
            server_x, server_y = server_positions[server_index]

            current_coords = canvas.coords(patient_circle)
            current_x, current_y = (current_coords[0] + current_coords[2]) // 2, (current_coords[1] + current_coords[3]) // 2

            if patient_state == "waiting" and timer_seconds >= arrival_time:
                patient_obj["state"] = "moving_to_server"

            if patient_state == "moving_to_server":
                # Move towards the assigned server
                if abs(current_x - server_x) > animation_speed:
                    dx = animation_speed if current_x < server_x else -animation_speed
                    canvas.move(patient_circle, dx, 0)
                    canvas.move(patient_label, dx, 0)
                elif abs(current_y - server_y) > animation_speed:
                    dy = animation_speed if current_y < server_y else -animation_speed
                    canvas.move(patient_circle, 0, dy)
                    canvas.move(patient_label, 0, dy)
                else:
                    patient_obj["state"] = "at_server"
                    patient_data["start"] = timer_seconds  # Record start time

            if patient_state == "at_server":
                if timer_seconds >= patient_data["start"] + service_time:
                    patient_obj["state"] = "moving_to_exit"
                    patient_data["end"] = timer_seconds  # Record end time

            if patient_state == "moving_to_exit":
                # Move towards the exit
                exit_x, exit_y = 700, 400
                if abs(current_x - exit_x) > animation_speed:
                    dx = animation_speed if current_x < exit_x else -animation_speed
                    canvas.move(patient_circle, dx, 0)
                    canvas.move(patient_label, dx, 0)
                elif abs(current_y - exit_y) > animation_speed:
                    dy = animation_speed if current_y < exit_y else -animation_speed
                    canvas.move(patient_circle, 0, dy)
                    canvas.move(patient_label, 0, dy)
                else:
                    patient_obj["state"] = "completed"

        time.sleep(0.05)  # Small delay for smooth animation


def run_timer():
    global timer_seconds, timer_running
    while timer_running:
        time.sleep(1)
        timer_seconds += 1
        timer_label.config(text=f"Time: {timer_seconds} sec")


# -------------------------------------------- main window--------------------------------------------

def update_fields(frame, distribution, args_store, field_vars):
    # Clear the current frame contents
    for widget in frame.winfo_children():
        widget.destroy()

    # Helper function to capture field values
    def capture_values(event=None):
        args_store.clear()
        if distribution in ["Exponential", "Poisson"]:
            args_store.append(field_vars["Lambda"].get())
        elif distribution == "Normal":
            args_store.append(field_vars["MU"].get())
            args_store.append(field_vars["SD"].get())
        elif distribution == "Uniform":
            args_store.append(field_vars["LL"].get())
            args_store.append(field_vars["UL"].get())
        elif distribution == "Gamma":
            args_store.append(field_vars["shape"].get())
            args_store.append(field_vars["scale"].get())
        print(f"Captured values for {distribution}: {args_store}")

    # Create fields based on the distribution
    if distribution in ["Exponential", "Poisson"]:
        ttk.Label(frame, text="Lambda (λ):").grid(row=0, column=0, padx=5, pady=5)
        field_vars["Lambda"] = tk.StringVar()
        lambda_entry = ttk.Entry(frame, textvariable=field_vars["Lambda"])
        lambda_entry.grid(row=0, column=1, padx=5, pady=5)
        lambda_entry.bind("<Return>", capture_values)

    elif distribution == "Normal":
        ttk.Label(frame, text="Mean (μ):").grid(row=0, column=0, padx=5, pady=5)
        field_vars["MU"] = tk.StringVar()
        mu_entry = ttk.Entry(frame, textvariable=field_vars["MU"])
        mu_entry.grid(row=0, column=1, padx=5, pady=5)
        mu_entry.bind("<Return>", capture_values)

        ttk.Label(frame, text="Standard Deviation (σ):").grid(row=1, column=0, padx=5, pady=5)
        field_vars["SD"] = tk.StringVar()
        sd_entry = ttk.Entry(frame, textvariable=field_vars["SD"])
        sd_entry.grid(row=1, column=1, padx=5, pady=5)
        sd_entry.bind("<Return>", capture_values)

    elif distribution == "Uniform":
        ttk.Label(frame, text="Lower Limit:").grid(row=0, column=0, padx=5, pady=5)
        field_vars["LL"] = tk.StringVar()
        ll_entry = ttk.Entry(frame, textvariable=field_vars["LL"])
        ll_entry.grid(row=0, column=1, padx=5, pady=5)
        ll_entry.bind("<Return>", capture_values)

        ttk.Label(frame, text="Upper Limit:").grid(row=1, column=0, padx=5, pady=5)
        field_vars["UL"] = tk.StringVar()
        ul_entry = ttk.Entry(frame, textvariable=field_vars["UL"])
        ul_entry.grid(row=1, column=1, padx=5, pady=5)
        ul_entry.bind("<Return>", capture_values)

    elif distribution == "Gamma":
        ttk.Label(frame, text="Shape Parameter (k):").grid(row=0, column=0, padx=5, pady=5)
        field_vars["shape"] = tk.StringVar()
        shape_entry = ttk.Entry(frame, textvariable=field_vars["shape"])
        shape_entry.grid(row=0, column=1, padx=5, pady=5)
        shape_entry.bind("<Return>", capture_values)

        ttk.Label(frame, text="Scale Parameter (θ):").grid(row=1, column=0, padx=5, pady=5)
        field_vars["scale"] = tk.StringVar()
        scale_entry = ttk.Entry(frame, textvariable=field_vars["scale"])
        scale_entry.grid(row=1, column=1, padx=5, pady=5)
        scale_entry.bind("<Return>", capture_values)


def update_inter_arrival_fields(event):
    global ia_args, ia_field_vars
    ia_args = []
    ia_field_vars = {}
    update_fields(inter_arrival_frame, inter_arrival_dropdown.get(), ia_args, ia_field_vars)
    update_simulation_type_label()
    print("Inter-arrival args:", ia_args)


def update_service_time_fields(event):
    global st_args, st_field_vars
    st_args = []
    st_field_vars = {}
    update_fields(service_time_frame, service_time_dropdown.get(), st_args, st_field_vars)
    update_simulation_type_label()
    print("Service time args:", st_args)


def update_simulation_type_label():
    inter_arrival_dist = inter_arrival_dropdown.get()
    service_time_dist = service_time_dropdown.get()

    inter_arrival_type = "M" if inter_arrival_dist in ["Exponential", "Poisson"] else "G"
    service_time_type = "M" if service_time_dist in ["Exponential", "Poisson"] else "G"

    sim_type_label.config(text=f"Simulation Type: {inter_arrival_type}/{service_time_type}/{server_entry.get()}")

def update_server_count(event):
     update_simulation_type_label()


def run_simulation():
    global ia_args, st_args, data
    inter_arrival_dist = inter_arrival_dropdown.get()
    service_time_dist = service_time_dropdown.get()
    server_count = server_entry.get()

    # Pass all parameters to the simulation function
    print(ia_args, st_args)
    data = simulation_main(inter_arrival_dist, service_time_dist, server_count, ia_args, st_args)
    print(data)
    global timer_running, timer_seconds
    timer_running = True
    timer_seconds = 0
    # update_data()
    root.withdraw()
    show_simulation_screen()



# Create the main window
root = tk.Tk()
root.title("Queuing Simulator")
root.geometry("400x550")

# Initialize global variables
MU = tk.StringVar()
Lambda = tk.StringVar()
UL = tk.StringVar()
LL = tk.StringVar()
SD = tk.StringVar()
ia_args = []
st_args = []
args = []

# Title label
title_label = ttk.Label(root, text="Queuing Simulator", font=("Helvetica", 16))
title_label.pack(pady=10)

# Inter-arrival Time Section
inter_arrival_label = ttk.Label(root, text="Inter-Arrival Distribution:")
inter_arrival_label.pack(pady=5)

inter_arrival_dropdown = ttk.Combobox(root, values=["Exponential", "Normal", "Uniform", "Gamma", "Poisson"])
inter_arrival_dropdown.pack(pady=5)
inter_arrival_dropdown.bind("<<ComboboxSelected>>", update_inter_arrival_fields)

inter_arrival_frame = ttk.Frame(root)
inter_arrival_frame.pack(pady=10)

# Service Time Section
service_time_label = ttk.Label(root, text="Service Time Distribution:")
service_time_label.pack(pady=5)

service_time_dropdown = ttk.Combobox(root, values=["Exponential", "Normal", "Uniform", "Gamma", "Poisson"])
service_time_dropdown.pack(pady=5)
service_time_dropdown.bind("<<ComboboxSelected>>", update_service_time_fields)

service_time_frame = ttk.Frame(root)
service_time_frame.pack(pady=10)

# Number of Servers Section
server_label = ttk.Label(root, text="Number of Servers:")
server_label.pack(pady=5)

server_entry = ttk.Entry(root)
server_entry.insert(0, "1")  # Default value is 1 server
server_entry.pack(pady=5)
server_entry.bind("<KeyRelease>", update_server_count)


# Simulation Type Label
sim_type_label = ttk.Label(root, text="Simulation Type: M/M/1", font=("Helvetica", 12))
sim_type_label.pack(pady=10)

# Run Simulation Button
run_button = ttk.Button(root, text="Run Simulation", command=run_simulation)
run_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
