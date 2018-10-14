#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import ros_kalman_filter2
from kuka_kickass_kalman.msg import Obs

def callback(vel_msg):
    #once velocity is recieved, wait for next sensor reading
    sensor_msg = rospy.wait_for_message('sensor_readings', Obs)
    
    #housekeeping with the msgs
    ui     = vel_msg.linear.x 
    uj     = vel_msg.linear.y
    uTruei = vel_msg.linear.x 
    uTruej = vel_msg.linear.y
    zi     = sensor_msg.z1
    zj     = sensor_msg.z2
    zTruei = zi  #TODO: Need true zTruei
    zTruej = zj  #TODO: Need true zTruej
    
    u      = [ui,uj]         #noisy velocity
    uTrue  = [uTruei,uTruej] #true velocity
    z      = [zi,zj]         #noisy position
    zTrue  = [zTruei,zTruej] #true position
        
    #estimate the postition
    xEsti,xEstj = kf.move_forward(u,uTrue,z,zTrue,generate_input_noise = True,generate_measurement_noise = False)
    
    #caculate error
    xErri, = zTruei-xEsti
    xErrj  = zTruej-xEstj

    #create and send position estimate messege
    global xEst_msg
    xEst_msg    = Obs()
    xEst_msg.z1 = xErri
    xEst_msg.z2 = xErrj
    xEst_pub.publish(xEst_msg)
    
    #create and send error messege
    global xErr_msg
    xErr_msg    = Obs()
    xErr_msg.z1 = xErri
    xErr_msg.z2 = xErrj
    xErr_pub.publish(xErr_msg)
    
    #log info
    rospy.loginfo("\nxEst"+str(xEst_msg)+"\neErr:"+str(xErr_msg))

def kf_node():
    global kf
    kf = kalman_filter()
    rospy.init_node('kf_node', anonymous=True)
    
    xEst_pub = rospy.Publisher('geometry_msgs/Pos/xEst', Twist, queue_size=10)
    Err_pub = rospy.Publisher('geometry_msgs/Pos/error', Twist, queue_size=10)
    
    rospy.Subscriber('/cmd_vel', Twist, callback=callback)
    rospy.spin()

if __name__ == '__main__':
    kf_node()
