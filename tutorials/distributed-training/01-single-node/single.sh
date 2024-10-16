#!/bin/bash
#SBATCH --partition=DGX
#SBATCH --job-name=gpu-train
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=100gb
#SBATCH --gres=gpu:4

#####################################
#       ENV SETUP                   #
#####################################
source /u/area/ntosato/scratch/distributed/dgx_env/bin/activate
export OMP_NUM_THREADS=1
#####################################

#####################################
#       RESOURCES                   #
#####################################
echo "Node allocated ${SLURM_NODELIST}"
echo "Using ${SLURM_NNODES} nodes"
echo "Using ${SLURM_NTASKS} tasks in total"
echo "Using ${SLURM_TASKS_PER_NODE} task per node"
echo "Using ${SLURM_GPUS_ON_NODE} gpus per node"
#echo "Total gpu used ${SLURM_GPUS}"
###################################

export LOGLEVEL=INFO
srun torchrun --nnodes=1 --nproc-per-node=4 --rdzv-id=100 --rdzv-backend=c10d --rdzv-endpoint=localhost:0 main.py

