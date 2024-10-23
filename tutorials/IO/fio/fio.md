# FIO - flexible IO tester

To have the details, look the file in this folder. They contain the blocksize, the benchmark setup and so on.

## Raw storage - HDD

```bash
$ fio raw-spin.fio
...
Run status group 0 (all jobs):
  WRITE: bw=253MiB/s (265MB/s), 253MiB/s-253MiB/s (265MB/s-265MB/s), io=2544MiB (2668MB), run=10049-10049msec

Run status group 1 (all jobs):
   READ: bw=253MiB/s (265MB/s), 253MiB/s-253MiB/s (265MB/s-265MB/s), io=2544MiB (2668MB), run=10058-10058msec

Disk stats (read/write):
  sda: ios=3823/4293, sectors=5087712/5210112, merge=0/0, ticks=212909/241225, in_queue=454134, util=98.74%
```
The bandwidth obtained match with the theoretical one and with the measure done with `dd`.

## Raw storage - NVME

```bash
$ fio raw-nvme.fio
Run status group 0 (all jobs):
  WRITE: bw=6504MiB/s (6820MB/s), 6504MiB/s-6504MiB/s (6820MB/s-6820MB/s), io=16.0GiB (17.2GB), run=2519-2519msec

Run status group 1 (all jobs):
   READ: bw=6125MiB/s (6422MB/s), 6125MiB/s-6125MiB/s (6422MB/s-6422MB/s), io=16.0GiB (17.2GB), run=2675-2675msec

Run status group 2 (all jobs):
  WRITE: bw=6454MiB/s (6768MB/s), 6454MiB/s-6454MiB/s (6768MB/s-6768MB/s), io=32.0GiB (34.4GB), run=5077-5077msec

Run status group 3 (all jobs):
   READ: bw=6805MiB/s (7136MB/s), 6805MiB/s-6805MiB/s (7136MB/s-7136MB/s), io=32.0GiB (34.4GB), run=4815-4815msec
```

This test write and read first using one single processes and then 2 processes. Using more proccesses the read bandwidth is near to the maximum performance available.

## HDD with XFS

```bash
$ mkfs.xfs /dev/sda
$ mount /dev/sda /mnt/mydisk
$ fio fs-spin.fio
Run status group 0 (all jobs):
  WRITE: bw=248MiB/s (260MB/s), 248MiB/s-248MiB/s (260MB/s-260MB/s), io=4984MiB (5226MB), run=20068-20068msec

Run status group 1 (all jobs):
   READ: bw=251MiB/s (263MB/s), 251MiB/s-251MiB/s (263MB/s-263MB/s), io=5024MiB (5268MB), run=20054-20054msec

Disk stats (read/write):
  sda: ios=9931/7482, sectors=10169344/10207352, merge=0/4, ticks=90007/73153, in_queue=163160, util=98.60%
```

## NVME with XFS

```bash
$ fio fs-nvme.fio

Run status group 0 (all jobs):
  WRITE: bw=6464MiB/s (6778MB/s), 6464MiB/s-6464MiB/s (6778MB/s-6778MB/s), io=40.0GiB (42.9GB), run=6337-6337msec

Run status group 1 (all jobs):
   READ: bw=6335MiB/s (6642MB/s), 6335MiB/s-6335MiB/s (6642MB/s-6642MB/s), io=40.0GiB (42.9GB), run=6466-6466msec

Run status group 2 (all jobs):
  WRITE: bw=6420MiB/s (6731MB/s), 6420MiB/s-6420MiB/s (6731MB/s-6731MB/s), io=80.0GiB (85.9GB), run=12761-12761msec

Run status group 3 (all jobs):
   READ: bw=6809MiB/s (7139MB/s), 6809MiB/s-6809MiB/s (7139MB/s-7139MB/s), io=80.0GiB (85.9GB), run=12032-12032msec
```

## Controller raid test

To test the raid controller, we write and read from all the disk at the same time, and we read the aggregated bandwithd.


```bash
$ fio all_disk.fio
Starting 12 processes
Jobs: 12 (f=12): [W(12)][100.0%][w=3063MiB/s][w=765 IOPS][eta 00m:00s]
Write_sda: (groupid=0, jobs=12): err= 0: pid=241200: Wed Oct 23 08:59:57 2024
  write: IOPS=766, BW=3067MiB/s (3216MB/s)(60.1GiB/20066msec); 0 zone resets
    slat (usec): min=161, max=162702, avg=767.12, stdev=3826.34
    clat (msec): min=4, max=208, avg=61.74, stdev= 8.24
     lat (msec): min=6, max=209, avg=62.51, stdev= 8.05
    clat percentiles (msec):
     |  1.00th=[   40],  5.00th=[   56], 10.00th=[   57], 20.00th=[   58],
     | 30.00th=[   59], 40.00th=[   60], 50.00th=[   62], 60.00th=[   63],
     | 70.00th=[   64], 80.00th=[   66], 90.00th=[   69], 95.00th=[   72],
     | 99.00th=[   85], 99.50th=[   99], 99.90th=[  155], 99.95th=[  167],
     | 99.99th=[  194]
   bw (  MiB/s): min= 2584, max= 3344, per=100.00%, avg=3070.41, stdev=15.25, samples=480
   iops        : min=  646, max=  836, avg=767.60, stdev= 3.81, samples=480
  lat (msec)   : 10=0.06%, 20=0.29%, 50=1.28%, 100=97.89%, 250=0.47%
  cpu          : usr=2.08%, sys=1.22%, ctx=16205, majf=0, minf=150
  IO depths    : 1=0.1%, 2=0.2%, 4=99.8%, 8=0.0%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwts: total=0,15388,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=4

Run status group 0 (all jobs):
  WRITE: bw=3067MiB/s (3216MB/s), 3067MiB/s-3067MiB/s (3216MB/s-3216MB/s), io=60.1GiB (64.5GB), run=20066-20066msec
```

## Write to all nvme

```bash
Starting 2 processes
Jobs: 2 (f=2)
Write_nvme: (groupid=0, jobs=2): err= 0: pid=241320: Wed Oct 23 09:01:19 2024
  write: IOPS=1550, BW=12.1GiB/s (13.0GB/s)(32.0GiB/2641msec); 0 zone resets
    slat (usec): min=319, max=1388, avg=834.62, stdev=130.07
    clat (usec): min=3719, max=16635, avg=9310.87, stdev=787.07
     lat (usec): min=4149, max=17370, avg=10145.48, stdev=788.48
    clat percentiles (usec):
     |  1.00th=[ 8848],  5.00th=[ 8979], 10.00th=[ 8979], 20.00th=[ 8979],
     | 30.00th=[ 9110], 40.00th=[ 9110], 50.00th=[ 9110], 60.00th=[ 9241],
     | 70.00th=[ 9241], 80.00th=[ 9241], 90.00th=[ 9372], 95.00th=[11469],
     | 99.00th=[11994], 99.50th=[12518], 99.90th=[15139], 99.95th=[15401],
     | 99.99th=[16581]
   bw (  MiB/s): min=12496, max=12640, per=100.00%, avg=12604.80, stdev=29.60, samples=10
   iops        : min= 1562, max= 1580, avg=1575.60, stdev= 3.70, samples=10
  lat (msec)   : 4=0.12%, 10=92.77%, 20=7.10%
  cpu          : usr=40.75%, sys=22.37%, ctx=4066, majf=0, minf=27
  IO depths    : 1=0.1%, 2=0.1%, 4=0.2%, 8=99.7%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=100.0%, 8=0.1%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwts: total=0,4096,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=8

Run status group 0 (all jobs):
  WRITE: bw=12.1GiB/s (13.0GB/s), 12.1GiB/s-12.1GiB/s (13.0GB/s-13.0GB/s), io=32.0GiB (34.4GB), run=2641-2641msec

Disk stats (read/write):
  nvme1n1: ios=0/17349, sectors=0/30738432, merge=0/235, ticks=0/150521, in_queue=150521, util=94.44%
  nvme2n1: ios=0/18863, sectors=0/32976336, merge=0/0, ticks=0/169349, in_queue=169349, util=95.09%
```

