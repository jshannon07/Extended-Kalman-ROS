"""

Extended kalman filter (EKF) localization sample

author: Atsushi Sakai (@Atsushi_twi)

modified by Ben Ware and Allen Spain

"""
import numpy as np
import math
import matplotlib.pyplot as plt
import random

from geometry_msgs.msg import Pose
from std_msgs.msg import String
from geometry_msgs.msg import Twist

# # Estimation parameter of EKF
Q = np.diag([0.1, 0.1, 0.1, 0.1])**2
R = np.diag([1.0, 1.0])**2
DT = 1  # Descrete time steps
SIM_TIME = 100

def get_rand(): return random.choice([1,1,1,0])

show_animation = True

## Assumptions and notes:
# Robot sensor noise is d by adding to each coordinate: np.random.randn()//2
# Input noise is simulated with a 25% chance to "slip" and not move.
# Robot does not have prior knowledge of chance of "slipping"
# Robot does not assume it is confined to a descrete domain.
# Simulated input ommits [0,-1] to create simple tendency to move upward

def check_input(u, uTrue, z, zTrue):
    #check u
    if type(u)==list:
        u=np.array(u).T
    elif len(z.shape)==1:
        u=np.array(u.tolist()).T
    elif len(z.shape)==2 and u.shape[0] == 1 and u.shape[1] == 2:
            u = u.T
    #check uTrue
    if type(uTrue)==list:
        uTrue=np.array(uTrue).T
    elif len(z.shape)==1:
        uTrue=np.array(uTrue.tolist()).T
    elif len(z.shape)==2 and uTrue.shape[0] == 1 and uTrue.shape[1] == 2:
            uTrue = uTrue.T
    #check z
    if type(z)==list:
        z=np.array(z)
    elif len(z.shape)==1:
        z=np.array(z.tolist())
    elif len(z.shape)==2 and z.shape[0] == 2 and z.shape[1] == 1:
            z = z.T
    #check zTrue
    if type(zTrue)==list:
        zTrue=np.array(zTrue)
    elif len(zTrue.shape)==1:
        zTrue=np.array(zTrue.tolist())
    elif len(zTrue.shape)==2 and zTrue.shape[0] == 2 and zTrue.shape[1] == 1:
            zTrue = zTrue.T
    #return
    return (u, uTrue, z, zTrue)



#velocity i and j from cmd vel
def simulate_input():
    [v_i,v_j] = random.choice([[1,0],[-1,0],[0,1]]) # omitted [0,-1] to create tendency to move upward
    u = np.matrix([v_i, v_j]).T
    return u
def simulate_measurement(xTrue):
    #gps i,j
    i = xTrue[0, 0]
    j = xTrue[1, 0]
    z = np.matrix([i, j])
    return z

    def recieve_input():
        # [v_i,v_j] = random.choice([[1,0],[-1,0],[0,1]]) # omitted [0,-1] to create tendency to move upward
        rospy.init_node('/cmd_vel', anonymous=True)
	    # rospy.spin()
        u = np.matrix(c).T
        # return u

    def vel_callback(data):
        [v_i,v_j] = [data.linear.x, data.linear.y]


	def recieve_inputs(self):
        recieve_input()
        uTrue =  self.u
        xTrue = motion_model(self.xTrue, uTrue)
        # Replace with rage finder model
        zTrue = simulate_measurement(xTrue)

        # maybe add measurement_noise
        add_measurement_noise = True
        if add_measurement_noise: z = simulate_measurement_noise(zTrue)
        else:z=zTrue

        # maybe add input_noise
        add_input_noise = True
        if add_input_noise: u = simulate_input_noise(uTrue)
        else:u=uTrue
        return (u, uTrue, z, zTrue)


    # def simulate_inputs(self):
    #     uTrue = simulate_input()
    #     xTrue = motion_model(self.xTrue, uTrue)
    #     zTrue = simulate_measurement(xTrue)
    #
    #     # maybe add measurement_noise
    #     add_measurement_noise = True
    #     if add_measurement_noise: z = simulate_measurement_noise(zTrue)
    #     else:z=zTrue
    #
    #     # maybe add input_noise
    #     add_input_noise = True
    #     if add_input_noise: u = simulate_input_noise(uTrue)
    #     else:u=uTrue
    #     return (u, uTrue, z, zTrue)

    #################################################
	# Publishers and subscribers
def listen_vel():
	rospy.init_node('/cmd_vel', anonymous=True)
	rospy.Subscriber('/cmd_vel', Twist, vel_callback)
    u = [data.linear.x, data.linear.y]
    return u


    # get velocity of Move_You
 def vel_callback(data):
     global u
     u = data


 def talk_pose():
     odometry_publisher = rospy.Publisher('/you_odom',Pose, queue_size=10)
     rospy.init_node('/you_odom', anonymous=True)
     rate = rospy.Rate(1) # 1hz

     global odom
     odom = Pose()
     odom.position.x = xEsti
     odom.position.y = xEstj
     odometry_publisher.publish(odom)

def simulate_input_noise(u):
    ui = u[0, 0]*get_rand()
    uj = u[1, 0]*get_rand()
    u = np.matrix([ui, uj]).T
    return u

def simulate_measurement_noise(z):
    # add noise to gps i-j
    i = z[0,0] + np.random.randn()//2
    j = z[0,1] + np.random.randn()//2
    z = np.matrix([i, j])
    return z


def motion_model(x, u):
#     u is the change in location or "velocity"
#     x = position i,j
#     velocities are independent of each other
    F = np.matrix([[1.0, 0, 0, 0],
                   [0, 1.0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]])

    B = np.matrix([[1.0, 0],
                   [0, 1.0],
                   [1.0, 0],
                   [0, 1.0]])

    x = F * x + B * u
    return x
def observation_model(x):
    #  Observation Model
    H = np.matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0]
#         [1, 0],
#         [0, 1]
    ])
    z = H * x
    return z


def jacobF(x, u):
    """
    Jacobian of Motion Model

    motion model
    x_{t+1} = x_t+v_x
    y_{t+1} = y_t+v_y
    x_t{t+1} = v_x
    y_t{t+1} = v_y
    so
    dx/dv_x = 1
    dy/dv_y = 1
    """
    v_x =u[0, 0]
    v_y =u[1, 0]
    jF = np.matrix([
         [1.0, 0.0, 1, 0],
         [0.0, 1.0, 0, 1],
         [0.0, 0.0, 1.0, 0.0],
         [0.0, 0.0, 0.0, 1.0]])
    return jF



def jacobH(x):
    # Jacobian of Observation Model
    jH = np.matrix([
        [1, 0, 0, 0],
        [0, 1, 0, 0]
    ])
    return jH



// TODO: publish xEst as odom2
def ekf_estimation(xEst, PEst, z, u):

    #  Predict
    xPred = motion_model(xEst, u)
    jF = jacobF(xPred, u)
    PPred = jF * PEst * jF.T + Q

    #  Update
    jH = jacobH(xPred)
    zPred = observation_model(xPred)
    y = z.T - zPred
    S = jH * PPred * jH.T + R
    K = PPred * jH.T * np.linalg.inv(S)
    xEst = xPred + K * y
    PEst = (np.eye(len(xEst)) - K * jH) * PPred


    return xEst, PEst


def plot_covariance_ellipse(xEst, PEst):
    Pxy = PEst[0:2, 0:2]
    eigval, eigvec = np.linalg.eig(Pxy)

    if eigval[0] >= eigval[1]:
        bigind = 0
        smallind = 1
    else:
        bigind = 1
        smallind = 0

    t = np.arange(0, 2 * math.pi + 0.1, 0.1)
    a = math.sqrt(eigval[bigind])
    b = math.sqrt(eigval[smallind])
    x = [a * math.cos(it) for it in t]
    y = [b * math.sin(it) for it in t]
    angle = math.atan2(eigvec[bigind, 1], eigvec[bigind, 0])
    R = np.matrix([[math.cos(angle), math.sin(angle)],
                   [-math.sin(angle), math.cos(angle)]])
    fx = R * np.matrix([x, y])
    px = np.array(fx[0, :] + xEst[0, 0]).flatten()
    py = np.array(fx[1, :] + xEst[1, 0]).flatten()
    plt.plot(px, py, "--r")

def graph_hist(hz,hxTrue,hxDR,hxEst,xEst,PEst):
        plt.cla()
        plt.plot(hz[:, 0], hz[:, 1], ".g")
        plt.plot(np.array(hxTrue[0, :]).flatten(),
                 np.array(hxTrue[1, :]).flatten(), "-b")
        plt.plot(np.array(hxDR[0, :]).flatten(),
                 np.array(hxDR[1, :]).flatten(), "-k")
        plt.plot(np.array(hxEst[0, :]).flatten(),
                 np.array(hxEst[1, :]).flatten(), "-r")
        plot_covariance_ellipse(xEst, PEst)
        plt.axis("equal")
        plt.grid(True)
        plt.pause(0.001)

class kalman_filter:
    def __init__(self):
        # State Vector [x y yaw v]'
        self.xEst = np.matrix(np.zeros((4, 1)))
        self.xTrue = np.matrix(np.zeros((4, 1)))
        self.PEst = np.eye(4)
        self.xDR = np.matrix(np.zeros((4, 1)))  # Dead reckoning
        # history
        self.hxEst = self.xEst
        self.hxTrue = self.xTrue
        self.hxDR = self.xTrue
        self.hz = np.zeros((1, 2))
        self.hu = np.zeros((1, 2))
        # self.u = np.zeros((1,2))

    // TODO: publish xTrue as odom2.

    def move_forward(self,u,uTrue,z,zTrue):
        #main function
        u, uTrue, z, zTrue = check_input(u, uTrue, z, zTrue)
        self.simulate_DR(u)
        self.estimate(u,z)
        # publish self.XTrue
        self.xTrue = motion_model(self.xTrue, uTrue)
        self.store_history(u,z)


	# simulate input from sensor
	# input from teleop
	# Input pose




    def simulate_DR(self,u):
        # simulate DR movement (i.e. localize robot as if it had only positional data from the start)
        self.xDR = motion_model(self.xDR, u)


    def estimate(self,u,z):
        self.xEst, self.PEst = ekf_estimation(self.xEst, self.PEst, z, u)


    def store_history(self,u,z):
        # store data history
        self.hxEst  = np.hstack((self.hxEst, self.xEst))
        self.hxDR   = np.hstack((self.hxDR, self.xDR))
        self.hxTrue = np.hstack((self.hxTrue, self.xTrue))
        self.hu     = np.vstack((self.hu, u.T))
        self.hz     = np.vstack((self.hz, z))


    def graph(self):
        graph_hist(self.hz,self.hxTrue,self.hxDR,self.hxEst,self.xEst,self.PEst)




#example usage
def main():
    kf = kalman_filter()
    for _ in range(100):
        u, uTrue, z, zTrue = kf.simulate_inputs()
        kf.move_forward(u,uTrue,z,zTrue)
        kf.graph()

if __name__ == '__main__':
    main()


"""
# optional robot driver.

# gps sensor sends messege containing: zTruei, zTruej, zi, zj (instructions say to use a custom message type)
    zTruei: true i position
    zTruej: true j position
    zi: noisy i position
    zj: noisy j position
        For simulating noise, we can:
            1. pick values from a normal distribution to add on i.e. for some constant c, do:
                zi = zTruei + np.random.randn()/c
                zj = zTruej + np.random.randn()/c
            2. same as 1 but descritize zi and zj, do:
                zi = zTruei + np.random.randn()//c
                zj = zTruej + np.random.randn()//c

# Teleopereation driver recives input from keyboard (or the telnode) and sends messege containing: uTruei, uTruej, ui, uj
    uTruei: true i velocity
    uTruej: true j velocity
    ui: noisy i velocity
    uj: noisy j velocity
        Note that valid input and uTruei,uTruej output combinations are:
            Move Forward: uTruei = 0, uTruei = 1
            Move Backward: uTruei = 0, uTruei = -1
            Move Left: uTruei = -1, uTruei = 0
            Move Right: uTruei = 1, uTruei = 0
        For simulating noise, we can:
            1. we can have a chance that the robot slips and doesnt move
            2. we can have a chance that it picks any of the random direction
    For testing we can use random.choice([[1,0],[-1,0],[0,1]]) to input

# kf script recieves these messeges and in seperate topics sends
        a geometry_msgs/Pos message containing the odometry information:
            xEsti: Estimated i position
            xEstj: Estimated j position
        a geometry_msgs/Pos messege containing the error
            xERRi=xTruei-xEsti
            xERRi=xTruei-xEst
                and maybe
            xsqERRi=(xTruei-xEst)^2
            xsqERRi=(xTruei-xEst)^2

# Finally we need to visualize in the world:
    the robot's position
    the estimated position from the kf script
    maybe the sensor's noisy position?
        It doesn't seems like we need to show the variance like in the nice script we were provided does.
"""
