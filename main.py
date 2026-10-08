We need answer code only. Need write small complete runnable Python project: docker-compose service health checker. Single file, under 60 lines, short module docstring, standard library only, include __main__ block. Need likely parse docker-compose.yml? Standard library only, no yaml. Could perhaps check docker-compose services via `docker compose ps --format json` and health. But "docker-compose service health checker" maybe read docker-compose.yml? Standard lib only means no PyYAML. Could use subprocess to call `docker compose ps --format json`, parse JSON, check health/status. Single file under 60 lines. Need runnable. Include __main__. Short module docstring.

Need decide implementation. Use `docker compose ps --format json` output. Docker compose v2 supports `--format json` returns JSON array (or newline JSON?). Actually `docker compose ps --format json` outputs JSON array in recent versions? Let's recall: `docker compose ps --format json` outputs a JSON array of objects. Each object has fields: ID, Name, Command, Project, Service, State, Health, ExitCode, Publishers. In older maybe newline-delimited JSON. We can handle both. Standard library json, subprocess, sys, time, argparse? Under 60 lines. Need health checker: list unhealthy services, maybe wait until healthy with timeout. Could implement CLI: `python compose_health.py [compose-file?] [--timeout]`. But simplest: run `docker compose ps --format json`, parse, print healthy/unhealthy. Could include poll loop.

Requirements: "docker-compose service health checker". Single file, under 60 lines, short module docstring, standard library only, include a __main__ block. Reply code only.

Could write:

"""Check Docker Compose service health using `docker compose ps`."""
import json, subprocess, sys, time

def services():
    out = subprocess.check_output(["docker","compose","ps","--format","json"], text=True)
    out = out.strip()
    if not out: return []
    try:
        data = json.loads(out)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return [json.loads(line) for line in out.splitlines() if line.strip()]

def check(timeout=60, interval=2):
    deadline = time.time() + timeout
    while True:
        svcs = services()
        if not svcs:
            print("No services found.")
            return 0
        bad = []
        for s in svcs:
            name = s.get("Service") or s.get("Name") or "?"
            state = (s.get("State") or "").lower()
            health = (s.get("Health") or "").lower()
            if state != "running" or health in ("unhealthy", "starting"):
                bad.append(f"{name}: state={state or '?'} health={health or '-'}")
        if not bad:
            print("All services healthy.")
            return 0
        if time.time() >= deadline:
            print("Unhealthy services:")
            for b in bad: print(" -", b)
            return 1
        print("Waiting...")
        time.sleep(interval)

if __name__ == "__main__":
    sys.exit(check(int(sys.argv[1]) if len(sys.argv) > 1 else 60))

Need under 60 lines. Count. This is ~40. Good. But is it correct? `docker compose ps --format json` may output JSON array. If service has no healthcheck, Health may be empty. We treat state running and health empty as okay. If health "starting", treat bad until healthy. If no healthcheck, okay. If state exited, bad.

Could also support docker-compose (v1) command? Requirement "docker-compose service health checker" maybe command `docker-compose`. But Docker Compose v2 uses `docker compose`. Could detect? Simpler use `docker compose`. But maybe project name suggests docker-compose. We can use `docker-compose`? Standard. Maybe we can allow env var? Under 60 lines. Could try `docker compose` and fallback to `docker-compose`. But that adds lines. We can implement `COMPOSE = ["docker", "compose"]` maybe. Maybe use `shutil.which` to detect. But standard lib. Hmm.

Need "small, complete, runnable Python project". Single file. Under 60 lines. Short module docstring. Standard library only. Include __main__ block. Code only.

Potential issue: `docker compose ps --format json` in some versions outputs JSON array with newlines. Our parse handles both. But if out is JSON array, json.loads succeeds. If newline-delimited, json.loads fails and we parse lines. Good.

Potential issue: `subprocess.check_output` raises CalledProcessError if docker not found or compose fails. We might want to handle. But small. Could catch and print error. Add try/except in services. Under 60 lines.

Maybe implement with argparse? Not needed.

Could include docstring and comments? Short.

Let's count lines exactly if I write:

1 """Check Docker Compose service health using `docker compose ps`."""
2
3 import json
4 import subprocess
5 import sys
6 import time
7
8
9 def get_services():
10     out = subprocess.check_output(
11         ["docker", "compose", "ps", "--format", "json"], text=True
12     ).strip()
13     if not out:
14         return []
15     try:
16         data = json.loads(out)
17         return data if isinstance(data, list) else [data]
18     except json.JSONDecodeError:
19         return [json.loads(line) for line in out.splitlines() if line.strip()]
20
21
22 def check(timeout=60, interval=2):
23     deadline = time.time() + timeout
24     while True:
25         services = get_services()
26         if not services:
27             print("No services found.")
28             return 0
29         bad = []
30         for svc in services:
31             name = svc.get("Service") or svc.get("Name") or "?"
32             state = (svc.get("State") or "").lower()
33             health = (svc.get("Health") or "").lower()
34             if state != "running" or health in ("unhealthy", "starting"):
35                 bad.append(f"{name}: state={state or '?'} health={health or '-'}")
36         if not bad:
37             print("All services healthy.")
38             return 0
39         if time.time() >= deadline:
40             print("Unhealthy services:")
41             for item in bad:
42                 print(" -", item)
43             return 1
44         print("Waiting for services...")
45         time.sleep(interval)
46
47
48 if __name__ == "__main__":
49