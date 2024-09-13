from scipy.optimize import Bounds
import src.arm as arm
import src.xbox as xbox
import pygame
import numpy as np
import src.bulletsim as sim
import time 
import ikpy.chain
import logging, sys
import pybullet as p
import asyncio

logging.basicConfig(stream=sys.stderr, level=logging.WARNING, format="%(levelname)s: %(message)s")
logging.info("testing this")

mysim  = sim.Simulation("model/Fenrir.urdf")
testing = arm.Fenrir(bullet=mysim, simulate=True, urdf_path="model/Fenrir.urdf") 

# # approx movement area x +-0.3 y 0->-0.3 z 0 -> 0.4
# debugIds = []
# debugIds.append(p.addUserDebugParameter("X", -0.3, 0.3))
# debugIds.append(p.addUserDebugParameter("Y", -0.3, 0))
# debugIds.append(p.addUserDebugParameter("Z", 0, 0.45))
#
#
#3rd from last is the gripper rotation in mask
my_chain = ikpy.chain.Chain.from_urdf_file("model/Fenrir.urdf", base_elements=["base_link"],active_links_mask=[False, True, False, False, True, False, True, False, True, False, True, False, True, False, False])


# ik = my_chain.inverse_kinematics([0,0.15,0.2])
ik = [ 0, -1.675516266666666, 0, 0,-0.872664444444444, 0, 0.872664444444444, 0, 1.745329444444444, 0,  0.785398000000000, 0, 1.570796, 0, 0]

#ORIENTATION: 
# axis X and [0,0,1] tells robot to align chains x axis with the absolute z axis (can see the axes in plot) 
# 
orientation_axis = "X"
target_orientation = [0,0,1]

# target_orientation = [[0,0,-1],
#                       [1,0,0],
#                       [1,0,0]]
#


def doIK(coords, initial):
    # ik = my_chain.inverse_kinematics(coords, initial_position=initial)
    r = my_chain.inverse_kinematics(coords, target_orientation, orientation_mode=orientation_axis,initial_position=initial)
    print("Deg pos: ", testing.chain_to_deg(r))
    return r

print("links: -------------------------------")
# print(my_chain.links[1].bounds[0])
print(ik)
print(mysim.translateAngle([84, 40, 140, 100, 180, 90, 0]))
print("fiinish: -------------------------------")
#
testing.home()

# con = widgets.Controller()
# print(con)
#
# async def main():
#     print("bla")
#     global ik
    # LEFT_STICK_X = 0
    # LEFT_STICK_Y = 1
    # RIGHT_STICK_X = 4
    # RIGHT_STICK_Y = 3

# pygame.init()
# pygame.joystick.init()
# jc = pygame.joystick.get_count()
# print("count: ",jc)
# for i in range(pygame.joystick.get_count()):
#     joystick = pygame.joystick.Joystick(i)
#     joystick.init() 
#


def limit(val, min_val, max_val):
    return round(max(min(val, max_val),min_val),3)

# def init_controller():
#     try: 
#         joy = xbox.Joystick()
#         logging.info("Controller initialized")
#         return joy
#     except Exception as e: 
#         raise Exception("No controller connected")
#
# def check_controller_connected(): 
#     try: 
#         return joy.connected()
#     except Exception: 
#         return False
#
# def wait_for_reconnection(): 
#     while True:
#         if check_controller_connected():
#             logging.info("Controller reconnected")
#             return init_controller()
#         logging.info("Waiting for controller to reconnect...")
#         time.sleep(1)
#
def main():
    global ik
    joy = xbox.Joystick()
    # async def main():
    x=0
    y=-0.15
    z=0.2
    while True:
        xp=joy.leftX()
        yp=joy.leftY()
        zp=joy.rightY()
        if abs(xp)>0.5: x=testing.apply_limit(x-xp/300,-0.3,0.3)
        if abs(yp)>0.5: y=testing.apply_limit(y-yp/300,-0.3,0)
        if abs(zp)>0.5: z=testing.apply_limit(z+zp/300,0,0.4)
        # print(f'{x=},{y=},{z=}')

        testing.move_coord([x,y,z])

        # st = time.time()
        # ik = doIK([x,y,z], ik)
        # end = time.time() 
        # # print("Time: ",end-st)
        # rads = [ik[1],ik[4],ik[6],ik[8],ik[10],ik[12],0] #ik12
        # mysim.move_radian(rads)
        #
        #
        #
        time.sleep(1./240.)
            # await asyncio.sleep(0.1)
            
main()
    # except Exception as e:
    #     print(f"Error: {e}")
    #
    # while True: 
    #     try: 
    #         print("trying to refresh")
    #         joy = xbox.Joystick()
    #         if joy.connectStatus:
    #             main()
    #         time.sleep(1)
    #     except Exception as e:
    #         print(f"Error: {e}")
    #     except KeyboardInterrupt:
    #         break
    #
# if __name__ == "__main__":
#     main()
#
#
#
#
# loop = asyncio.get_event_loop()
# loop.create_task(main())

# while True: 
#     targetCoords = [ p.readUserDebugParameter(debugIds[i]) for i in range(len(debugIds)) ]
#     start = time.time()
#     ik = doIK(targetCoords,initial_pos)
#     end = time.time()
#     print("time:",end-start)
#     rads = [ik[1],ik[4],ik[6],ik[8],ik[10],ik[12],0]
#     mysim.move_radian(rads)
#     time.sleep(1./240.)
#

# while True:
#     testing.speed = 15
#     testing.accel_minmax = [20, 100]
#     testing.accel_std_dev = 4 
#     mysim.move_radian([-0.007128,0.05519,-1.461274,0.157288,-0.780446,0.004546,0])
#     testing.move_arm([84, 40, 140, 180, 180, 90, 90])
#     mysim.update()
#
