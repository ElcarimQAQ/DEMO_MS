#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>

int main(int argc, char *argv[])
{
    //初始化 ROS 节点:命名(唯一)
    ros::init(argc, argv, "Gouzi");
    //实例化 ROS 句柄
    ros::NodeHandle nh;
    ros::Publisher pub = nh.advertise<std_msgs::String>("fang",10);
    std_msgs::String msg;
    ros::Rate rate(10);
    int count = 0;
    while (ros::ok)
    {
        count++;
        std::stringstream ss;
        ss << "hello ---" << count;
        //msg.data = "hello";
        msg.data = ss.str();
        pub.publish(msg);

        rate.sleep();
        //官方建议添加
        //ros::spinOnce(); 
    }
    
    return 0;
}

