# Measuring the network bandwith with IPERF3

From the man: `iperf3  is a tool for performing network throughput measurements.  It can test TCP, UDP, or SCTP throughput.  To perform an iperf3 test the user must establish both a server and a client.`

Differently from MPI with RDMA, it aim to test the TCP/IP stack performance, we will test the ipoib protocol, that implement the TPC/IP layer over the Infiniband transport layer and the legacy stack using the Ethernet interfaces.

## Get iperf3

On a compute node, download ad compile iperf3 from source:

```bash
$ git clone https://github.com/esnet/iperf.git
$ cd iperf && git checkout 3.17.1
$ ./configure
$ make -j 4
```

## Start server
As showed in the previous tutorial, if you want to inspect the interfaces use the command `ip a` to discover the link layer type.

We will use the addresses `10.128.2.xxx` to test the Ethernet and `10.128.6.xxx` to test Infiniband.

So start a server on the desired interface and port:

```bash
$  cd src/
$ ./iperf3 -s 10.128.2.128 -p 12345
-----------------------------------------------------------
Server listening on 12345 (test #1)
-----------------------------------------------------------

```
## Start client

Start on another node an iperf3 client, with the flag `-n 10T`, that ask to perf to transfer 10 terabytes of data.

### Ethernet interface

To test the ethernet interface we will use the following command:

```bash
$ ./iperf3 -c 10.128.2.128 -p 12345 -n 10T
Connecting to host 10.128.2.128, port 12345
[  5] local 10.128.2.125 port 36142 connected to 10.128.2.128 port 12345
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  2.65 GBytes  22.8 Gbits/sec   45   1.31 MBytes
[  5]   1.00-2.00   sec  2.73 GBytes  23.4 Gbits/sec    0   1.33 MBytes
[  5]   2.00-3.00   sec  2.72 GBytes  23.3 Gbits/sec    0   1.35 MBytes
[  5]   3.00-4.00   sec  2.73 GBytes  23.5 Gbits/sec   41   1.21 MBytes
[  5]   4.00-5.00   sec  2.73 GBytes  23.4 Gbits/sec    0   1.31 MBytes
[  5]   5.00-6.00   sec  2.73 GBytes  23.4 Gbits/sec    0   1.32 MBytes
```

We can see that the results are coherent with the ones obtained with MPI and with the theoretical peak performance.

### Infiniband interface

Now restart the server on the address that use the infiniband card, and test again the connection:

**Server:**
```bash
$ ./iperf3 -s 10.128.6.128 -p 12345
-----------------------------------------------------------
Server listening on 12345 (test #1)
-----------------------------------------------------------
```


**Client**:
```bash
$ ./iperf3 -c 10.128.6.128 -p 12345 -n 10T
Connecting to host 10.128.6.128, port 12345
[  5] local 10.128.6.125 port 58696 connected to 10.128.6.128 port 12345
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  2.60 GBytes  22.3 Gbits/sec  230    700 KBytes
[  5]   1.00-2.00   sec  2.71 GBytes  23.3 Gbits/sec    0    745 KBytes
[  5]   2.00-3.00   sec  2.65 GBytes  22.8 Gbits/sec    0    829 KBytes
[  5]   3.00-4.00   sec  2.64 GBytes  22.7 Gbits/sec    0    829 KBytes
```

This is not a satisfing result, sice the maximum bandwith shoudl be around 100Gb/s. The reason is that we are CPU limited. To exploit all the bandwith, let's try to increment the number of client and look at the aggregated bandwith.

```bash
$ ./iperf3 -c 10.128.6.128 -p 12345 -n 10T --parallel 4
$ ./iperf3 -c 10.128.6.128 -p 12345 -n 10T --parallel 4
Connecting to host 10.128.6.128, port 12345
[  5] local 10.128.6.125 port 56504 connected to 10.128.6.128 port 12345
[  7] local 10.128.6.125 port 56516 connected to 10.128.6.128 port 12345
[ 10] local 10.128.6.125 port 56528 connected to 10.128.6.128 port 12345
[ 12] local 10.128.6.125 port 56544 connected to 10.128.6.128 port 12345
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  2.38 GBytes  20.4 Gbits/sec  435    792 KBytes
[  7]   0.00-1.00   sec  3.00 GBytes  25.7 Gbits/sec  772    949 KBytes
[ 10]   0.00-1.00   sec  2.94 GBytes  25.2 Gbits/sec  509   1.13 MBytes
[ 12]   0.00-1.00   sec  2.19 GBytes  18.8 Gbits/sec  522    872 KBytes
[SUM]   0.00-1.00   sec  10.5 GBytes  90.2 Gbits/sec  2238
```


Now the performace is reasonable and aligned with the hardware tested.
