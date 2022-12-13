rm ~/16833/project/data/tunnel/inspection/color/*
cp ./color/* ~/16833/project/data/tunnel/inspection/color/
rm ~/16833/project/data/tunnel/inspection/depth/*
cp ./rgbd1/* ~/16833/project/data/tunnel/inspection/depth/

cd /home/brianzx/16833/project/data/simulation/
rm -rf *

mkdir zigzag && cd zigzag
unzip ../../simulation_zigzag.zip
mv rgbd/ depth/

mkdir ../reconstruct && cd ../reconstruct
unzip ../../hand_reconstruct_V.zip
mv rgbd/ depth/

mkdir ../rgbd_wrapper && cd ../rgbd_wrapper
unzip ../../rgbd_wrapper.zip
mv rgbd/ depth/

/usr/bin/python3 /home/brianzx/16833/project/scripts/process.py

cd /home/brianzx/16833/project/data/simulation/zigzag/color/
rm 0121.png 0122.png 
mogrify -format jpg *.png
rm *.png
