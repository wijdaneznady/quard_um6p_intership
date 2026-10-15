"""Lecture 2 (14 Sep) - Python refresher for robotics.

Every slide example from part 1, written as small runnable exercises.
Run: python3 refresher.py      (needs numpy; see requirements.txt)
"""
import csv
import json
import logging
import math
from pathlib import Path

import numpy as np

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
log = logging.getLogger("refresher")
HERE = Path(__file__).parent


# ---- 1. Variables and types: units in the names -------------------------------
def ex_variables():
    altitude_m = 4.0          # float
    detection_count = 3       # int
    mission_active = True     # bool
    target_label = "inspection_car"
    latest_position = None    # not available yet
    log.info("variables: %s m, %d detections, active=%s, target=%s, position=%s",
             altitude_m, detection_count, mission_active, target_label, latest_position)


# ---- 2. Containers: tuple = one record, list = history, dict = named fields ----
def ex_containers():
    ranges_m = [2.4, 2.1, 1.9]                 # history that grows
    position_ned = (3.0, -1.0, -4.0)           # one fixed position
    state = {"mode": "ORBIT", "battery_pct": 78.0}
    ranges_m.append(1.7)
    north, east, down = position_ned           # unpacking
    log.info("latest range %.1f m, last three %s, altitude %.1f m, mode %s",
             ranges_m[-1], ranges_m[-3:], -down, state["mode"])


# ---- 3. Mutability: alias vs copy ---------------------------------------------
def ex_mutability():
    measurements = [1.0, 2.0]
    alias = measurements
    alias.append(3.0)                          # also changes measurements
    copy = measurements.copy()
    copy.append(99.0)                          # does not change measurements
    assert measurements == [1.0, 2.0, 3.0]
    log.info("alias changed the original, copy did not: %s / %s", measurements, copy)


# ---- 4. Conditions, for, while with an exit -----------------------------------
def mission_status(latest_position, altitude_m, max_altitude_m):
    if latest_position is None:
        return "waiting_for_odometry"
    elif altitude_m > max_altitude_m:
        return "limit_exceeded"
    return "ready"


def count_label(detections, label):
    count = 0
    for name in detections:
        if name == label:
            count += 1
    return count


def ex_control_flow():
    log.info("status: %s | %s | %s",
             mission_status(None, 0, 10), mission_status((0, 0, -12), 12, 10),
             mission_status((0, 0, -8), 8, 10))
    log.info("cars detected: %d", count_label(["car", "person", "car"], "car"))
    attempt = 0
    while attempt < 3:                         # always a stop condition
        attempt += 1
        log.info("connection attempt %d", attempt)


# ---- 5. Functions with a clear contract ---------------------------------------
def planar_distance_m(x1: float, y1: float, x2: float, y2: float) -> float:
    """Return the 2D Euclidean distance in metres."""
    return math.hypot(x2 - x1, y2 - y1)


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


# ---- 6. Exceptions: validate close to the source, catch only what you expect ---
def validate_altitude(altitude_m, max_altitude_m):
    if not 0.5 <= altitude_m <= max_altitude_m:
        raise ValueError(f"altitude_m={altitude_m} outside [0.5, {max_altitude_m}]")
    return altitude_m


def parse_altitude(raw):
    try:
        return float(raw)
    except ValueError as exc:
        log.error("Invalid altitude %r: %s", raw, exc)
        return None


# ---- 7. Files: JSON configuration in, CSV evidence out ------------------------
def load_mission(path=HERE / "mission.json"):
    with Path(path).open("r", encoding="utf-8") as f:
        cfg = json.load(f)
    radius_m = float(cfg["radius_m"])
    altitude_m = validate_altitude(float(cfg["altitude_m"]), float(cfg["max_altitude_m"]))
    return {"target": cfg["target_label"], "radius_m": radius_m, "altitude_m": altitude_m}


def write_telemetry(rows, path=HERE / "telemetry.csv"):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["time_s", "altitude_m"])
        w.writerows(rows)
    return path


# ---- 8. NumPy: shape/dtype, vectorized filtering, tracking error --------------
def ex_numpy():
    image = np.zeros((480, 640, 3), dtype=np.uint8)
    log.info("image shape %s (height, width, channels), dtype %s", image.shape, image.dtype)
    measurements_m = np.array([2.4, 2.1, -1.0, 1.9, 2.2])     # one invalid sample
    valid = measurements_m > 0.0
    filtered = measurements_m[valid]
    log.info("mean of valid ranges %.2f m (rejected %d sample)", filtered.mean(), (~valid).sum())
    desired_m = np.array([5.0, 0.0, -4.0])
    measured_m = np.array([4.7, 0.2, -3.9])
    error_m = float(np.linalg.norm(desired_m - measured_m))
    log.info("tracking error %.3f m", error_m)
    # filter detections before they enter the system: keep confidence >= 0.5
    conf = np.array([0.91, 0.32, 0.77, 0.12])
    labels = np.array(["car", "car", "person", "car"])
    keep = conf >= 0.5
    log.info("kept detections: %s", [(str(l), float(c)) for l, c in zip(labels[keep], conf[keep])])
    return error_m


def main():
    ex_variables()
    ex_containers()
    ex_mutability()
    ex_control_flow()
    log.info("distance (0,0)->(3,4) = %.1f m, clamp(12, 0, 10) = %.0f",
             planar_distance_m(0, 0, 3, 4), clamp(12, 0, 10))
    parse_altitude("four metres")              # logged error, no crash
    try:
        validate_altitude(15.0, 10.0)
    except ValueError as exc:
        log.warning("rejected parameter: %s", exc)
    log.info("mission config: %s", load_mission())
    log.info("telemetry written to %s", write_telemetry([[0.0, 1.2], [0.5, 2.6], [1.0, 4.0]]).name)
    ex_numpy()


if __name__ == "__main__":
    main()
