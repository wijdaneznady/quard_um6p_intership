"""Run the monitor on a simulated flight without ROS 2.

Shows several independent objects (step 8), the configuration (step 13),
CSV evidence and a NumPy tracking error. Usage: python3 demo_offline.py
"""
import csv
import json
import logging
from pathlib import Path

import numpy as np

from drone_monitor.domain import DroneMonitor, Sample

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
HERE = Path(__file__).parent


def simulated_flight():
    """Take-off to 4 m, hold, battery draining from 100 % to 20 %."""
    for k in range(41):
        t = 0.5 * k
        alt = min(4.0, 0.4 * t)
        yield Sample(t, 0.1 * t, 0.0, -alt, 100.0 - 2.0 * k)


def main():
    config = json.loads((HERE / "config" / "monitor.json").read_text())
    uav_1 = DroneMonitor.from_config(config)
    uav_2 = DroneMonitor("uav_2")                     # second, independent object
    uav_2.state.update_position(-3.0, 0.5, -2.0)

    out = HERE / "monitor_log.csv"
    desired = []
    measured = []
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time_s", "altitude_m", "battery_pct", "status"])
        last = None
        for s in simulated_flight():
            uav_1.state.update_position(s.north_m, s.east_m, s.down_m, s.time_s)
            uav_1.state.update_battery(s.battery_pct)
            uav_1.state.set_mode("TAKEOFF" if -s.down_m < 4.0 else "OFFBOARD")
            status = uav_1.status()
            w.writerow([s.time_s, round(uav_1.state.altitude_m, 2), s.battery_pct, status])
            if status != last:                         # log only state changes
                logging.info("t=%4.1f s  %s -> %s", s.time_s, uav_1.state, status)
                last = status
            desired.append([s.north_m, 0.0, -4.0])
            measured.append(uav_1.state.position_ned_m)

    err = np.linalg.norm(np.array(desired) - np.array(measured), axis=1)
    logging.info("distance to the 4 m target: %.2f m at start, %.2f m once at altitude", err[0], err[-1])
    logging.info("independent objects: %s | %s", uav_1.state, uav_2.state)
    logging.info("evidence written to %s", out.name)


if __name__ == "__main__":
    main()
