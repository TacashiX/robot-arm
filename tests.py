import arm
import sim
import time 

mysim  = sim.Simulation()
testing = arm.Fenrir(mysim, simulate=True) 

while True:
    testing.speed = 3000
    # testing.home()
    # time.sleep(1)
    testing.move_arm([50, 100, 20, 50, 99, 45, 90])
    # time.sleep(0.5)
    testing.move_arm([84, 40, 140, 100, 180, 90, 90])
    # time.sleep(0.5)

    testing.move_arm([0, 180, 0, 180, 0, 180, 90])
    testing.move_arm([180, 0, 180, 0, 180, 0, 90])
    # mysim.update()
    # time.sleep(1./240.)

