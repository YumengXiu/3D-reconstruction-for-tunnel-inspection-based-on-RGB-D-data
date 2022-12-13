import os

sep_idx=[38*i for i in range(1,6)]
data_name ='../data/tunnel/inspection'
for folder_name in ['color','depth']:
    for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__),data_name,folder_name), topdown=True):
        for name in files:
            idx = int(name.split('.')[0])
            for i in range(1,6):
                new_data_name=data_name+f'_{i}'
                new_root=os.path.join(os.path.dirname(__file__),new_data_name,folder_name)
                if not os.path.exists(new_root):
                    os.system(f'mkdir -p {new_root}')
                if idx<=sep_idx[i-1]:
                    os.system(f'cp {os.path.join(root,name)} {os.path.join(new_root,name)}')  
