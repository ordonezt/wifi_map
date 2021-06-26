#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from gazebo_wifi_plugin.msg import ReceiverReport
import numpy as np
from grilla_lib import Grilla, condicion_finalizacion
from nav_msgs.msg import OccupancyGrid

# para correr simulacion: LASER=rplidar RVIZ=true LOCALIZATION=amcl roslaunch ca_gazebo mapa
# para correr paquete: "rosrun mi_paquete_2 mi_nodo.py"
# para correr comando de velocidades por teclado: rosrun teleop_twist_keyboard teleop_twist_keyboard.py cmd_vel:=/create1/cmd_vel/out
# variables globales
dimension_x = 20#1000 Puse 3 para no explotar la consola
dimension_y = 20#1000
resolucion = 0.25 #celdas de 10cm

x = 0
y = 0
potencia = 0
grilla = Grilla(dimension_x, dimension_y, resolucion)


def my_timer_callback(self, event=None):
    global x,y
    global grilla

    str = "pos x={}, pos y={}, pot={}".format(y,x,potencia)
    
    grilla.agregar_punto(potencia, y, x)
    #grilla.graficar()
    aux = grilla.grilla2occupancy_grid()
    rospy.loginfo(aux)
    map_pub.publish(aux)
    
    rospy.loginfo(str)
    mi_pub.publish(String(str))

    if(condicion_finalizacion(grilla) == True):
        grilla.graficar()
        rospy.signal_shutdown("Mapa terminado!")

def callback_pos(msg):
    global x,y
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y

def callback_wifi(data):
    global potencia
    try:
        potencia = data.router_info[0].signal_strength
    except:
        potencia = -90

def subscriptor_pos():
    rospy.Subscriber("/create1/odom",Odometry,callback_pos)

def subscriptor_wifi():
    rospy.Subscriber("/cogrob_wireless_receiver/receiver_report", ReceiverReport, callback_wifi)
    

if __name__ == '__main__':
    
    # main
    # Inicio el nodo
    rospy.init_node('mi_nodo')
    mi_pub = rospy.Publisher('mi_publicador', String)
    map_pub = rospy.Publisher('publicador_mapa', OccupancyGrid)
    # Inicio el timer
    rospy.Timer(rospy.Duration(1), my_timer_callback)
    # Inicio el subscriptor de posicion
    subscriptor_pos()
    # Inicio el subscriptor de wifi
    subscriptor_wifi()
    # Utilizo spin para loopear
    rospy.spin()

