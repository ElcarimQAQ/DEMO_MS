#!/usr/bin/python
# -*- coding:utf8 -*-
#----------------函数头-------------------#
import paho.mqtt.client as mqtt
import time
import rospy
import json
from geometry_msgs.msg import Twist
from sensor_msgs.msg import BatteryState

#---------------------变量设置-------------------#
# Client对象构造
MQTTHOST = "a1tv8PbA9tI.iot-as-mqtt.cn-shanghai.aliyuncs.com"
MQTTPORT = 1883
mqttClient = mqtt.Client("a1tv8PbA9tI.SmartCar|securemode=2,signmethod=hmacsha256,timestamp=1653309123079|")
mqttClient.username_pw_set("SmartCar&a1tv8PbA9tI", "ecf257823f478c549c256bab3c3d069f4d64d729698d1149ffba5d32a99b107b")

post_path = "/sys/a1tv8PbA9tI/SmartCar/thing/event/property/post"

#---------------------mqtt设置------------------------#
# 连接MQTT服务器
def on_mqtt_connect():
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    print("连接阿里云")
    payload_json = {
        'id': int(time.time()),
        'params': {
            'connectState': 1,
        },
        'method': "thing.event.property.post"
        }
    time.sleep(0.5)
    on_publish(post_path,str(payload_json),1)
    print(str(payload_json))
    mqttClient.loop_start()

# publish 消息
def on_publish(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)

# 消息处理函数
def on_message_come(lient, userdata, msg):
    user_dic = json.loads(msg.payload)
    twist = Twist()
    try:
        param_dic =user_dic["params"]
    except:
        print("no params")
    print(user_dic)
    try:
        # 接受速度控制
        if("linear_x" in param_dic.keys()):
            pub_linear_x = user_dic["params"]["linear_x"]
            twist.linear.x = pub_linear_x
            print("从云平台接收到线速度x")
            print(pub_linear_x)
        
        if("linear_y" in param_dic.keys()):
            pub_linear_y = user_dic["params"]["linear_x"]
            twist.linear.y = pub_linear_y
            print("从云平台接收到线速度y")
            print(pub_linear_y)

        if("angular_z" in param_dic.keys()):
            pub_angular_z = user_dic["params"]["angular_z"]
            twist.angular.z = pub_angular_z
            print("从云平台接收到角速度z")
    
        pub.publish(twist)
        
    except:
        print(user_dic)


# subscribe 消息
def on_subscribe():
    # 订阅监听自定义Topic
    mqttClient.subscribe("/********/pythondevice2/user/update1", 1)
    mqttClient.on_message = on_message_come # 消息到来处理函数



#------------------小车速度上报------------------#
def vel_callback(data):
    print(data)
    if(data.linear.x == -0.0 and data.linear.y == -0.0 and data.angular.z ==-0.0 ):
        pass
    else:
        linear_x = data.linear.x
        linear_y = data.linear.y
        angular_z = data.angular.z
        payload_json = {
            'id': int(time.time()),
            'params': {
                'linear_x': linear_x,
                'linear_y': linear_y,
                'angular_z': angular_z,
                'baseState':1,
            },
            'method': "thing.event.property.post"
            }
        time.sleep(0.5)
        on_publish(post_path,str(payload_json),1)
        print(str(payload_json))

#------------------小车电量上报------------------#     
def battery_callback(data):  
    print(data)
    if(data.voltage == 0.0 and data.current == 0.0 ):
        pass
    else:
        payload_json = {
            'id': int(time.time()),
            'params': {
                'batteryState': {
                'voltage': 10.888889,
                'current': 0.2499982
                },
            },
            'method': "thing.event.property.post"
            }
        time.sleep(0.5)
        on_publish(post_path,str(payload_json),1)
        print(str(payload_json))


def send_cmd():
    rate = rospy.Rate(2) # 10hz
    while not rospy.is_shutdown():
        pub.publish(twist)
        rate.sleep()

def mqttcmdCB(data):
    trans_x = data.linear.x
    trans_y = data.linear.y
    rotat_z = data.angular.z
    


if __name__ == '__main__':
    rospy.init_node('mqtt_server')
    on_mqtt_connect()
    on_subscribe()
    
    #rospy.Subscriber("/mqtt_server", Twist, mqtt_callback)
    pub = rospy.Publisher('cmd_vel', Twist,queue_size = 3)
    #sub cmd_vel topic
    sub = rospy.Subscriber('/cmd_vel',Twist,vel_callback,queue_size=20)
    battery_sub = rospy.Subscriber('/battery',BatteryState,battery_callback,queue_size=3)
    rospy.spin()
