# MODIFY
n = 12
mod = 96
run = 0
cores = 24

script = """#!/bin/bash
#SBATCH --job-name="xs-{n}"
#SBATCH -o xs-{n}.%A.out
#SBATCH -e xs-{n}.%A.err
#SBATCH -p par7.q
#SBATCH -t 03:00:00
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24

source /etc/profile.d/modules.sh
module load intel/xe_2017.2

{tasks}
wait"""


for i in range(mod // cores):
    task_template = "nauty/geng -c {n} {res}/{mod} | xc/xc > /data/hvcs85/xc-{n}-{res}.out &"

    tasks = "\n".join(task_template.format(n=n, res=((i * cores) + res), mod=mod) for res in range(cores))

    open(f'job-{n}-{i}', 'w').write(script.format(tasks=tasks, n=n))
