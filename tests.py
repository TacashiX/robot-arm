import arm
import sim
import time 
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.WARNING, format="%(levelname)s: %(message)s")
logging.info("testing this")
mysim  = sim.Simulation()
testing = arm.Fenrir(bullet=mysim, simulate=True) 
while True:
    testing.speed = 15
    testing.accel_minmax = [20, 100]
    testing.accel_std_dev = 4 
    # testing.home()
    # time.sleep(1)
    testing.move_arm([50, 100, 20, 50, 99, 45, 90])
    # time.sleep(0.5)
    testing.move_arm([84, 40, 140, 100, 180, 90, 90])
    # time.sleep(0.5)
    # testing.move_arm([0, 180, 0, 180, 0, 180, 90])
    # testing.move_arm([180, 0, 180, 0, 180, 0, 90])
    # mysim.update()
    # time.sleep(1./240.)

