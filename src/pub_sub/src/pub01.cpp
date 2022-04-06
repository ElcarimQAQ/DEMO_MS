#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "Gouzi");
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
    }
    
    return 0;
}

