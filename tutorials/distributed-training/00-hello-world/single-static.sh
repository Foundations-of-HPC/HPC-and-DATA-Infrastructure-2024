#!/bin/bash
#SBATCH --partition=GPU
#SBATCH --job-name=gpu-train
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
##SBATCH --cpus-per-task=24
#SBATCH --mem=100gb
#SBATCH --gpus-per-task=2

#####################################
#       ENV SETUP                   #
#####################################
source ../gpu_env/bin/activate
export OMP_NUM_THREADS=1
#####################################

#####################################
#       RESOURCES                   #
#####################################
echo "Node allocated ${SLURM_NODELIST}"
echo "Using ${SLURM_NNODES} nodes"
echo "Using ${SLURM_NTASKS} tasks in total"
echo "Using ${SLURM_TASKS_PER_NODE} task per node"
echo ""

echo "Using ${SLURM_GPUS_ON_NODE} gpus per node"
#echo "Total gpu used ${SLURM_GPUS}"
###################################

export LOGLEVEL=INFO

torchrun --nproc-per-node=12 --nnodes=1 --rdzv-backend=static --master-addr=localhost --master-port=12345  main.py

