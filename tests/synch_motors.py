


def test_move(angles, speed, last_pos): 
    #need to iterate through speed and write positions accordingly... 20ms between calls? 
    #how the fuck do you calc this? Steps=speed/d_ms, step_distance=distance/steps float to int, finish movement after loop. 
    d_ms = 20
    steps = speed // d_ms 

    dist = [(x - y)/steps for x, y in zip(angles, last_pos)]
    print("Starting: ", last_pos)
    for i in range(1,steps): 
        print("Moving:   ", [int(x*i)+y for x,y in zip(dist,last_pos)])
    print("Final:    ", angles)
    #move left over distance

las = [1, 25, 119]
new = [3, 93, 8]
speed = 200
test_move(new, speed, las)

