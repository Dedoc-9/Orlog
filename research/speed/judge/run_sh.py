"""Run the judge's spherical-harmonic laws through the four executions, as measured for research/speed (the reference,
python, c99 and rust, by orl.py's own arbiter), writing the witnesses and the said output under work/speed-judge/.
  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/speed/judge/make_sh.py
  PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/speed/judge/run_sh.py
"""
import os
import subprocess
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
WORK = os.path.join(ROOT, "work", "speed-judge")
RUNS = os.path.join(WORK, "runs")


def run(name, witness):
    os.makedirs(RUNS, exist_ok=True)
    cmd = [sys.executable, "-B", os.path.join(ROOT, "orl.py"), "run", os.path.join(WORK, name + ".orl"),
           "--backends", "python,c99,rust", "--workdir", RUNS, "--witness", os.path.join(RUNS, witness), "--show"]
    r = subprocess.run(cmd, capture_output=True)
    with open(os.path.join(RUNS, "show-%s.txt" % name), "wb") as fh:
        fh.write(r.stdout.replace(b"\r\n", b"\n"))
    print(r.stdout.decode("utf-8", "replace").splitlines()[0] if r.stdout else r.stderr.decode()[-300:])
    return r.returncode


codes = [run("sh_say_r4", "witness-say-r4.json")]
codes += [run(n, "witness") for n in ("sh_sum_r4", "sh_sum_r8", "sh_sum_r16")]
sys.exit(max(codes))
