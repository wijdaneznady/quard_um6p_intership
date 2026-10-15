# Task 1 – Knowledge checks and explanations

Wijdane Znady · Team 2 · UM6P Vanguard, Track 2

## Lecture 1 – Ubuntu, terminal and Git (10 September)

**Why Ubuntu?** PX4 SITL, Gazebo and ROS 2 Humble are developed and tested on Ubuntu 22.04. Running them there avoids compatibility problems, and the terminal gives direct control over processes, files and logs.

**Absolute vs relative path.** `/home/student/quard_um6p_intership/gazebo/models` always points to the same place. `gazebo/models` depends on the current directory, which is why `pwd` should be checked first.

**Why `&&`?** `cd ~/quard_um6p_intership && source config/project.env` only runs the second command if the first succeeds, so nothing runs from the wrong directory.

**Why `rm` is dangerous.** There is no undo from the terminal. Before deleting: `pwd`, `ls` the target, check the exact path, and practise in a throw-away folder.

**`>` vs `>>`.** `>` replaces the file, `>>` appends to it. Evidence logs are built with `>>`.

**Environment variables.** Named values read by programs (e.g. `ROS_DOMAIN_ID`, `PX4_GZ_MODEL`). `export` makes a value visible to child processes; `source config/project.env` applies a whole configuration to the current shell.

**Git states.** untracked → modified → staged (`git add`) → committed (`git commit`) → published (`git push`). A saved file is not published until it has been staged, committed and pushed.

**Why a branch and a fork?** The fork is a personal copy, the branch isolates one change. The supervisor's `main` is never modified by a classroom exercise.

**Why not `git add .`?** It can stage logs, bags, build folders or secrets. Stage only the intended file and check with `git diff --staged`.

**Rejected push.** Collect evidence (`git status`, `git branch`, `git remote -v`), `git pull`, resolve conflicts, push again. Never `git push --force` on a shared branch.

## Lecture 2 – Python for robotics (14 September)

**Which container for a position, a measurement history and a named configuration?** A tuple for one position (fixed record), a list for a history (grows), a dictionary for configuration (named fields).

**Why separate a distance function from ROS 2 publication?** The calculation can then be tested alone, reused in other nodes, and a bug in the maths is not mixed with a communication problem.

**Class vs object.** The class is the blueprint (`DroneState`), the object is one instance (`uav_1`). Two objects share the code but keep their own values.

**Why does a ROS 2 Python node inherit from `Node`?** Because it *is* a node: inheritance gives it publishers, subscriptions, timers, parameters and the logger.

**When to catch an exception, when to stop?** Catch it when there is a meaningful response (skip one bad odometry message and log it). Let it stop the program when continuing would be unsafe or meaningless (invalid mission parameters at start-up).

**Why a virtual environment and `python -m pip`?** The environment isolates project packages from the system Python. `python -m pip` installs into the interpreter actually in use. (The ROS 2 Python packages themselves stay in the system environment, as documented by the internship.)

**What do NumPy `shape` and `dtype` tell us?** `shape` is the size along each axis (an image is `(480, 640, 3)` = height, width, channels). `dtype` is the number type (`uint8` = 0–255), which changes the range and the arithmetic.

**Why is an AI detection not a flight command?** A detection is an observation with a confidence and possible errors. It must be filtered, geo-referenced and checked by the mission logic; the flight controller keeps control and the safety rules.

### OOP knowledge check

- **Why does every method receive `self`?** It is the object the method works on, so `self.battery_pct` means the battery of *this* drone.
- **What goes in `__init__`?** Every attribute the object needs, in a valid starting state (position `(0, 0, 0)`, battery 100 %, mode `IDLE`).
- **Property or method?** A property for a cheap value derived from the state (`altitude_m`). A method for an action or heavy work (`update_position`).
- **Inheritance vs composition in `DroneMonitorNode`.** It *is a* `Node` (inheritance) and *has a* `DroneMonitor` (composition).
- **Where to validate telemetry?** In the object that stores it (`update_battery` rejects 120 %), close to the source.
- **Why test without ROS 2?** The tests run in a fraction of a second, without a simulator, and failures point directly to the logic.
- **How does a state-machine class help?** Each mission phase is explicit (IDLE → TAKEOFF → OFFBOARD → LAND), transitions are checked in one place, and logs show exactly where a mission stopped.

### Reading a robotics controller (applied to our survey controller)

1. **Responsibility:** fly the lawnmower survey in offboard mode and land.
2. **Persistent state:** mission parameters from `survey.yaml` (height, speed, lines, tolerances), the last odometry and vehicle status, the current mission state and target point.
3. **Interfaces:** publishes `offboard_control_mode` and `trajectory_setpoint` (20 Hz) and `vehicle_command` (arm, mode, land); subscribes to `vehicle_odometry` and `vehicle_status`; services `start` and `abort`.
4. **One event traced:** timer tick → read last position → if closer than 2 m to the target, move the target forward → publish the setpoint.
5. **Safety:** the target waits if the drone is behind; the mission stops if the error exceeds 6 m or the state lasts too long; states and errors are logged.
