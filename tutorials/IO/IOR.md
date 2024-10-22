# IOR installation

```
$ git clone https://github.com/hpc/ior.git && cd ior 
$ git checkout 4.0.0 
$ ./bootstrap 
$ module load openMPI/4.1.5/gnu 
$ ./configure
$ make
```

# IOR Bandwidth

Common steps, allocation and module load:

```
$ salloc -N4 --exclusive -p EPYC  --time=0:30:0
$ module load openMPI/4.1.5/gnu 
$ cd ior/src
```

## First naive attemp

Use 16 processes per node, a single file shared among all mpi processes.

```
$ mpirun -np 64 --map-by node  ./ior -t 1m -b 64m -s 1

Results:
access    bw(MiB/s)  IOPS   
------    ---------  ----   
write     50.28      50.28  
read      1339.55    1339.58
```

The performance is very poor, since the file is shared among all processes.

## One file per process

The flag `-F` enable one file-per-process.
```
$ mpirun -np 64 --map-by node  ./ior -t 1m -b 64m -s 1 -F

Results:
access    bw(MiB/s)  IOPS
------    ---------  ----
write     34857      35170
read      378211     378737
```
The performance are now too high to be reliable. They are way more than theoretical peak performance.
This is due a cache effect, let's see how to tackle this problem. Could be a valid solution to write a file such that is notpossible to cache. Ipotetically larger than the nodes memory.

## Reorder task - avoid cache while reading

Or use a smarter way reordering the tasks `-C` .
Each process read the file of its neighbor, doing that we avoid caching effect while reaading.

```
$ mpirun -np 64 --map-by node  ./ior -t 1m -b 64m -s 4 -F -C

Results:

access    bw(MiB/s)  IOPS
------    ---------  ----
write     18528      18546
read      976.03     977.26
```

Please note that the write performance still to high.

Using the flag `-e` the cache is forced to be flushed. 

```
$ mpirun -np 64 --map-by node  ./ior -t 1m -b 64m -s 4 -F -C -e

Results:

access    bw(MiB/s)  IOPS
------    ---------  ----
write     2714.28    2714.69
read      3483.56    3486.54
```

The performance are now more plausible and realistic, they give us an idea of the underling infrastructure.

Finally, it is possible to repeat the tests several time to collect statistc using the flag `-i`.

```
$ mpirun -np 64 --map-by node  ./ior -t 1m -b 64m -s 4 -F -C -e -i 10
Summary of all tests:
Operation   Max(MiB)   Min(MiB)  Mean(MiB)     StdDev   Max(OPs)   Min(OPs)  Mean(OPs)     StdDev    Mean(s) 
write        2919.08    2514.20    2715.98     109.28    2919.08    2514.20    2715.98     109.28    6.04223 
read         3589.55    3255.40    3406.18     117.42    3589.55    3255.40    3406.18     117.42    4.81577 
```

## Try to squeeze out performance from our filesystem


### Scratch

Add the StoneWall flag to avoid that slowest process can impact on performance and request more nodes.

Do it on scratch :

```
$ mpirun -npernode 32 ./ior -t 1m -b 8m -s 2000 -D 30 -F -C -e -g -O stoneWallingWearOut=1 -i 12

Summary of all tests:
Operation   Max(MiB)   Min(MiB)  Mean(MiB)     StdDev   Max(OPs)   Min(OPs)  Mean(OPs)     StdDev
write        4878.94    4429.27    4615.66     135.87    4878.94    4429.27    4615.66     135.87
read         4964.75    4653.93    4817.86      97.67    4964.75    4653.93    4817.86      97.67
```

### Fast

And fast, using the flas `-o` to select a custom path. 

```
$ mpirun -npernode 16 ./ior -t 8m -b 8m -s 2000 -D 30 -F -C -e -g -O stoneWallingWearOut=1 -i 12 -o /fast/area/ntosato/test 

Summary of all tests:
Operation   Max(MiB)   Min(MiB)  Mean(MiB)     StdDev   Max(OPs)   Min(OPs)  Mean(OPs)     StdDev
write        5818.53    3803.91    4676.19     571.38     727.32     475.49     584.52      71.42
read        12713.33   11001.65   11933.88     470.47    1589.17    1375.21    1491.73      58.81

```

### Home filesystem

```
$ mpirun -np 72  ./ior -t 8m -b 512m -s 6 -a MPIIO -v -i 10  -F -C -e -o /orfeo/cephfs/home/area/ntosato/test

Summary of all tests:
Operation   Max(MiB)   Min(MiB)  Mean(MiB)     StdDev   Max(OPs)   Min(OPs)  Mean(OPs)     StdDev
write        1564.87    1428.33    1499.89      42.61     195.61     178.54     187.49       5.33
read         4620.71    2973.13    3813.08     503.23     577.59     371.64     476.64      62.90
```
### Local scratch

Since `/local_scratch` is local, doesn't make sense to read the files of the neighbor, so perform only a write test.
```
$ mpirun -npernode 16 ./ior -t 8m -b 8m -s 500 -D 30 -F -w -e -g -O stoneWallingWearOut=1 -o /local_scratch/test

Results:
access    bw(MiB/s)  IOPS
------    ---------  ----
write     1037.91    1038.00

```

# IOPS measure

To measure the IOPS we will tune the IOR parameter according the defintion of IOPS:
 - Transfer randomly the data `-z`
 - Use the smallest amount of data available -t 4k
 - Avoid the use of the cache with `--posix.odirect `

## Measure write IOPS

### Fast

```
$ mpirun -npernode 128 ./ior -F -C -e -g -b 1m -t 4k -s6 -D45 -w -z --posix.odirect -l random -i 10 -o /fast/area/ntosato/test

Summary of all tests:
Operation   Max(MiB)   Min(MiB)  Mean(MiB)     StdDev   Max(OPs)   Min(OPs)  Mean(OPs)
write         314.67     188.81     264.35      41.68   80555.34   48335.38   67673.61
```

### Scratch ~


```
$ mpirun -npernode 128 ./ior -F -C -e -g -b 1m -t 4k -s6 -D45 -w -z --posix.odirect -l random -i 10

Summary of all tests:
Operation   Max(MiB)   Min(MiB)  Mean(MiB)     StdDev   Max(OPs)   Min(OPs)  Mean(OPs)     StdDev
write          20.87      17.64      18.97       0.92    5343.75    4515.07    4856.69     236.37
```

## Measure read IOPS

First generate the data and then read.

```
$ mpirun -npernode 128 --map-by node ./ior -F -C -e -g -b 1m -t 4k -s 1 -w -k -z  -i 1 -o /fast/area/ntosato/test

$ mpirun -npernode 128 --map-by node ./ior -F -C -e -g -b 1m -t 4k  -D 25 -r -z -l random -i 10 -o /fast/area/ntosato/test
```

## How to not measure

```
$ mpirun -npernode 128  ./ior -F -e -g -b 1m -t 4k -s6 -D45  -w -z  -i 1

Results:

access    bw(MiB/s)  IOPS       Latency(s)  block(KiB) xfer(KiB)  open(s)    wr/rd(s)   close(s)   total(s)   iter
------    ---------  ----       ----------  ---------- ---------  --------   --------   --------   --------   ----
write     2917.01    777864     0.003619    1024.00    4.00       0.063059   1.52       0.000121   1.58       0

```

# Metadata test

## File operation

### Home

```
[ntosato@login01 src]$ srun -N10 --tasks-per-node 24  ./mdtest -n 100 -F -i 10 -C -T -r -u -d /u/area/ntosato/

SUMMARY rate: (of 10 iterations)
   Operation                     Max            Min           Mean        Std Dev
   ---------                     ---            ---           ----        -------
   File creation               13569.541      10008.703      11630.367       1135.798
   File stat                 1160544.352     999705.004    1067745.405      54524.347
   File removal                11536.326       8171.592       9221.775        959.603
```

### Scratch

```
$ srun -N10 --tasks-per-node 24  ./mdtest -n 100 -F -i 10 -C -T -r -u

SUMMARY rate: (of 10 iterations)
   Operation                     Max            Min           Mean        Std Dev
   ---------                     ---            ---           ----        -------
   File creation               13266.229       9995.831      11196.186       1077.320
   File stat                 1760432.591    1409040.971    1578904.628     121489.583
   File read                       0.000          0.000          0.000          0.000
   File removal                 9677.017       8261.058       8886.967        476.524
```

### Fast

```
$ srun -N10 --tasks-per-node 24  ./mdtest -n 100 -F -i 10 -C -T -r -u -d /fast/area/ntosato/

SUMMARY rate: (of 10 iterations)
   Operation                     Max            Min           Mean        Std Dev
   ---------                     ---            ---           ----        -------
   File creation               11113.117       9503.938      10201.188        572.270
   File stat                 1209241.348    1065253.881    1134152.213      44100.453
   File read                       0.000          0.000          0.000          0.000
   File removal                 7663.792       7087.840       7355.955        205.800
```

## Directory operation

### Scratch 

```
$ srun -N10 --tasks-per-node 24  ./mdtest -n 100 -D -i 10 -C -T -r -u
SUMMARY rate: (of 10 iterations)
   Operation                     Max            Min           Mean        Std Dev
   ---------                     ---            ---           ----        -------
   Directory creation          11338.918       9201.428      10176.229        638.724
   Directory stat            1457916.404    1150858.554    1348808.262      99696.175
   Directory removal            8010.133       7327.041       7634.967        187.638
```
### Fast

```
$ srun -N10 --tasks-per-node 24  ./mdtest -n 100 -D -i 10 -C -T -r -u -d /fast/area/ntosato/
SUMMARY rate: (of 10 iterations)
   Operation                     Max            Min           Mean        Std Dev
   ---------                     ---            ---           ----        -------
   Directory creation          12435.608      10512.106      11385.986        596.846
   Directory stat            1196890.707    1093833.355    1131034.540      39114.990
   Directory removal            7742.537       6309.447       7113.125        462.393
-- finished at 05/09/2024 02:04:15 --
```
### Home

```
$ srun -N10 --tasks-per-node 24  ./mdtest -n 100 -D -i 10 -C -T -r -u -d /u/area/ntosato/
SUMMARY rate: (of 10 iterations)
   Operation                     Max            Min           Mean        Std Dev
   ---------                     ---            ---           ----        -------
   Directory creation          12059.907       9153.985      10090.489        857.738
   Directory stat            1003012.086     214408.513     824791.487     218962.433
   Directory removal            8189.212       7359.462       7797.126        256.542

```
