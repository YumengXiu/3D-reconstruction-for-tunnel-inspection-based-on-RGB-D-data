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
To run Colmap, follow the instructions on [COLMAP SFM](https://colmap.github.io/) to install colmap and run it through either command line or GUI.
To input pose estimation to COLMAP:
run
```
python feedBagInput.py -h 
```
for instructions and follow it to extract data, feed pose.
After that, put the generated database file into colmap workspace, specify workspace and source input (images) to COLMAP and run the algorithm. 

## ASH
This method is based on [W. Dong, Y. Lao, M. Kaess and V. Koltun: ASH: A Modern Framework for Parallel Spatial Hashing in 3D Perception, arXiv, 2021.](https://arxiv.org/abs/2110.00511) and [Open3D](https://github.com/isl-org/Open3D). Follow the instruction [here](http://www.open3d.org/docs/release/getting_started.html) for the installation.

To run, checkout to `ASH/` and run belows,
```
python src/dense_slam_gui.py --config configs/tunnel_config.yml \   # or simulation_config.yml
                             --device cuda:0                        # or cpu:0 if no cuda device
```