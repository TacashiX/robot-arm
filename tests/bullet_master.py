import pybullet as p
import time
import pybullet_data
physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")
# cubeStartPos = [0,0,0]
# cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
p.resetDebugVisualizerCamera( cameraDistance=1.2, cameraYaw=50, cameraPitch=-35, cameraTargetPosition=[-0.31,0.26,-0.29])
robotId = p.loadURDF("ArmAssembly.urdf",[0,0,0]) 
                   # useMaximalCoordinates=1) ## New feature in Pybullet
                   # flags=p.URDF_USE_INERTIA_FROM_FILE)

ordered_joints = []
joint_indices = []
jnames = []
dblist = [] 
for j in range(p.getNumJoints(robotId)):
    info = p.getJointInfo(robotId, j)
    #j 28 excludes useless joint
    if info[2] != p.JOINT_REVOLUTE or j == 28: continue
    jname = info[1].decode("ascii")
    lower, upper = (info[8], info[9])
    jnames.append(jname)
    joint_indices.append(j)
    ordered_joints.append((j,lower, upper)) 

    p.setJointMotorControl2(robotId, j, controlMode=p.VELOCITY_CONTROL, force=0)

#still need to append these to debug list to read later    
for i in range(0, len(ordered_joints)):
    dbval = p.addUserDebugParameter(jnames[i], ordered_joints[i][1], ordered_joints[i][2])
    dblist.append(dbval) 
#read param value 
# p.readUserDebugParameter(sl1)

#need translation function for 0-180 to min-max radian
targetPos = []
while True:
    # p.setJointMotorControl2(bodyUniqueId=robotId, jointIndex=0, controlMode=p.POSITION_CONTROL, targetPosition=p.readUserDebugParameter(sl1), targetVelocity=100, force=100)
    targetPos = [ p.readUserDebugParameter(dblist[i]) for i in range(0,len(dblist)) ]
    p.setJointMotorControlArray(robotId, joint_indices, p.POSITION_CONTROL, targetPositions=targetPos)
    print(targetPos)
    p.stepSimulation()
    time.sleep(1./240.)

cubePos, cubeOrn = p.getBasePositionAndOrientation(robotId)
print(cubePos,cubeOrn)
p.disconnect()

