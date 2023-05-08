#!/usr/bin/env python3

import rospy
import tf2_ros
import geometry_msgs.msg

tfBuffer = tf2_ros.Buffer()
tfListener = tf2_ros.TransformListener(tfBuffer)

def write_tf_to_file(file_path):
    try:
        transform = tfBuffer.lookup_transform("target_frame", "source_frame", rospy.Time(0))
        # target_frame and source_frame are the names of the frames you want to transform between
        # rospy.Time(0) means to get the latest available transform

        with open(file_path, 'a') as f:
            f.write("Transform from %s to %s:\n" % (transform.header.frame_id, transform.child_frame_id))
            f.write("Translation: x=%f, y=%f, z=%f\n" % (transform.transform.translation.x,
                                                          transform.transform.translation.y,
                                                          transform.transform.translation.z))
            f.write("Rotation: x=%f, y=%f, z=%f, w=%f\n\n" % (transform.transform.rotation.x,
                                                              transform.transform.rotation.y,
                                                              transform.transform.rotation.z,
                                                              transform.transform.rotation.w))
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        rospy.logerr("Failed to lookup transform!")

def write_tf_to_file(file_path):
    try:
        transform = tfBuffer.lookup_transform("target_frame", "source_frame", rospy.Time(0))
        # target_frame and source_frame are the names of the frames you want to transform between
        # rospy.Time(0) means to get the latest available transform

        with open(file_path, 'a') as f:
            f.write("Transform from %s to %s:\n" % (transform.header.frame_id, transform.child_frame_id))
            f.write("Translation: x=%f, y=%f, z=%f\n" % (transform.transform.translation.x,
                                                          transform.transform.translation.y,
                                                          transform.transform.translation.z))
            f.write("Rotation: x=%f, y=%f, z=%f, w=%f\n\n" % (transform.transform.rotation.x,
                                                              transform.transform.rotation.y,
                                                              transform.transform.rotation.z,
                                                              transform.transform.rotation.w))
    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        rospy.logerr("Failed to lookup transform!")

if __name__ == '__main__':
    rospy.init_node('tf_to_file')

    file_path = "/path/to/your/file.txt"

    rate = rospy.Rate(10) # 10 Hz
    while not rospy.is_shutdown():
        write_tf_to_file(file_path)
        rate.sleep()
