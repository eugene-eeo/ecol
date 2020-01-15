

n = 11
mod = 24


script = """#!/bin/bash
#SBATCH --job-name="xs-{n}"
#SBATCH -o myscript.%A.out
#SBATCH -e myscript.%A.err
#SBATCH -p par7.q
#SBATCH -t 01:30:00
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24

source /etc/profile.d/modules.sh
module load intel/xe_2017.2

{tasks}
wait"""

task_template = "nauty/geng -c {n} {res}/{mod} | xc/xc > xc-{n}-{res}.out &"

tasks = "\n".join(task_template.format(n=n, res=res, mod=mod) for res in range(mod))

print(script.format(tasks=tasks, n=n))
