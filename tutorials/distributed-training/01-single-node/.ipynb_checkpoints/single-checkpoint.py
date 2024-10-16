import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
import torch.distributed as dist
import os
import sys
from torch.utils.data import DataLoader,DistributedSampler
import time
from torch.nn.parallel import DistributedDataParallel as DDP
class AlexNetCIFAR(nn.Module):
    def __init__(self, num_classes=10):
        super(AlexNetCIFAR, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 192, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(192, 384, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(),
            nn.Linear(256 * 4 * 4, 4096),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(inplace=True),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), 256 * 4 * 4)  # Flatten the feature map
        x = self.classifier(x)
        return x




def train(model, train_loader, criterion, optimizer, epoch):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (inputs, targets) in enumerate(train_loader):
        inputs, targets = inputs.to(device_id), targets.to(device_id)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

        if batch_idx % 100 == 0:
            print(f'Epoch {epoch}, Batch {batch_idx}, Loss: {running_loss / (batch_idx + 1):.3f}, '
                  f'Accuracy: {100. * correct / total:.3f}%')

def test(model, test_loader, criterion):
    model.eval()
    test_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, targets in test_loader:
            inputs, targets = inputs.to(device_id), targets.to(device_id)

            outputs = model(inputs)
            loss = criterion(outputs, targets)

            test_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

    print(f'Test Loss: {test_loss / len(test_loader):.3f}, Test Accuracy: {100. * correct / total:.3f}%')
if __name__=="__main__":
    assert dist.is_available()
    os.environ['NCCL_SOCKET_IFNAME'] = 'enp225s0f1np1'
    os.environ['NCCL_DEBUG'] = 'info'
    os.environ['NCCL_IB_HCA']='mlx5'
    #https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html    
    dist.init_process_group("nccl")
    rank=dist.get_rank()
    print(f"Hello from rank {rank}\n")
    device_id = rank % torch.cuda.device_count()
    model = AlexNetCIFAR().to(device_id)
    ddp_model = DDP(model, device_ids=[device_id])

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
    train_loader = DataLoader(train_dataset, shuffle=False,
                              sampler=train_sampler,batch_size=256,num_workers=1, drop_last=True)
    test_loader = DataLoader(test_dataset, shuffle=False,
                             sampler=test_sampler, drop_last=True)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    num_epochs = 50
    for epoch in range(num_epochs):
        start_time = time.time()
        train(ddp_model, train_loader, criterion, optimizer, epoch)
        test(ddp_model, test_loader, criterion)
        end_time = time.time()
        print(f"Time per epochs {end_time-start_time}")
        