# This tutorial explores  some of  the hardware components of a DGX station 



#top vs  htop

Let us explore load and processeses with top: 

```

root@dgx002:~# top
top - 09:48:36 up 55 days, 13:40,  3 users,  load average: 0,67, 1,04, 1,18
Tasks: 2498 total,   1 running, 2497 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0,0 us,  0,2 sy,  0,0 ni, 99,8 id,  0,0 wa,  0,0 hi,  0,0 si,  0,0 st
MiB Mem : 1031843,+total, 733339,5 free,  10587,5 used, 287917,0 buff/cache
MiB Swap:      0,0 total,      0,0 free,      0,0 used. 1015339,+avail Mem

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   9490 root      20   0  475964  83136   7548 S  32,2   0,0  26856:06 nv-hostengine
 977281 root      20   0    9,8g 990004  21616 S  13,5   0,1  69:12.36 nvsm_core
2582137 root      20   0   15876   6796   3348 R   1,3   0,0   0:00.54 top
  14472 root      20   0 9149772  47352   9132 S   0,7   0,0 265:56.32 nvsm_api_gatewa
     15 root      20   0       0      0      0 I   0,3   0,0  79:41.87 rcu_sched
   3119 root      20   0       0      0      0 S   0,3   0,0 103:47.55 nvswi1
   3152 root      39  19       0      0      0 S   0,3   0,0 741:49.46 kipmi0
   3246 root      20   0       0      0      0 S   0,3   0,0 103:35.58 nvswi3
  10499 root      20   0   18452  10708   6528 S   0,3   0,0  45:55.64 mosquitto
 333273 zabbix    20   0   38552   3908   2620 S   0,3   0,0   1:10.73 zabbix_agentd
2554586 root      20   0       0      0      0 I   0,3   0,0   0:00.38 kworker/u513:4-writeback
      1 root      20   0  168648  12292   6384 S   0,0   0,0   3:23.36 systemd
      2 root      20   0       0      0      0 S   0,0   0,0   0:35.41 kthreadd
      3 root       0 -20       0      0      0 I   0,0   0,0   0:00.00 rcu_gp
      4 root       0 -20       0      0      0 I   0,0   0,0   0:00.00 rcu_par_gp

```

A more advanced command is htop:

```


Other commands to test 


## hwloc commands 


## lspci commands to identify all the disks/network cards/gpus


##nvidia-smi set of commands
  nvidia nvlink
  nvidia   

##
