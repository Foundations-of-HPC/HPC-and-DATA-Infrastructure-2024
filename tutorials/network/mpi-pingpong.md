# MPI benchmark

With this kind of measure we wanto to assess the interconnect performance, using Infiniband netwrok and the Ethernet network. To do that we will use MPI, that with UCX is capable to exploit the RDMA capabilities offered by Infiniband switch and NIC.

A detailed guide could be found (on the official orfeo docs)[https://orfeo-doc.areasciencepark.it/examples/MPI-communication/], it depict also the latency and bandwith of commmunication inside the single node, conversely in the following section we will focus on the inter-node communication.

## Download and compile

**Allocate a pair of nodes**:
```bash
$ salloc -n2 -c 24 -N2 -p EPYC --time=1:0:0 --mem=50G
```

**Download**:
```bash
$ git clone --branch IMB-v2021.3 https://github.com/intel/mpi-benchmarks.git
$ cd mpi-benchmarks/src_c
``**

**Compile**:
```bash
$ module load openMPI/4.1.6/gnu
$ srun -n1 -N1 make
```

## Run using RDMA and UCX

By default the modular architecture of mpi will select the best interconnect available, in our case it will use Infiniband with UCX.

So we will run a pingpong to measure the network bandwidth, specifing:
- The maximum message length of 2^28 byte, so we hide the latency
- We map the processes by node, so we are sure to use the network

```bash
$ mpirun --map-by node ./IMB-MPI1 pingpong -msglog 28
#----------------------------------------------------------------
#    Intel(R) MPI Benchmarks 2018, MPI-1 part
#----------------------------------------------------------------
# Date                  : Mon Oct 21 19:31:05 2024
# Machine               : x86_64
# System                : Linux
# Release               : 6.10.3-200.fc40.x86_64
# Version               : #1 SMP PREEMPT_DYNAMIC Mon Aug  5 14:30:00 UTC 2024
# Calling sequence was:
# ./IMB-MPI1 pingpong -msglog 28
# Minimum message length in bytes:   0
# Maximum message length in bytes:   268435456
## MPI_Datatype                   :   MPI_BYTE
#---------------------------------------------------
# Benchmarking PingPong
# #processes = 2
#---------------------------------------------------
       #bytes #repetitions      t[usec]   Mbytes/sec
            0         1000         1.81         0.00
            1         1000         1.82         0.55
            2         1000         1.83         1.09
            4         1000         1.87         2.14
            8         1000         1.82         4.40
           16         1000         1.93         8.30
           32         1000         1.95        16.42
           64         1000         2.07        30.90
          128         1000         2.13        60.04
          256         1000         2.67        95.94
          512         1000         2.85       179.83
         1024         1000         3.00       341.10
         2048         1000         3.63       563.72
         4096         1000         4.50       909.57
         8192         1000         5.43      1508.06
        16384         1000         6.08      2692.89
        32768         1000         8.41      3896.02
        65536          640        11.50      5700.96
       131072          320        18.41      7119.99
       262144          160        28.80      9101.16
       524288           80        49.98     10490.71
      1048576           40        92.54     11331.17
      2097152           20       177.36     11824.56
      4194304           10       347.05     12085.60
      8388608            5       686.69     12216.08
     16777216            2      1366.01     12281.88
     33554432            1      2913.77     11515.80
     67108864            1      5620.89     11939.19
    134217728            1     10882.01     12333.91
    268435456            1     21932.48     12239.18
# All processes entering MPI_Finalize
```

**Results**:
*Latency**: We can see that the latency with message size 0 is ~ 1.8 usec. 
*Bandwith*: The maximum bandwith achived is ~ 12300 MB/s, it is near to the theretical given by the mellanox card of 100 Gb/s, that could be queried with the command `srun -n1 -N1 ibstatus`. 

## Using Ethernet protocol


We can repeat the test using the interface ``bond0`, is necessary to specify the value of the variable `UCX_NET_DEVICES`.

```bash
$ mpirun   --map-by node   -x UCX_NET_DEVICES=bond0 ./IMB-MPI1 pingpong -msglog 28#----------------------------------------------------------------
#    Intel(R) MPI Benchmarks 2018, MPI-1 part
#----------------------------------------------------------------
# Date                  : Mon Oct 21 19:56:40 2024
# Machine               : x86_64
# System                : Linux
# Release               : 6.10.3-200.fc40.x86_64
# Version               : #1 SMP PREEMPT_DYNAMIC Mon Aug  5 14:30:00 UTC 2024
# MPI Version           : 3.1
# Calling sequence was:
# ./IMB-MPI1 pingpong -msglog 28
# Minimum message length in bytes:   0
# Maximum message length in bytes:   268435456
#---------------------------------------------------
# Benchmarking PingPong
# #processes = 2
#---------------------------------------------------
       #bytes #repetitions      t[usec]   Mbytes/sec
            0         1000        16.20         0.00
            1         1000        15.89         0.06
            2         1000        16.34         0.12
            4         1000        16.22         0.25
            8         1000        16.26         0.49
           16         1000        16.15         0.99
           32         1000        16.25         1.97
           64         1000        16.40         3.90
          128         1000        16.57         7.72
          256         1000        17.03        15.03
          512         1000        17.19        29.78
         1024         1000        18.29        55.99
         2048         1000        26.10        78.46
         4096         1000        25.46       160.86
         8192         1000        31.12       263.24
        16384         1000        38.49       425.64
        32768         1000        51.18       640.27
        65536          640       122.12       536.67
       131072          320       177.73       737.46
       262144          160       221.77      1182.06
       524288           80       350.09      1497.57
      1048576           40       549.13      1909.51
      2097152           20       968.42      2165.55
      4194304           10      1987.41      2110.44
      8388608            5      3776.95      2221.00
     16777216            2      7763.19      2161.12
     33554432            1     14440.33      2323.66
     67108864            1     27415.11      2447.88
    134217728            1     54438.40      2465.50
    268435456            1    108141.03      2482.27
# All processes entering MPI_Finalize
```**

**Results**:
The results show a latency one order of magnitude higher respect RDMA version, precisely 16.20 usec, while the peak bandwith of ~2500 MB/s is near the peak performance of the 25Gb NIC.

