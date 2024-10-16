import os
import sys
import tempfile
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
from torch.nn.parallel import DistributedDataParallel as DDP

from model import AlexNetCIFAR

if __name__=="__main__":
    assert dist.is_available()
    os.environ['NCCL_SOCKET_IFNAME'] = 'ibp216s0'
    os.environ['NCCL_DEBUG'] = 'info'
    os.environ['NCCL_IB_HCA']='mlx5'
    #https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html    
    dist.init_process_group("nccl")
    rank=dist.get_rank()
    
    print(f"Hello from rank {rank}\n")
    device_id = rank % torch.cuda.device_count()

    model = AlexNetCIFAR().to(device_id)
    ddp_model = DDP(model, device_ids=[device_id])


    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(ddp_model.parameters(), lr=0.001)
    optimizer.zero_grad()
    
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])

    train_dataset = datasets.CIFAR10(root='../data', train=True, download=True, transform=transform_train)
    test_dataset = datasets.CIFAR10(root='../data', train=False, download=True, transform=transform_test)
    
    train_sampler = DistributedSampler(train_dataset) 
    test_sampler = DistributedSampler(test_dataset) 

    train_loader = DataLoader(train_sampler, shuffle=False,
                    sampler=train_sampler)
    test_sampler = DataLoader(test_sampler, shuffle=False,
                sampler=test_sampler)
    
#    for epoch in range(start_epoch, n_epochs):
#        if is_distributed:
#            sampler.set_epoch(epoch)
#        train(loader)

    print("DONE")
    dist.destroy_process_group()
