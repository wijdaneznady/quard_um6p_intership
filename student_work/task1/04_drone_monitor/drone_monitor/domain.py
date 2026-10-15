"""Lecture 2, part 2 - End-to-end OOP mini-project: from raw telemetry to a drone monitor.

Domain classes only: no ROS 2 import, so they can be tested alone (step 14).
"""
from dataclasses import dataclass

FLIGHT_MODES = ("IDLE", "TAKEOFF", "OFFBOARD", "LAND", "FAILSAFE")


class DroneState:
    """Latest estimated state of one drone (steps 1-8)."""

    def __init__(self, drone_id: str):
        if not drone_id:
            raise ValueError("drone_id must not be empty")
        self.drone_id = drone_id
        self._position_ned_m = (0.0, 0.0, 0.0)   # internal: North, East, Down (step 5)
        self.battery_pct = 100.0
        self.flight_mode = "IDLE"
        self.last_update_s = None

    def update_position(self, north_m, east_m, down_m, time_s=None):
        """Store a new NED position (step 3). Rejects values that are not numbers."""
        self._position_ned_m = (float(north_m), float(east_m), float(down_m))
        self.last_update_s = time_s

    def update_battery(self, battery_pct):
        """Battery must stay in [0, 100] (step 4)."""
        value = float(battery_pct)
        if not 0.0 <= value <= 100.0:
            raise ValueError("battery_pct outside [0, 100]")
        self.battery_pct = value

    def set_mode(self, mode: str):
        if mode not in FLIGHT_MODES:
            raise ValueError(f"unknown flight mode {mode!r}")
        self.flight_mode = mode

    @property
    def position_ned_m(self):
        return self._position_ned_m

    @property
    def altitude_m(self):
        """Down is positive towards the ground, so altitude = -down (step 6)."""
        return -self._position_ned_m[2]

    def __str__(self):  # step 7
        return (f"{self.drone_id}: mode={self.flight_mode}, "
                f"altitude={self.altitude_m:.2f} m, battery={self.battery_pct:.1f}%")


class BatteryMonitor:
    """Decides if the battery is low; it never commands the drone (step 9)."""

    def __init__(self, warning_threshold_pct=25.0):
        threshold = float(warning_threshold_pct)
        if not 0.0 <= threshold <= 100.0:
            raise ValueError("invalid warning threshold")
        self.warning_threshold_pct = threshold

    def is_low(self, battery_pct):
        return float(battery_pct) <= self.warning_threshold_pct


class AltitudeMonitor:
    """Extra component (same pattern): altitude must stay inside the mission limit."""

    def __init__(self, max_altitude_m=10.0):
        self._max_altitude_m = float(max_altitude_m)

    def within_limit(self, altitude_m):
        return 0.0 <= altitude_m <= self._max_altitude_m


class DroneMonitor:
    """Composition: a monitor HAS a state, a battery monitor and an altitude monitor."""

    def __init__(self, drone_id, battery_warning_pct=25.0, max_altitude_m=10.0):
        self.state = DroneState(drone_id)
        self.battery_monitor = BatteryMonitor(battery_warning_pct)
        self.altitude_monitor = AltitudeMonitor(max_altitude_m)

    def status(self):
        if self.battery_monitor.is_low(self.state.battery_pct):
            return "LOW_BATTERY"
        if not self.altitude_monitor.within_limit(self.state.altitude_m):
            return "ALTITUDE_LIMIT"
        return "NOMINAL"

    @classmethod
    def from_config(cls, config: dict):
        """Step 13: values come from configuration, the class only validates them."""
        return cls(config["drone_id"],
                   config.get("battery_warning_pct", 25.0),
                   config.get("max_altitude_m", 10.0))


@dataclass
class Sample:
    """One telemetry record, used by the offline demo."""
    time_s: float
    north_m: float
    east_m: float
    down_m: float
    battery_pct: float
