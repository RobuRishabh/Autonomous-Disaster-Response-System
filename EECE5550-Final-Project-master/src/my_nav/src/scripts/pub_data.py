#!/usr/bin/env python

import rospy
import tf2_ros
import tf2_geometry_msgs
import tf2_msgs.msg
from geometry_msgs.msg import TransformStamped


def publish_transforms(file_path):
    # Initialize node
    rospy.init_node('transform_publisher')

    # Initialize transform buffer and broadcaster
    tfBuffer = tf2_ros.Buffer()
    tfBroadcaster = tf2_ros.StaticTransformBroadcaster()

    # Read transforms from file
    with open(file_path, 'r') as f:
        transform_lines = f.readlines()

    # Create TFMessage object
    tfMessage = tf2_msgs.msg.TFMessage()

    # Parse transform lines and add them to TFMessage
    for line in transform_lines:
        if line.startswith('Transform from'):
            frame_ids = line.split(' ')[-3:]
            translation_line = transform_lines.pop(0)
            rotation_line = transform_lines.pop(0)
            translation = [float(x.split('=')[1]) for x in translation_line.split(', ')]
            rotation = [float(x.split('=')[1]) for x in rotation_line.split(', ')]
            transform = TransformStamped()
            transform.header.frame_id = frame_ids[0]
            transform.child_frame_id = frame_ids[2][:-2]  # Remove trailing colon from child frame ID
            transform.transform.translation.x = translation[0]
            transform.transform.translation.y = translation[1]
            transform.transform.translation.z = translation[2]
            transform.transform.rotation.x = rotation[0]
            transform.transform.rotation.y = rotation[1]
            transform.transform.rotation.z = rotation[2]
            transform.transform.rotation.w = rotation[3]
            tfMessage.transforms.append(transform)

    # Publish TFMessage
    tfBroadcaster.sendTransform(tfMessage.transforms)

    # Sleep briefly to allow time for transforms to be broadcast
    rospy.sleep(0.5)

    # Transform frames and display in RViz
    for transform in tfMessage.transforms:
        try:
            transformed_point = tf2_geometry_msgs.do_transform_point((0, 0, 0), transform)
            rviz_marker = rospy.Publisher('/visualization_marker', Marker, queue_size=1)
            marker = Marker()
            marker.header.frame_id = transform.child_frame_id
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose.position = transformed_point.point
            marker.scale.x = 0.1
            marker.scale.y = 0.1
            marker.scale.z = 0.1
            marker.color.a = 1.0
            marker.color.r = 1.0
            rviz_marker.publish(marker)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            rospy.logerr("Failed to transform frame %s to %s!" % (transform.child_frame_id, transform.header.frame_id))


if __name__ == '__main__':
    file_path = 'path/to/transform/file.txt'
    publish_transforms(file_path)
