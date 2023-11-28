import tdmclient.notebook

await tdmclient.notebook.start() 
import time
import math


state = "begin"
target = 0
xi=0
yi=0
xt=0
yt=2
xnt=-1
ynt=2
xnnt=-2
ynnt=2
position_i = [xi,yi]
position = position_i
xp=[xt,xnt,xnnt]
yp=[yt,ynt,ynnt]
path = [xp,yp]
x_s=[xi+1,xi-1]
y_s=[yi+2,yi+2]
special_cases = [x_s,y_s]
i = 1



def switch_sens(sens):
    if(sens == 1):
        sens = 2
    else:
        sens = 1
    return sens


def rotate_robot(angle_degrees, rotation_speed, carre):
    # Convertir l'angle en radians
    angle_radians = math.radians(angle_degrees)

    # Calculer la distance que chaque roue doit parcourir
    wheel_distance = 5  # Remplacez par la distance réelle entre les roues de votre robot
    wheel_circumference = 2 * math.pi * (wheel_distance / 2)
    distance_to_travel = (angle_radians / (2 * math.pi)) * wheel_circumference
    # Ajuster la vitesse des moteurs pour faire tourner le robot
    if (carre == 1): 
        motor_speed = rotation_speed
        motor_left_target = motor_speed + 7
        motor_right_target = -motor_speed 
    if (carre == 2):
        motor_speed = rotation_speed
        motor_left_target = -motor_speed
        motor_right_target = motor_speed + 7 
    # Inverser la vitesse du moteur droit pour tourner

    # Définir les variables des moteurs
    set_var(motor_left_target=motor_left_target, motor_right_target=motor_right_target)
    time.sleep(2.2)
    # Attendez que le robot ait tourné la distance souhaitée
    time.sleep(distance_to_travel / motor_speed)
    
def forward_robot(motor_speed):
    motor_left_target = motor_speed
    motor_right_target = motor_speed
    set_var(motor_left_target=motor_left_target, motor_right_target=motor_right_target) 
    time.sleep(3)
    
def beginning_robot(motor_speed):
    motor_left_target = motor_speed
    motor_right_target = motor_speed
    set_var(motor_left_target=motor_left_target, motor_right_target=motor_right_target)
    
def local_nav():
    global prox_horizontal, state, carre, path, position_i, special_cases, case
    
    w_l = [0,  20, -20, -20, 0, 0, 0]
    w_r = [0, -20, -20,  20, 0, 0,  0]
    # Scale factors for sensors and constant factor
    sensor_scale = 200
    
    
    y = [0,0]
    x = [0,0,0,0,0,0,0]
    proxi,=get_var("prox_horizontal")
        
    for i in range(len(x)):
        # Get and scale inputs
        x[i] = proxi[i] // sensor_scale
        if (x[2] > 20):
            state = obstacle
          
    if(state == begin):
        #print("avance")
        beginning_robot(100)
    if(state == obstacle):
        print("stop")
        # le robot s'arrête devant l'obstacle pendant 2 secondes 
        forward_robot(0)
        print("1") 
        # ils ont le même x donc le global path est derrière l'obstacle
        if (position[0] == path[0][0]): 
            for i in range(len(path)):
                #for j in (len(special_cases)):
                if(path[0][i]==special_cases[0][0]):
                    target = 1
                if(path[0][i]==special_cases[0][1]):
                    target = 2
            state = obstacle_derriere
        # la target est à gauche de l'obstacle 
        if (position[0] > path[0][0]): 
            state = obstacle_left
        # la target est à droite de l'obstacle 
        if (position[0] < path[0][0]): 
            state = obstacle_right
    if(state == obstacle_derriere):
        print("target derrière obstacle")
        if (target == 1):
            print("obstacle à droite")
            sens = 1
        else :
            print("obstacle à gauche") 
            sens = 2
        rotate_robot(90,100,sens)
        forward_robot(100)
        rotate_robot(90,100,switch_sens(sens))
        forward_robot(100)
        time.sleep(5)
        if(target == 0):
            print("path est bien derriere")
            rotate_robot(90,100,switch_sens(sens))
            forward_robot(100)
            rotate_robot(90,100,sens)
            state = 5
        else : 
            i+=1
            state = 5
    if(state == obstacle_left):
        print("target à gauche")
        rotate_robot(90,100,2)
        forward_robot(100)
        rotate_robot(90,100,1)
        forward_robot(100)
        state = 5
    if(state == obstacle_right):
        print("target à droite")
        rotate_robot(90,100,1)
        print("jai tourné")
        forward_robot(100)
        print("jai avancé")
        rotate_robot(90,100,2)
        print("jai tourné")
        forward_robot(100)
        print("c'est fini")
        state = next_step
    if(state == next_step):
        #if(path[0][1] == path[0][0]):
        if(path[0][i] == path[0][0]):
            print("je fais rien")
            state = end
        if(path[0][0] > path[0][i]):
            rotate_robot(90,100,2)
            state = end
        if(path[0][0] < path[0][i]):
            print("je dois tourner")
            rotate_robot(90,100,1)
            state = end
    if(state == end):
        print("stop")
        forward_robot(0)
        
           
    
start = 0 
while start==0: 
    local_nav()

