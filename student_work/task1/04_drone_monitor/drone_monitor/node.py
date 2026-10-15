"""Steps 10-12: the ROS 2 node.

Inheritance: DroneMonitorNode IS a Node.
Composition: it HAS a DroneMonitor (the testable domain logic).
Run inside the internship workspace (ROS 2 Humble + px4_msgs sourced):
    python3 -m drone_monitor.node
"""
import json
from pathlib import Path

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from px4_msgs.msg import VehicleOdometry, BatteryStatus

from .domain import DroneMonitor

CONFIG = Path(__file__).resolve().parent.parent / "config" / "monitor.json"


class DroneMonitorNode(Node):
    def __init__(self):
        super().__init__("drone_monitor")
        config = json.loads(CONFIG.read_text())
        self.monitor = DroneMonitor.from_config(config)
        # PX4 publishes with best-effort reliability
        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                         history=HistoryPolicy.KEEP_LAST, depth=10)
        self.create_subscription(VehicleOdometry, "/fmu/out/vehicle_odometry",
                                 self.odometry_callback, qos)
        self.create_subscription(BatteryStatus, "/fmu/out/battery_status",
                                 self.battery_callback, qos)
        self.create_timer(1.0, self.report)     # log at 1 Hz, not at odometry rate
        self.get_logger().info(f"monitor ready for {self.monitor.state.drone_id}")

    def odometry_callback(self, msg):
        try:
            self.monitor.state.update_position(*msg.position)
        except (TypeError, ValueError) as exc:
            self.get_logger().error(f"Rejected odometry: {exc}")
            return

    def battery_callback(self, msg):
        try:
            self.monitor.state.update_battery(100.0 * msg.remaining)
        except (TypeError, ValueError) as exc:
            self.get_logger().error(f"Rejected battery: {exc}")

    def report(self):
        status = self.monitor.status()
        log = self.get_logger().warn if status != "NOMINAL" else self.get_logger().info
        log(f"{self.monitor.state} -> {status}")


def main():
    rclpy.init()
    node = DroneMonitorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
