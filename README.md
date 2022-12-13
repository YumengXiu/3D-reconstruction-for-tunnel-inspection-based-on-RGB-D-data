# 3D-reconstruction-for-tunnel-inspection-based-on-RGB-D-data
16833 final Project


## NeRF-based Method
NeRF-based method is based on [NICE-SLAM repo](https://github.com/cvg/nice-slam). First follow the readme of [NICE-SLAM repo](https://github.com/cvg/nice-slam) to install all the requirement and run the [demo](https://github.com/cvg/nice-slam#demo) successfully.

Then prepare the data of tunnel in the same format of ScanNet (the one used in the deme above). Change the path `cd  nerf-based` and run the following command to run the NeRF-based SLAM. To run the simulation, run `python -W ignore run.py  configs/Demo/new_sim.yaml --nice` instead.

```
python -W ignore run.py configs/Demo/new.yaml --imap
```

To visualize the results of tracking and mapping, run the following with the real data. For the simulation, run `python visualizer.py configs/Demo/new_sim.yaml --nice --no_gt_traj --save_rendering` instead.

```
python visualizer.py configs/Demo/new.yaml --imap --no_gt_traj --save_rendering
```

## SfM-based Method
This method is based on [COLMAP SFM](https://colmap.github.io/). Follow the readme to install Colmap and run it. feedBagInput.py is the file to extract rgb images as well as poses and then feed the pose into the colmap database. Note that in this process, make sure the data(.bag), image dir and colmap workspace are in same dir.
To run Colmap, follow the instructions on [COLMAP SFM](https://colmap.github.io/).
To input pose estimation to COLMAP:
run
```
python feedBagInput.py -h 
```
for instructions and follow it to extract data, feed pose
