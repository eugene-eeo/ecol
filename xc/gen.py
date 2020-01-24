# MODIFY
n = 12
mod = 96 * 4
run = 0
cores = 24
refilter = False
random = False
cg = True
prog = "xc/xc 1500"

script = """#!/bin/bash
#SBATCH --job-name="xs-{n}"
#SBATCH -o xs-{n}.%A.out
#SBATCH -e xs-{n}.%A.err
#SBATCH -p par7.q
#SBATCH -t 01:00:00
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24

source /etc/profile.d/modules.sh
module load intel/xe_2017.2

{tasks}
wait"""

for i in range(mod // cores):
    if cg:
        task_template = "cat cores.g6 | xc/cg -d5 -N50 -n1000 | {prog} > /ddn/data/hvcs85/xc-hzc-{res}.out &"
    elif random:
        task_template = "nauty/genrang -g -P2 {n} 10000000 | {prog} > /ddn/data/hvcs85/xc-{n}-{res}.out &"
    elif refilter:
        task_template = "cat /ddn/data/hvcs85/xc-{n}-{res}.out | {prog} > /ddn/data/hvcs85/xc-{n}-{res}-filtered.out &"
    else:
        task_template = "nauty/geng -c {n} {res}/{mod} | {prog} > /ddn/data/hvcs85/xc-{n}-{res}.out &"

    tasks = "\n".join(task_template.format(n=n, res=((i * cores) + res), mod=mod, prog=prog) for res in range(cores))

    job_name = 'job-{n}-{i}-{p}'.format(n=n, i=i, p=(
        "random" if random else "refilter" if refilter else "cg" if cg else "geng"
    ))
    open(job_name, 'w').write(script.format(tasks=tasks, n=n))
    print('sbatch {name}'.format(name=job_name))
