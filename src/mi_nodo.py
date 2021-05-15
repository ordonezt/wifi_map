#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from gazebo_wifi_plugin.msg import ReceiverReport

# para correr simulacion: LASER=rplidar RVIZ=true LOCALIZATION=amcl roslaunch ca_gazebo mapa
# para correr paquete: "rosrun mi_paquete_2 mi_nodo.py"

# variables globales
x = 0
y = 0
potencia = 0



def my_timer_callback(self, event=None):
    global x,y
    str = "pos x={}, pos y={}, pot={}".format(y,x,potencia)
    rospy.loginfo(str)
    mi_pub.publish(String(str))

def callback_pos(msg):
    global x,y
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y

def callback_wifi(data):
    global potencia
    potencia = data.router_info[0].signal_strength

def subscriptor_pos():
    rospy.Subscriber("/create1/odom",Odometry,callback_pos)

def subscriptor_wifi():
    rospy.Subscriber("/cogrob_wireless_receiver/receiver_report", ReceiverReport, callback_wifi)
    

if __name__ == '__main__':
    
    # main
    # Inicio el nodo
    rospy.init_node('mi_nodo')
    mi_pub = rospy.Publisher('mi_publicador', String)
    # Inicio el timer
    rospy.Timer(rospy.Duration(1), my_timer_callback)
    # Inicio el subscriptor de posicion
    subscriptor_pos()
    # Inicio el subscriptor de wifi
    subscriptor_wifi()
    # Utilizo spin para loopear
    rospy.spin()

