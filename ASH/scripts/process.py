import os
import cv2
import numpy as np

for data_name in ['../data/tunnel/inspection','../data/simulation/zigzag','../data/simulation/reconstruct','../data/simulation/rgbd_wrapper']:
    for folder_name in ['color','depth']:
        paths=[[] for _ in range(4)]
        for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__),data_name,folder_name), topdown=True):
            for name in files:
                n_digit=len(name.split('_')[0])-1
                paths[n_digit if n_digit<4 else -1].append((root,name))
        idx=1
        for l in paths:
            for p in sorted(l):
                ext=p[1].split('.')[-1]
                old_path=os.path.join(*p)
                new_path=os.path.join(p[0],f'{idx:0>4d}.{ext}')
                # print(p[1],f'{idx:0>4d}.{ext}')
                if folder_name=='depth':
                    im=cv2.imread(old_path, cv2.IMREAD_UNCHANGED)
                    if im.dtype==np.uint8:
                        im=im.astype(np.uint16)*255
                    if len(im.shape)>2 and im.shape[2]>1:
                        im=im[:,:,0]
                    os.remove(old_path)
                    cv2.imwrite(new_path,im.astype(np.uint16))
                    # print(im.max())
                else:
                    os.rename(old_path,new_path)
                idx+=1