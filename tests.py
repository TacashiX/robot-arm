import arm
import time 
testing = arm.Fenrir(simulate=True) 
testing.home()
time.sleep(1000)
testing.move_arm([50, 100, 20, 50, 180, 45, 90])
time.sleep(1000)

