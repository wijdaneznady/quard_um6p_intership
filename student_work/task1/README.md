# Task 1 – Course activities and mini-projects

Wijdane Znady · Team 2 · UM6P Vanguard, Track 2

All exercises and mini-projects from the two lectures, solved. Every file only touches `student_work/`; nothing in PX4, Gazebo or ROS 2 is changed.

## Lecture 1 – The Foundation: Ubuntu, terminal and Git (10 Sep)

| # | Exercise (slide) | Solution |
|---|---|---|
| 1 | Terminal Sandbox, Mission 1: workspace `drone_ws` (67) | `01_bash/terminal_missions.sh` |
| 2 | Mission 2: `config.env` with `ROS_DOMAIN_ID=42`, backup (68) | `01_bash/terminal_missions.sh` |
| 3 | Mission 3: rename to `archive`, `grep`, clean-up (69) | `01_bash/terminal_missions.sh` |
| 4 | Project exercises: navigate, `mkdir/touch`, `cp/mv`, safe `rm`, `cat/head/tail`, evidence `run.log`, `find/grep`, `&&`, environment, permissions, processes (42–60) | `01_bash/project_exercises.sh` |
| 5 | Git small safe change + `git status/diff` (85–86) | `02_git/git_practice.sh` |
| 6 | End-to-end Git practice (104) and live demonstration, steps 1–17 on a fork, branch `docs/git-practice` (107–126) | `02_git/git_practice.sh` |
| 7 | **Student Challenge:** branch `docs/installation-observations` with Ubuntu version, ROS 2 distribution, installation phase and one verified command (133) | `02_git/student_challenge.sh` |

## Lecture 2 – Python for robotics (14 Sep)

| # | Exercise (slides) | Solution |
|---|---|---|
| 8 | Refresher: variables with units, containers, slicing, copies, conditions, loops with an exit, functions, exceptions, JSON config, CSV evidence, NumPy (shape, filtering, tracking error), logging (6–45) | `03_python_refresher/refresher.py` + `mission.json` |
| 9 | Virtual environment and dependency file (31–33) | `03_python_refresher/requirements.txt` |
| 10 | **Mini-project: end-to-end OOP drone monitor**, steps 1–14 (51–69): `DroneState`, validation, property, `__str__`, independent objects, composition (`BatteryMonitor`, `DroneMonitor`), inheritance (`DroneMonitorNode(Node)`), subscription, error handling, configuration, tests | `04_drone_monitor/` |
| 11 | Knowledge checks (47, 72) and reading a controller file (70) | `ANSWERS.md` |

## How to run

```bash
# Lecture 1
bash 01_bash/terminal_missions.sh                  # safe: runs in a temporary folder
bash 01_bash/project_exercises.sh                  # writes student_work/run.log in the repository
GH_USER=<your-github-username> bash 02_git/git_practice.sh
bash 02_git/student_challenge.sh                   # from inside your fork

# Lecture 2
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r 03_python_refresher/requirements.txt
python 03_python_refresher/refresher.py
cd 04_drone_monitor
python -m pytest -q                                # 9 tests, no ROS 2 needed
python demo_offline.py                             # simulated flight -> monitor_log.csv
# with the simulation running and the ROS 2 workspace sourced:
python3 -m drone_monitor.node
```

## Results

- `refresher.py` runs every lecture example; the invalid altitude is logged and the out-of-range parameter is rejected, without crashing.
- `04_drone_monitor`: **9/9 tests pass**. The offline demo switches from `NOMINAL` to `LOW_BATTERY` when the battery reaches 24 % (threshold 25 %), and two drones keep independent states.
- The ROS 2 node subscribes to `/fmu/out/vehicle_odometry` and `/fmu/out/battery_status` (best-effort QoS, as PX4 publishes) and logs the status once per second.
