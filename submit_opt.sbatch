#!/bin/bash
#SBATCH --nodes=1
#SBATCH --partition=compute
#SBATCH --ntasks-per-node=8
#SBATCH --time=120:00:00
#SBATCH --mem=32GB
#SBATCH --job-name=ae_opt
#SBATCH --array=1-99

module add apps/gaussian/16

cd $SLURM_SUBMIT_DIR
OPTNAME=$(sed -n "${SLURM_ARRAY_TASK_ID}p" OPT_IN_ARRAY.txt)
g16 ${OPTNAME}
