import functools
import threading
from functools import partial
import src.xbox as xbox
import time
import src.arm as arm
import src.bulletsim as bulletsim
import logging, sys 
import asyncio
import websockets
import json

log = logging.getLogger(__name__)
interrupt_flag = threading.Event() 
gp_input = [0,0,0,0,0,0,0]

async def ws_controller_mode(robot):
    robot.home()
    global gp_input
    x=0
    y=-0.15
    z=0.2

    while not interrupt_flag.is_set():
        # print(f"testing: {gp_input}")
        if robot.button_pressed():
            robot.home()
            robot.mode = "M"
            break
        if gp_input[6] == 1: #Guide Button 
            robot.disable_servos()
            robot.mode = "M"
            break
        if gp_input[5] == 1: 
            x, y, z = 0,-0.15,0.2
            robot.move_coord([x,y,z],smooth=True)
            #continuing here stops updating the controller and gets stuck in a loop 
            gp_input[5] = 0
            continue

        #Main axes
        if abs(gp_input[0])>0.5: x=robot.apply_limit(x-gp_input[0]/300,-0.3,0.3)
        if abs(gp_input[1])>0.5: y=robot.apply_limit(y+gp_input[1]/300,-0.3,0)
        if abs(gp_input[2])>0.5: z=robot.apply_limit(z-gp_input[2]/300,0,0.4)
        
        #gripper steps in 2-5 range for now 
        if gp_input[3]>0.4: robot.grip(int(gp_input[3]/2*10))
        if gp_input[4]>0.4: robot.grip(-int(gp_input[4]/2*10))

        st = time.time()
        if robot.coords != [x,y,z]:
            robot.move_coord([x,y,z])
        end = time.time() 
        log.debug(f"IK Time: {end-st}")
        await asyncio.sleep(robot.accel_minmax[0]/1000) #no idea what speed to use yet
    log.info("Exiting controller mode.")
    robot.mode = "M"


async def main_loop(robot, s):
    global gp_input
    robot.mode = "C"
    while not interrupt_flag.isSet():
        if robot.mode == "C":
            await ws_controller_mode(robot)
        else:
            if robot.button_pressed():
                robot.home()
            if gp_input[6] == 1: #Guide Button 
                robot.mode = "C"
            log.info(f"Robot is idle. {robot.mode=}")
        s.update() #only for simulation
        await asyncio.sleep(0.1)

async def handler(websocket, r):
    update_task = asyncio.create_task(update(websocket,r))
    receive_task = asyncio.create_task(receive(websocket))
    await asyncio.wait([ update_task, receive_task], return_when=asyncio.FIRST_COMPLETED)


async def receive(websocket):
    global gp_input
    async for message in websocket:
        gp_input = [ float(x) for x in message.split(",")]
        # print(f"Received: {message}")

async def update(websocket,r):
    while True:
        # await websocket.send(f"Servo Angles: {r.curr_pos}\n\rPos: {r.coords}\nGripper: {r.gripper_pos}")
        await websocket.send(json.dumps([r.curr_pos, r.coords,r.gripper_pos]))
        await asyncio.sleep(1/500) # don't have to update alot

async def start(robot,bsim): 
    passing_handler = functools.partial(handler, r=robot)
    start_server = websockets.serve(passing_handler, "localhost", 8765)
    await asyncio.gather(start_server, main_loop(robot,bsim))

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(levelname)s: %(message)s")
    bsim = bulletsim.Simulation("model/Fenrir.urdf") 
    robot = arm.Fenrir(bullet=bsim, simulate=True, urdf_path="model/Fenrir.urdf")

    asyncio.get_event_loop().run_until_complete(start(robot,bsim))

    # main_loop(robot,bsim)
    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()
    #
