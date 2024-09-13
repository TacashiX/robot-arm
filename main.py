import threading
import src.xbox as xbox
import time
import src.arm as arm
import src.bulletsim as bulletsim
import logging, sys 
import asyncio
import websockets

log = logging.getLogger(__name__)
interrupt_flag = threading.Event() 
gp_input = [0,0,0,0,0,0,0]

def emergency_stop():
        print("Emergency stop initiated!")
        interrupt_flag.set()

def controller_mode(robot):
    robot.home()
    joy = xbox.Joystick()
    x=0
    y=-0.15
    z=0.2

    while not interrupt_flag.is_set():
        if robot.button_pressed():
            interrupt_flag.set()
            robot.home()
            break
        if joy.Guide() == 1:
            interrupt_flag.set()
            robot.disable_servos()
            break
        if joy.Start() == 1: 
            robot.home() 
            break
        
        if abs(joy.leftX())>0.5: x=robot.apply_limit(x-joy.leftX()/300,-0.3,0.3)
        if abs(joy.leftY())>0.5: y=robot.apply_limit(y-joy.leftY()/300,-0.3,0)
        if abs(joy.rightY())>0.5: z=robot.apply_limit(z+joy.rightY()/300,0,0.4)
        
        joy.leftTrigger()

        st = time.time()
        robot.move_coord([x,y,z])
        end = time.time() 
        log.debug(f"IK Time: {end-st}")
        time.sleep(robot.accel_minmax[0]/1000) #no idea what speed to use yet
    log.info("Exiting controller mode.")

async def ws_controller_mode(robot):
    robot.home()
    global gp_input
    x=0
    y=-0.15
    z=0.2

    while not interrupt_flag.is_set():
        print(f"testing: {gp_input}")
        if robot.button_pressed():
            interrupt_flag.set()
            robot.home()
            break
        if gp_input[6] == 1: #Guide Button 
            interrupt_flag.set()
            robot.disable_servos()
            break
        if gp_input[5] == 1: 
            robot.home() 
            break
        
        if abs(gp_input[0])>0.5: x=robot.apply_limit(x-gp_input[0]/300,-0.3,0.3)
        if abs(gp_input[1])>0.5: y=robot.apply_limit(y+gp_input[1]/300,-0.3,0)
        if abs(gp_input[2])>0.5: z=robot.apply_limit(z-gp_input[2]/300,0,0.4)
        
        st = time.time()
        robot.move_coord([x,y,z])
        end = time.time() 
        log.debug(f"IK Time: {end-st}")
        await asyncio.sleep(robot.accel_minmax[0]/1000) #no idea what speed to use yet
    log.info("Exiting controller mode.")


async def main_loop(robot, s):

    log.info("Entering Main Loop")

    robot.mode = "C"
    while True:
        if robot.mode == "C":
            await ws_controller_mode(robot)
        else:
            if robot.button_pressed():
                interrupt_flag.set()
                robot.home()
            log.debug(f"Robot is idle. {robot.mode=}")
        robot.mode = "F"
        s.update()
        await asyncio.sleep(0.2)

async def handler(websocket, path):
    update_task = asyncio.create_task(update(websocket))
    receive_task = asyncio.create_task(receive(websocket))
    await asyncio.wait([ update_task, receive_task], return_when=asyncio.FIRST_COMPLETED)


async def receive(websocket):
    global gp_input
    async for message in websocket:
        gp_input = [ float(x) for x in message.split(",")]
        print(f"Received: {message}")

async def update(websocket):
    global gp_input
    while True:
        await websocket.send(f"Current trigger: {gp_input[4]}")
        await asyncio.sleep(1/500)

async def start(robot,bsim): 
    start_server = websockets.serve(handler, "localhost", 8765)
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
