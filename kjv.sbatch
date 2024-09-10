#!/usr/bin/bash

#SBATCH -N 1
#SBATCH --tasks-per-node=4
#SBATCH --job-name=kjv
#SBATCH --output=kjv_output.txt

## First make sure all other modules are not loaded
module purge

## Load the appropriate module
module load openmpi/4.0.3-gcc-8.5.0


# Fix your environment
export OMPI_MCA_pml="^ucx"
export OMPI_MCA_btl_openib_if_include="mlx4_0:1"

python3 markov-chain.py