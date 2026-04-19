# Environment Awareness

Detect environment constraints before choosing strategies.

## What to Probe

### Hardware

- CPU: cores, architecture
- RAM: total, available
- GPU: presence, model, VRAM
- Disk: space, type (SSD/HDD)

### Software

- Toolchains available (compilers, interpreters)
- Package managers
- Test runners
- Build systems
- Linters and formatters

### Network

- Internet connectivity
- Proxy configuration
- External API access

### Container

- Running in Docker/container
- Resource limits

## Why It Matters

Before committing to a hypothesis, filter against environment constraints:

| Strategy | Environment Need |
|----------|-----------------|
| GPU optimization | GPU available |
| Package installation | Network + package manager |
| Compiler optimization | Specific toolchain |
| Containerization | Docker available |

## How to Use

1. Run environment probe at run start
2. Store the environment profile
3. Filter hypotheses against constraints
4. Log the environment summary in results log header

## Example Commands

```bash
# CPU
nproc
uname -m

# RAM
free -m

# GPU
nvidia-smi || echo "no NVIDIA GPU"

# Disk
df -m .

# Container
cat /proc/1/cgroup | grep -E "docker|crio" || echo "not in container"
```
