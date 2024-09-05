import threading
import time
import src.arm as arm
import src.bulletsim as sim

# Global variables
current_mode = None
interrupt_flag = threading.Event()  # Used to signal interruptions

class Robot:
    def __init__(self):
        self.some_variable = 0  # Example variable

    def move_forward(self):
        while not interrupt_flag.is_set():
            self.some_variable += 1
            print(f"Robot is moving forward... Variable: {self.some_variable}")
            time.sleep(1)  # Simulate work being done
        print("Exiting move_forward mode...")

    def move_backward(self):
        while not interrupt_flag.is_set():
            self.some_variable -= 1
            print(f"Robot is moving backward... Variable: {self.some_variable}")
            time.sleep(1)
        print("Exiting move_backward mode...")

    def emergency_stop(self):
        print("Emergency stop initiated!")
        interrupt_flag.set()

    def execute_special_action(self):
        print("Executing special action...")

def execute_mode(robot):
    global current_mode

    # Clear the interrupt flag at the start of a new mode
    interrupt_flag.clear()

    if current_mode == "move_forward":
        robot.move_forward()
    elif current_mode == "move_backward":
        robot.move_backward()
    elif current_mode == "turn_left":
        robot.turn_left()
    elif current_mode == "turn_right":
        robot.turn_right()
    elif current_mode == "emergency_stop":
        robot.emergency_stop()
    else:
        print(f"Unknown mode: {current_mode}")

def main_loop(robot):
    global current_mode

    while True:
        if current_mode:
            execute_mode(robot)
            current_mode = None  # Reset mode after execution
        else:
            print("Robot is idle...")
        
        time.sleep(0.1)  # Adjust sleep time as needed

if __name__ == "__main__":
    bsim = sim.Simulation() 
    robot = arm.Fenrir(bullet=bsim, simulate=True)
    main_loop(robot)

