import os
import yaml
import rosbag
import cv2
from cv_bridge import CvBridge
import numpy as np
from utils.database import COLMAPDatabase

import argparse

# this file must be put in the colmap workspace, at the same dir as images.
# also, the data .bag file must be in the same dirs

TOPIC_COLOR = "/camera/color/image_raw_t"
TOPIC_DEPTH = "/camera/depth/image_rect_raw_t"

def get_poses(bag, args):

    TOPIC = "/mavros/local_position/pose"
    pose_topic = bag.read_messages(TOPIC)
    length = bag.get_message_count(TOPIC)
    
    print("-" * 80)
    print("Total POSE number: {}, downsampling to {}".format(length, args.num_images))
    
    poses = []
    for k, b in enumerate(pose_topic):
        if k % (length // args.num_images) == 0 and k < (length // args.num_images) * args.num_images:
            poses.append(
                [
                b.message.pose.orientation.w,
                b.message.pose.orientation.x,
                b.message.pose.orientation.y,
                b.message.pose.orientation.z,
                b.message.pose.position.x,
                b.message.pose.position.y,
                b.message.pose.position.z    
                ]
            )
    return poses

def get_intrinsics(downsample_h, downsample_w):
    
    height, width = 720, 1280 # the original d435i rgb camera output height and width
    K = [912.1310424804688, 0.0, 636.2242431640625, 0.0, 912.2687377929688, 351.17333984375, 0.0, 0.0, 1.0] # camera instrinsics 
    scale = downsample_h / height
    
    camera = [
        downsample_w,
        downsample_h,
        K[0] * scale, # focal_x
        K[4] * scale, # focal_y
        int(K[2] * scale), # principal point x
        int(K[5] * scale), # principal point y
    ]
    
    return camera
        

def create_database(args, poses, camera, names):
    """ 
    create sqlite 3 database
    inputs:
        poses: list of lists containing drone pose at each keypoint
        intrinsics: extracted intrinsics with scale correction
    outputs:
        creates a "database.db" for colmap
    """

    database_path = os.path.join(args.export_path, "database.db")
    db = COLMAPDatabase.connect(database_path)
    db.create_tables()

    # Create camera 
    print(camera[2:])
    model, width, height, params = \
        1, camera[0], camera[1], camera[2:]

    camera_id1 = db.add_camera(model, width, height, params)

    # Create images.
    for i in range(args.num_images):
        db.add_image(names[i], camera_id1, prior_q=np.array(poses[i][:4]), prior_t=np.array(poses[i][4:]))

    db.commit()
    db.close()


if __name__ == "__main__":
    

    parser = argparse.ArgumentParser(description="Read rosbag, extract rgbd images and import pose into database")

    parser.add_argument(
        "-i", "--input_path", type=str, help="path to bag file", required=True
    )
    parser.add_argument(
        "-e",
        "--export_path",
        type=str,
        help="path to extracted RGB and Depth images",
        required=True,
    )
    parser.add_argument(
        "-n",
        "--num_images",
        type=int,
        help="number of images desired for extraction",
        default=50,
    )
    parser.add_argument(
        "-s", "--scale_percent", type=int, default=60, help="downsampling scale"
    )
    parser.add_argument(
        "--rgb_only", help="only extract rgb to reduce time", action="store_true"
    )

    args = parser.parse_args()

    os.makedirs(os.path.join(args.export_path, "images"), exist_ok=True)
    os.makedirs(os.path.join(args.export_path, "depth"), exist_ok=True)

    bag = rosbag.Bag(args.input_path)

    info_dict = yaml.load(
        rosbag.Bag(args.input_path, "r")._get_yaml_info(), Loader=yaml.Loader
    )

    if not args.rgb_only: # extract depth images
        
        DESCRIPTION = "depth_"
        image_topic = bag.read_messages(TOPIC_DEPTH)
        length = bag.get_message_count(TOPIC_DEPTH)
        print("-" * 80)
        print("Total image number: {}, downsampling to {}".format(length, args.num_images))

        for k, b in enumerate(image_topic):
            if k % (length // args.num_images) == 0 and k < (length // args.num_images) * args.num_images:
                bridge = CvBridge()
                cv_image = bridge.imgmsg_to_cv2(b.message, b.message.encoding)
                cv_image.astype(np.uint8)

                depth_colormap = cv2.applyColorMap(
                    cv2.convertScaleAbs(cv_image, alpha=0.03), cv2.COLORMAP_JET
                )
                cv2.imwrite(
                    os.path.join(args.export_path, "depth", str(b.timestamp) + ".png"),
                    depth_colormap,
                )

                print("saved: " + DESCRIPTION + str(b.timestamp) + ".png")

    # saved_name, h, w = extract_rgb(bag, args)
    
    DESCRIPTION = "color_"
    image_topic = bag.read_messages(TOPIC_COLOR)
    length = bag.get_message_count(TOPIC_COLOR)
    print("-" * 80)
    print("Total image number: {}, downsampling to {}".format(length, args.num_images))
    saved_name = []
    for k, b in enumerate(image_topic):
        if k % (length // args.num_images) == 0 and k < (length // args.num_images) * args.num_images:
            bridge = CvBridge()
            cv_image = bridge.imgmsg_to_cv2(b.message, b.message.encoding)
            cv_image = cv2.cvtColor(cv_image,cv2.COLOR_RGB2BGR)# simulation?
            scale_percent = args.scale_percent  # percent of original size
            width = int(cv_image.shape[1] * scale_percent / 100)
            height = int(cv_image.shape[0] * scale_percent / 100)
            cv_image = cv2.resize(cv_image, (width, height))
            cv_image.astype(np.uint8)
            
            saved_name.append(str(b.timestamp) + ".png") # for images.txt
            
            output_path = os.path.join(args.export_path, "images", str(b.timestamp) + ".png")
            cv2.imwrite(
                output_path,
                cv_image,
            )

            print("saved: " + DESCRIPTION + str(b.timestamp) + ".png")

            
    
    poses = get_poses(bag, args)
    camera = get_intrinsics(height, width)
    create_database(args, poses, camera, saved_name)
    

    bag.close()

    print("rosbag info has been extracted. Poses are feeded into database")
