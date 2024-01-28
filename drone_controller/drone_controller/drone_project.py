import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist, Pose

class DroneController(Node):
    def __init__(self):
        super().__init__('drone_controller')
        self.x = 3.0
        self.y = 1.0
        # Current pose subscriber
        self.gt_pose_sub = self.create_subscription(
            Pose,
            '/drone/gt_pose',
            self.pose_callback,
            1)
        self.gt_pose = None

        # Control command publisher
        self.command_pub = self.create_publisher(Twist, '/drone/cmd_vel', 10)
        
        # Callback for executing a control commands
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Feel free to fill with your code! Add some objects to represent a goal points to achieve

    
    def pose_callback(self, data):
        self.gt_pose = data
        print(f"{data}")

    
    def timer_callback(self):
        print(f"Current pose: {self.gt_pose}")
        msg = Twist()
        msg.linear.z = 6.5
        xpos = 0.0
        ypos = 0.0
        zang = 0.0
        if self.gt_pose is not None:
            xpos = self.gt_pose.position.x
            ypos = self.gt_pose.position.y
        print(xpos)
        print(self.x)
        if xpos > 2.9 and xpos < 3.1:
            self.x = 1.0
        if xpos > 0.9  and xpos < 1.1:
            self.y = 5.0
        if ypos > 4.9 and ypos < 5.1:
            self.x = 3.0
        if xpos > 2.9 and xpos < 3.1:
            self.y = 1.0
        msg.linear.x = self.x
        msg.linear.y = self.y
        print(msg.linear.x)
        self.command_pub.publish(msg)
        print("Published!")



def main(args=None):
    rclpy.init(args=args)

    node = DroneController()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()