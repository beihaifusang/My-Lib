// Generated by gencpp from file perception_msgs/imu_msg.msg
// DO NOT EDIT!


#ifndef PERCEPTION_MSGS_MESSAGE_IMU_MSG_H
#define PERCEPTION_MSGS_MESSAGE_IMU_MSG_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>

namespace perception_msgs
{
template <class ContainerAllocator>
struct imu_msg_
{
  typedef imu_msg_<ContainerAllocator> Type;

  imu_msg_()
    : header()
    , sys_time_us(0)
    , measurement_time(0)
    , status(0)
    , measurement_span(0.0)
    , linear_acceleration_x(0.0)
    , linear_acceleration_y(0.0)
    , linear_acceleration_z(0.0)
    , linear_acceleration_covariance()
    , angular_velocity_x(0.0)
    , angular_velocity_y(0.0)
    , angular_velocity_z(0.0)
    , angular_velocity_covariance()
    , orientation_pitch(0.0)
    , orientation_roll(0.0)
    , orientation_yaw(0.0)
    , orientation_quternion_1(0.0)
    , orientation_quternion_2(0.0)
    , orientation_quternion_3(0.0)
    , orientation_quternion_4(0.0)
    , orientation_covariance()  {
      linear_acceleration_covariance.assign(0.0);

      angular_velocity_covariance.assign(0.0);

      orientation_covariance.assign(0.0);
  }
  imu_msg_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , sys_time_us(0)
    , measurement_time(0)
    , status(0)
    , measurement_span(0.0)
    , linear_acceleration_x(0.0)
    , linear_acceleration_y(0.0)
    , linear_acceleration_z(0.0)
    , linear_acceleration_covariance()
    , angular_velocity_x(0.0)
    , angular_velocity_y(0.0)
    , angular_velocity_z(0.0)
    , angular_velocity_covariance()
    , orientation_pitch(0.0)
    , orientation_roll(0.0)
    , orientation_yaw(0.0)
    , orientation_quternion_1(0.0)
    , orientation_quternion_2(0.0)
    , orientation_quternion_3(0.0)
    , orientation_quternion_4(0.0)
    , orientation_covariance()  {
  (void)_alloc;
      linear_acceleration_covariance.assign(0.0);

      angular_velocity_covariance.assign(0.0);

      orientation_covariance.assign(0.0);
  }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef uint64_t _sys_time_us_type;
  _sys_time_us_type sys_time_us;

   typedef uint64_t _measurement_time_type;
  _measurement_time_type measurement_time;

   typedef uint8_t _status_type;
  _status_type status;

   typedef double _measurement_span_type;
  _measurement_span_type measurement_span;

   typedef double _linear_acceleration_x_type;
  _linear_acceleration_x_type linear_acceleration_x;

   typedef double _linear_acceleration_y_type;
  _linear_acceleration_y_type linear_acceleration_y;

   typedef double _linear_acceleration_z_type;
  _linear_acceleration_z_type linear_acceleration_z;

   typedef boost::array<double, 9>  _linear_acceleration_covariance_type;
  _linear_acceleration_covariance_type linear_acceleration_covariance;

   typedef double _angular_velocity_x_type;
  _angular_velocity_x_type angular_velocity_x;

   typedef double _angular_velocity_y_type;
  _angular_velocity_y_type angular_velocity_y;

   typedef double _angular_velocity_z_type;
  _angular_velocity_z_type angular_velocity_z;

   typedef boost::array<double, 9>  _angular_velocity_covariance_type;
  _angular_velocity_covariance_type angular_velocity_covariance;

   typedef double _orientation_pitch_type;
  _orientation_pitch_type orientation_pitch;

   typedef double _orientation_roll_type;
  _orientation_roll_type orientation_roll;

   typedef double _orientation_yaw_type;
  _orientation_yaw_type orientation_yaw;

   typedef double _orientation_quternion_1_type;
  _orientation_quternion_1_type orientation_quternion_1;

   typedef double _orientation_quternion_2_type;
  _orientation_quternion_2_type orientation_quternion_2;

   typedef double _orientation_quternion_3_type;
  _orientation_quternion_3_type orientation_quternion_3;

   typedef double _orientation_quternion_4_type;
  _orientation_quternion_4_type orientation_quternion_4;

   typedef boost::array<double, 9>  _orientation_covariance_type;
  _orientation_covariance_type orientation_covariance;





  typedef boost::shared_ptr< ::perception_msgs::imu_msg_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::perception_msgs::imu_msg_<ContainerAllocator> const> ConstPtr;

}; // struct imu_msg_

typedef ::perception_msgs::imu_msg_<std::allocator<void> > imu_msg;

typedef boost::shared_ptr< ::perception_msgs::imu_msg > imu_msgPtr;
typedef boost::shared_ptr< ::perception_msgs::imu_msg const> imu_msgConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::perception_msgs::imu_msg_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::perception_msgs::imu_msg_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace perception_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': True}
// {'perception_msgs': ['/home/shawn/baidu/ai-auto/l3-apollo/catkin_build/src/modules/ros_msgs/perception/msg'], 'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::perception_msgs::imu_msg_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::perception_msgs::imu_msg_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::perception_msgs::imu_msg_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::perception_msgs::imu_msg_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::perception_msgs::imu_msg_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::perception_msgs::imu_msg_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::perception_msgs::imu_msg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "a5d5185182740eff2a9cfee6dab5ea7b";
  }

  static const char* value(const ::perception_msgs::imu_msg_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xa5d5185182740effULL;
  static const uint64_t static_value2 = 0x2a9cfee6dab5ea7bULL;
};

template<class ContainerAllocator>
struct DataType< ::perception_msgs::imu_msg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "perception_msgs/imu_msg";
  }

  static const char* value(const ::perception_msgs::imu_msg_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::perception_msgs::imu_msg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# This is a message to hold data from an IMU (Inertial Measurement Unit)\n\
#\n\
# Accelerations should be in m/s^2 (not in g's), and rotational velocity should be in rad/sec\n\
#\n\
# If the covariance of the measurement is known, it should be filled in (if all you know is the \n\
# variance of each measurement, e.g. from the datasheet, just put those along the diagonal)\n\
# A covariance matrix of all zeros will be interpreted as \"covariance unknown\", and to use the\n\
# data a covariance will have to be assumed or gotten from some other source\n\
#\n\
# If you have no estimate for one of the data elements (e.g. your IMU doesn't produce an orientation \n\
# estimate), please set element 0 of the associated covariance matrix to -1\n\
# If you are interpreting this message, please check for a value of -1 in the first element of each \n\
# covariance matrix, and disregard the associated estimate.\n\
\n\
Header header\n\
\n\
uint64 sys_time_us              #/*用于各传感器消息时间同步的时间戳*/\n\
\n\
uint64 measurement_time\n\
#unit is us.\n\
\n\
uint8 status\n\
\n\
# When measurement_span is non-zero, the gyroscope and accelerometer\n\
# measurements are averaged for the period from\n\
# (measurement_time - measurement_span) to measurement_time. Usually,\n\
#      measurement_span = 1 / sampling_frequency.\n\
#\n\
# When measurement_span is 0, angular_velocity and linear_acceleration are\n\
# instantaneous at measurement_time.\n\
\n\
float64 measurement_span\n\
\n\
float64 linear_acceleration_x\n\
float64 linear_acceleration_y\n\
float64 linear_acceleration_z\n\
float64[9] linear_acceleration_covariance # Row major x, y z\n\
\n\
float64 angular_velocity_x\n\
float64 angular_velocity_y\n\
float64 angular_velocity_z\n\
float64[9] angular_velocity_covariance # Row major about x, y, z axes\n\
\n\
float64 orientation_pitch\n\
float64 orientation_roll\n\
float64 orientation_yaw\n\
\n\
float64 orientation_quternion_1\n\
float64 orientation_quternion_2\n\
float64 orientation_quternion_3\n\
float64 orientation_quternion_4\n\
\n\
float64[9] orientation_covariance # Row major about x, y, z axes\n\
\n\
================================================================================\n\
MSG: std_msgs/Header\n\
# Standard metadata for higher-level stamped data types.\n\
# This is generally used to communicate timestamped data \n\
# in a particular coordinate frame.\n\
# \n\
# sequence ID: consecutively increasing ID \n\
uint32 seq\n\
#Two-integer timestamp that is expressed as:\n\
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n\
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n\
# time-handling sugar is provided by the client library\n\
time stamp\n\
#Frame this data is associated with\n\
# 0: no frame\n\
# 1: global frame\n\
string frame_id\n\
";
  }

  static const char* value(const ::perception_msgs::imu_msg_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::perception_msgs::imu_msg_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.sys_time_us);
      stream.next(m.measurement_time);
      stream.next(m.status);
      stream.next(m.measurement_span);
      stream.next(m.linear_acceleration_x);
      stream.next(m.linear_acceleration_y);
      stream.next(m.linear_acceleration_z);
      stream.next(m.linear_acceleration_covariance);
      stream.next(m.angular_velocity_x);
      stream.next(m.angular_velocity_y);
      stream.next(m.angular_velocity_z);
      stream.next(m.angular_velocity_covariance);
      stream.next(m.orientation_pitch);
      stream.next(m.orientation_roll);
      stream.next(m.orientation_yaw);
      stream.next(m.orientation_quternion_1);
      stream.next(m.orientation_quternion_2);
      stream.next(m.orientation_quternion_3);
      stream.next(m.orientation_quternion_4);
      stream.next(m.orientation_covariance);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct imu_msg_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::perception_msgs::imu_msg_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::perception_msgs::imu_msg_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "sys_time_us: ";
    Printer<uint64_t>::stream(s, indent + "  ", v.sys_time_us);
    s << indent << "measurement_time: ";
    Printer<uint64_t>::stream(s, indent + "  ", v.measurement_time);
    s << indent << "status: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.status);
    s << indent << "measurement_span: ";
    Printer<double>::stream(s, indent + "  ", v.measurement_span);
    s << indent << "linear_acceleration_x: ";
    Printer<double>::stream(s, indent + "  ", v.linear_acceleration_x);
    s << indent << "linear_acceleration_y: ";
    Printer<double>::stream(s, indent + "  ", v.linear_acceleration_y);
    s << indent << "linear_acceleration_z: ";
    Printer<double>::stream(s, indent + "  ", v.linear_acceleration_z);
    s << indent << "linear_acceleration_covariance[]" << std::endl;
    for (size_t i = 0; i < v.linear_acceleration_covariance.size(); ++i)
    {
      s << indent << "  linear_acceleration_covariance[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.linear_acceleration_covariance[i]);
    }
    s << indent << "angular_velocity_x: ";
    Printer<double>::stream(s, indent + "  ", v.angular_velocity_x);
    s << indent << "angular_velocity_y: ";
    Printer<double>::stream(s, indent + "  ", v.angular_velocity_y);
    s << indent << "angular_velocity_z: ";
    Printer<double>::stream(s, indent + "  ", v.angular_velocity_z);
    s << indent << "angular_velocity_covariance[]" << std::endl;
    for (size_t i = 0; i < v.angular_velocity_covariance.size(); ++i)
    {
      s << indent << "  angular_velocity_covariance[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.angular_velocity_covariance[i]);
    }
    s << indent << "orientation_pitch: ";
    Printer<double>::stream(s, indent + "  ", v.orientation_pitch);
    s << indent << "orientation_roll: ";
    Printer<double>::stream(s, indent + "  ", v.orientation_roll);
    s << indent << "orientation_yaw: ";
    Printer<double>::stream(s, indent + "  ", v.orientation_yaw);
    s << indent << "orientation_quternion_1: ";
    Printer<double>::stream(s, indent + "  ", v.orientation_quternion_1);
    s << indent << "orientation_quternion_2: ";
    Printer<double>::stream(s, indent + "  ", v.orientation_quternion_2);
    s << indent << "orientation_quternion_3: ";
    Printer<double>::stream(s, indent + "  ", v.orientation_quternion_3);
    s << indent << "orientation_quternion_4: ";
    Printer<double>::stream(s, indent + "  ", v.orientation_quternion_4);
    s << indent << "orientation_covariance[]" << std::endl;
    for (size_t i = 0; i < v.orientation_covariance.size(); ++i)
    {
      s << indent << "  orientation_covariance[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.orientation_covariance[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // PERCEPTION_MSGS_MESSAGE_IMU_MSG_H