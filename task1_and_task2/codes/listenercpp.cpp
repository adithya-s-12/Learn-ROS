#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Int16.h"
#include "std_msgs/Bool.h"
#include "robot_pkg/custom_message.h"

void num_callback(const std_msgs::Int16::ConstPtr& msg){
    ROS_INFO("the number is: [%d]", msg->data);
}

void callback(const std_msgs::String::ConstPtr& msg){
    ROS_INFO("I heard: [%s]",msg->data.c_str());
}

void bool_callback(const std_msgs::Bool::ConstPtr& msg){
    ROS_INFO("the decision is : [%s]",msg->data?"true":"false");
}

void custom_callback(const robot_pkg::custom_message::ConstPtr& msg){
    ROS_INFO("ID-number: %d, Name: %s, Employment status: %s, location(x,y,theta): (%f,%f,%f)",
    msg->id.data, msg->name.data.c_str(), msg->employed.data?"true":"false",
    msg->location.x, msg->location.y, msg->location.theta);
}

void num_subscriber(ros::NodeHandle& n){
    ros::Subscriber sub = n.subscribe("num_chatter", 1000, num_callback);
    ros::spin();
}

void listener(ros::NodeHandle& n){
    ros::Subscriber sub = n.subscribe("chatter", 1000, callback);
    ros::spin();
}

void bool_subscriber(ros::NodeHandle& n){
    ros::Subscriber sub = n.subscribe("bool_chatter", 1000, bool_callback);
    ros::spin();
}

void custom_subscriber(ros::NodeHandle& n){
    ros::Subscriber sub = n.subscribe("custom_chatter",1000,custom_callback);
    ros::spin();
}

int main(int argc, char **argv){
    ros::init(argc,argv,"listenercpp");
    ros::NodeHandle n;
    custom_subscriber(n);

    return 0;
}