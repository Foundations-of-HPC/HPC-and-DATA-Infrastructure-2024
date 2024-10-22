# List of tutorials 

## STREAM Tutorials

This is a collection of tutorials and exercise on benchmarking memory bandwidth on different nodes of ORFEO architecture. 

- [STREAM benchmark on Epyc nodes](STREAM/stream_on_epyc.md)
- [STREAM benchmark on Thin/Large node](STREAM_stream_on_intel.md)
- [STREAM benchmark on DGX nodes](STREAM/stream_on_dgx.md)

## Hardware

- [List of commands usefull to discover your hardware](hardware-discover/discover.md)

## Distributed training

A set of samples that show how to train a NN model with pytorch, exploiting `nccl` backend and multiple nodes.

- [Sample distributed pytorch job](distributed-training/00-hello-world)
- [Single node training](distributed-training/01-single-node)
- [Distributed training](02-multi-node)

## IO 

A set of tools to test the IO:

- [`dd`](IO/dd.md)
- [`IOR`](IO/IOR.md)

## Network

Sessions of measure on Infiniband and Ethernet network:

- [iperf3, Ethernet test](network/iperf3.md)
- [MPI benchmark to test RDMA](network/mpi-pingpong.md)

## Slurm

How slurm work, cgroup  resource management, array job, job dependencies.

- [Advanced slurm](slurm/slurm.md)

