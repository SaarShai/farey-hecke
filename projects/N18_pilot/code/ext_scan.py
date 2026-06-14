import json, numpy as np, sys
from search58 import gen_L0_stream, IP
for fn in ["sys_seed304_n57.json","sys_seed303_n57.json"]:
    sysv = np.array(json.load(open(fn)), dtype=np.int32)
    ext=[]; cnt=0
    for v in gen_L0_stream():
        cnt+=1
        va=np.array(v,dtype=np.int32); d=sysv@va
        if np.all(np.abs(d)==IP): ext.append(v)
    print(fn,"scanned",cnt,"extension-candidates(±2 with all 57):",len(ext),flush=True)
    if ext: print("  examples:",ext[:2],flush=True)
