import pybullet as p
import time 
import asyncio
import pybullet_data
import pkg_resources
import logging
from pathlib import Path
log = logging.getLogger(__name__)

class Simulation:

    def __init__(self,urdf, directControl=False):
        p.connect(p.GUI) # p.DIRECT for non-graphical
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-10)
        p.loadURDF("plane.urdf")
        p.resetDebugVisualizerCamera(cameraDistance=1.2, cameraYaw=50, cameraPitch=-35, cameraTargetPosition=[-0.31,0.26,-0.29])
        # urdf_file = pkg_resources.resource_filename('robot-arm/model', 'Fenrir.urdf')
        # urdf_file = str(Path("../model/Fenrir.urdf"))
        # print("urdf_file")
        self.robotId = p.loadURDF(urdf, [0,0,0],
                             useFixedBase=1,
                             flags=p.URDF_USE_INERTIA_FROM_FILE)

        self.joints = []
        for j in range(p.getNumJoints(self.robotId)):
            info = p.getJointInfo(self.robotId, j)
            #only grab revolute joints
            if info[2] != p.JOINT_REVOLUTE: continue
            #append joint info [joint index, name, lower limit, upper limit]
            self.joints.append((j, info[1].decode("ascii"), info[8], info[9]))
            
        self.joint_indices = [j[0] for j in self.joints[:-1]]
        log.info("Simulation initialized")
        log.debug(f'Detected joints: {self.joints}')

        #add joints to debug values for display and control
        if directControl:
            self.guiControl()


    def update(self):
            p.stepSimulation()
    
    def translateAngle(self, inputs):
        #arm uses 0-180deg, last value gripper, useless for now but it will move useless j1 gear
        #this will implode if arm list changes size
        rad_positions = []
        for i in range(len(inputs)): 
            normalized_pos  = inputs[i] / 180
            #map normalized position to simulation joint limits
            rad_pos = normalized_pos * (self.joints[i][3] - self.joints[i][2]) + self.joints[i][2]
            rad_positions.append(rad_pos)
        log.debug(f"translated position {inputs} to {rad_positions}")
        return rad_positions

    def updatePosition(self, rawPos):
        pos = self.translateAngle(rawPos)
        p.setJointMotorControlArray(self.robotId, self.joint_indices, p.POSITION_CONTROL, targetPositions=pos) 
        self.update()

    def guiControl(self):
        debugIds = []
        for i in range(len(self.joints)): 
            dbval = p.addUserDebugParameter(self.joints[i][1], self.joints[i][2], self.joints[i][3])
            debugIds.append(dbval)
        
        while True: 
            targetPos = [ p.readUserDebugParameter(debugIds[i]) for i in range(len(debugIds)) ]
            p.setJointMotorControlArray(self.robotId, self.joint_indices, p.POSITION_CONTROL, targetPositions=targetPos)
            p.stepSimulation()
            time.sleep(1./240.)
        
            

    def move_radian(self, radian_pos):
        p.setJointMotorControlArray(self.robotId, self.joint_indices, p.POSITION_CONTROL, targetPositions=radian_pos) 
        self.update()


    async def update_loop(self):
        while True: 
            self.update()
            await asyncio.sleep(1./240.)

