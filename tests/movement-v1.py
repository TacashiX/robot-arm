import numpy as np
# from matplotlib import pyplot as plt
import time

def generate_curve(total_time, min_d=20, max_d=50, std_dev_factor=4):
    #calc steps, works in my head. might not work in reality 
    steps = int(total_time / ((min_d + max_d)/2)) 
    #create time vector
    time_vector = np.linspace(0, total_time, steps)
    mean = total_time / 2
    std_dev = total_time / std_dev_factor
    #generate curve 
    curve = max_d * np.exp(-0,5 * ((time_vector - mean) / std_dev) **2)
    #scale curve to respect min and max values and flip 
    curve = np.interp(curve, (curve.min(), curve.max()), (max_d, min_d))
    #return array with int values instead of float
    return curve.astype(int).tolist()

def move_arm(new_pos, curr_pos, speed):
    #calc distances
    dist = np.array([(x - y) for x,y in zip(new_pos, curr_pos)])
    #total_time from max distance
    total_time = speed * abs(max(dist, key=abs))
    #generate curve 
    curve = generate_curve(total_time)
    #need to change this to take into account <0 values 
    step_distance = np.astype(dist/len(curve), int)
    #calc step distance for each motor 
    for ms in curve:
        for i in range(0,len(step_distance)):
            print(i) #so lsp leaves me the fuck alone
            # motor[i].pos = curr_pos[i] + step_distance[i]
            
            #deal with <0 step bullshit 
            if step_distance[i] == 0:
                if curr_pos < new_pos:
                    #motor[i].pos = curr_pos[i] += 1
                    print("shut up lsp")
                elif curr_pos > new_pos:
                    #motor[i].pos = curr_pos[i] -= 1
                    print("shut up lsp")

        curr_pos = curr_pos + step_distance 
        time.sleep(ms)

    #deal with left over shit from float->int | new_pos- (step_distance*len(curve))
    #just move step by step i dont give a fuck i think. no more math. i'll change it if its annoying me 
    leftovers = np.array(new_pos-(step_distance*len(curve)))
    for _ in range(abs(max(leftovers, key=abs))):
        for i in range(0,len(leftovers)):
            if curr_pos[i] > new_pos[i]:
                #motor[i].pos -= 1
                curr_pos[i] -= 1
            elif curr_pos[i] < new_pos[i]:
                #motor[i].pos += 1 
                curr_pos[i] += 1
            
    return 

#Global vars to simulate values that should be part of some class
curr_pos = [] 

'''
changes:
    - probably make duration min/max, std_dev_factor, and speed arm properties you can update.
    - might have to try switching to numpy arrays for everything if calc too slow 
    .

    '''

