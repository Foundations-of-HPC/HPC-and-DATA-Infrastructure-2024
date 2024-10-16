#!/bin/bash
#SBATCH --partition=DGX
#SBATCH --job-name=gpu-train
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=100gb

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

####################################
#      MASTER ELECTION             #
####################################
export master_node=$(scontrol getaddrs $SLURM_NODELIST | head -n1 | awk -F ':' '{print$2}' | sed 's/^[ \t]*//;s/[ \t]*$//')
echo "Master node used ${master_node}"
####################################
export MASTER_ADDR=${master_node}
export MASTER_PORT=12345

#srun torchrun \
#  --nnodes=2 \
#  --nproc_per_node=2 \
#  --rdzv_id=$SLURM_JOB_ID \
#  --rdzv_backend=c10d \
# --rdzv_endpoint=$MASTER_ADDR  main.py

export LOGLEVEL=INFO

srun torchrun \
--nnodes 2 \
--nproc_per_node 2 \
--rdzv_id $RANDOM \
--rdzv_backend c10d \
--rdzv_endpoint $master_node:12345 main.py

#srun torchrun --nnodes=2 --nproc-per-node=2 --rdzv-id=100 --rdzv-backend=c10d --rdzv-endpoint=localhost:0 main.py

