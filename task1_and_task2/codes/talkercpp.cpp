#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Int16.h"
#include "std_msgs/Bool.h"
#include <sstream>
#include "robot_pkg/custom_message.h"

void number_publisher(ros::NodeHandle& n){
    ros::Publisher num_chatter_pub = n.advertise<std_msgs::Int16>("num_chatter",1000); // let ros master know(advertise) the type of data (string) and the topic(chatter_pub) that its being published on.
    ros::Rate loop_rate(10); // keep track of time after rate::sleep() is called.

    int count = 0;
    while (ros::ok())
    {
        std_msgs::Int16 msg;
        msg.data = count; 

        ROS_INFO("%d", msg.data); //basically cout
        num_chatter_pub.publish(msg);

        ros::spinOnce();
        loop_rate.sleep();
        count++;
    }
}

void talker(ros::NodeHandle& n){
    ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter",1000); // let ros master know(advertise) the type of data (string) and the topic(chatter_pub) that its being published on.
    ros::Rate loop_rate(10); // keep track of time after rate::sleep() is called.

    int count = 0;
    while (ros::ok())
    {
        std_msgs::String msg;
        std::stringstream ss;
        ss<<"hello world!"<<count;
        msg.data = ss.str(); //store ss as string data type in data attribute of msg.

        ROS_INFO("%s", msg.data.c_str()); //basically cout
        chatter_pub.publish(msg);

        ros::spinOnce();
        loop_rate.sleep();
        count++;
    }
}

void bool_publisher(ros::NodeHandle& n){
    ros::Publisher bool_chatter_pub = n.advertise<std_msgs::Bool>("bool_chatter",1000); // let ros master know(advertise) the type of data (string) and the topic(chatter_pub) that its being published on.
    ros::Rate loop_rate(10); // keep track of time after rate::sleep() is called.

    std_msgs::Bool msg;
    bool decision=false;
    msg.data = decision;
    while (ros::ok())
    {
        ROS_INFO("%d", msg.data); //basically cout
        bool_chatter_pub.publish(msg);
    
        ros::spinOnce();
        loop_rate.sleep();
        if (msg.data == 0)
            msg.data = true;
        else
            msg.data = false;

    }
}

void custom_publisher(ros::NodeHandle& n){
    ros::Publisher custom_chatter_pub = n.advertise<robot_pkg::custom_message>("custom_chatter",1000);
    ros::Rate loop_rate(10);

    robot_pkg::custom_message msg;
    msg.id.data = 1;
    msg.name.data = "hello";
    msg.employed.data = false;
    msg.location.x = 0;
    msg.location.y = 0;
    msg.location.theta = 0;

    while (ros::ok())
    {
        custom_chatter_pub.publish(msg);
        ros::spinOnce();
        loop_rate.sleep();

        if (msg.employed.data == 0)
            msg.employed.data = true;
        else
            msg.employed.data = false;
        msg.id.data++;
        msg.location.x += 2;
        msg.location.y += 3;
        msg.location.theta += 1;
        ROS_INFO("in this loop");
    }
    
}

int main(int argc, char **argv){

    ros::init(argc, argv, "talkercpp");

    ros::NodeHandle n; // must write in order to use the node and close it after use
    custom_publisher(n);
    return 0;
}