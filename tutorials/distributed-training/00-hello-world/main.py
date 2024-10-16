import os
import sys
import tempfile
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
from torch.nn.parallel import DistributedDataParallel as DDP

if __name__=="__main__":
    assert dist.is_available()
    os.environ['NCCL_SOCKET_IFNAME'] = 'ibp216s0'
    os.environ['NCCL_DEBUG'] = 'info'
    os.environ['NCCL_IB_HCA']='mlx5'
    #https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html
    dist.init_process_group("nccl")
    rank=dist.get_rank()
    print(f"Hello from rank {rank}\n")
    dist.destroy_process_group()
