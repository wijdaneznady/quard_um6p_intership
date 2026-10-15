"""Step 14: domain logic tested without ROS 2.   Run: python3 -m pytest -q"""
import pytest

from drone_monitor.domain import BatteryMonitor, DroneMonitor, DroneState


def test_altitude_from_ned_position():
    state = DroneState("test_uav")
    state.update_position(1.0, 2.0, -4.5)
    assert state.altitude_m == 4.5


def test_invalid_battery_is_rejected():
    state = DroneState("test_uav")
    with pytest.raises(ValueError):
        state.update_battery(120.0)
    assert state.battery_pct == 100.0          # the bad value was not stored


def test_non_numeric_position_is_rejected():
    state = DroneState("test_uav")
    with pytest.raises(ValueError):
        state.update_position("north", 0, 0)


def test_unknown_mode_is_rejected():
    with pytest.raises(ValueError):
        DroneState("uav").set_mode("FLYING_FAST")


def test_objects_are_independent():
    a, b = DroneState("a"), DroneState("b")
    a.update_position(0, 0, -4)
    b.update_position(0, 0, -2)
    assert (a.altitude_m, b.altitude_m) == (4.0, 2.0)


def test_battery_monitor_threshold():
    m = BatteryMonitor(25.0)
    assert m.is_low(25.0) and m.is_low(10.0) and not m.is_low(60.0)
    with pytest.raises(ValueError):
        BatteryMonitor(150.0)


def test_drone_monitor_status():
    mon = DroneMonitor("uav", battery_warning_pct=25.0, max_altitude_m=10.0)
    mon.state.update_position(0, 0, -4)
    assert mon.status() == "NOMINAL"
    mon.state.update_position(0, 0, -12)
    assert mon.status() == "ALTITUDE_LIMIT"
    mon.state.update_battery(20.0)
    assert mon.status() == "LOW_BATTERY"


def test_from_config():
    mon = DroneMonitor.from_config({"drone_id": "uav_9", "battery_warning_pct": 30})
    assert mon.state.drone_id == "uav_9"
    assert mon.battery_monitor.warning_threshold_pct == 30.0


def test_str_is_readable():
    s = DroneState("uav_1")
    s.update_position(0, 0, -4)
    assert str(s) == "uav_1: mode=IDLE, altitude=4.00 m, battery=100.0%"
