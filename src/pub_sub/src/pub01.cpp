#include "ros/ros.h"
#include "std_msgs/String.h"

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "Gouzi");
    ros::NodeHandle nh;
    ros::Publisher pub = nh.advertise<std_msgs::String>("fang",10);
    std_msgs::String msg;
    while (ros::ok)
    {
        msg.data = "hello";
        pub.publish(msg);
    }
    
    return 0;
}

