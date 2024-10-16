#!/bin/bash
#SBATCH --partition=GPU
#SBATCH --job-name=gpu-train
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=100gb
#SBATCH --gpus-per-task=2

#####################################
#       ENV SETUP                   #
#####################################
source ../gpu_env/bin/activate         #
export OMP_NUM_THREADS=1            #
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


####################################
#      MASTER ELECTION             #
####################################
export master_node=$(scontrol getaddrs $SLURM_NODELIST | head -n1 | awk -F ':' '{print$2}' | sed 's/^[ \t]*//;s/[ \t]*$//') 
echo "Master node used ${master_node}"
####################################
export MASTER_ADDR=${master_node}
export MASTER_PORT=12345

export LOGLEVEL=INFO

srun torchrun \
--nnodes 2 \
--nproc_per_node 2 \
--rdzv_id $RANDOM \
--rdzv_backend c10d \
--rdzv_endpoint $master_node:12345 main.py

