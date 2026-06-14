import json, numpy as np
from search58 import gen_L0_stream, IP
sysv = np.array(json.load(open("sys_seed303_n57.json")), dtype=np.int32)
ext=0; cnt=0
for v in gen_L0_stream():
    cnt+=1
    if np.all(np.abs(sysv@np.array(v,dtype=np.int32))==IP): ext+=1
print("sys_seed303_n57.json scanned",cnt,"extenders(±2 with all 57):",ext,flush=True)
