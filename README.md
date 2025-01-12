# Simulation of Patient Allocation in Servers

This project simulates the allocation of patients to servers based on a queueing model. It features a GUI created with Tkinter for user interaction and utilizes Python's animation capabilities to visually represent the movement of patients through the system. Additionally, it integrates a `formula.py` module to handle various distribution formulas and a simulation function for computation.

---

## Features

1. **Dynamic Patient Simulation:**
   - Patients are assigned to specific servers based on input data.
   - Visual representation of patients moving from an entry point to their allocated servers, undergoing service, and then exiting.

2. **Configurable Servers and Parameters:**
   - Number of servers and simulation parameters can be customized through the GUI.

3. **Built-in Distribution Formulas:**
   - The `formula.py` file contains formulas for various distributions (e.g., exponential, Poisson).
   - The appropriate formula is selected dynamically based on user input.

4. **Gantt Chart Visualization:**
   - A Gantt chart is generated to visualize server utilization and patient allocation over time.

5. **Real-Time Timer Integration:**
   - A timer syncs the animation with the simulation logic for realistic behavior.

6. **Easy-to-Use GUI:**
   - Tkinter-based interface for entering simulation parameters, starting/stopping the simulation, and viewing results.

---

## Requirements

- **Python 3.7+**
- Libraries:
  - `tkinter`
  - `matplotlib`
  - `random`
  - `threading`
  - `time`
 
# How It Works

### 1. **Input Parameters**

- Use the GUI to specify:
  - Number of servers
  - Patient arrival rate (`lambda`)
  - Service rate (`mu`)
  - Distribution type (selected via `formula.py`).

### 2. **Simulation Process**

- Patients are generated based on the specified distribution.
- Each patient is allocated to a specific server, and their movements are animated.

### 3. **Output**

- **Gantt Chart:** Visualizes server activity.
- **Animation:** Displays patients moving through the system.
- **Results Table:** Shows detailed data for each patient:
  - **ID**
  - **Inter-arrival time**
  - **Arrival time**
  - **Service time**
  - **Start and end times**
  - **Wait time**
  - **Server allocation**

---

# formula.py Overview

The `formula.py` file contains:

- **Distribution Functions:**
  - Exponential distribution
  - Poisson distribution
  - Uniform distribution
- **Simulation Function:**
  - Dynamically selects the appropriate distribution based on Tkinter input.
