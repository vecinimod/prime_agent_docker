# Prime Agent: Local Multi-GPU AI Deployment

This repository contains a robust, Dockerized deployment environment for [prime-agent](https://github.com/PrimeIntellect-ai/prime-agent). It leverages a dual-GPU vLLM backend, a Node.js-based orchestrator with an embedded Python 3.11 IPython kernel, and secure remote access via Tailscale.

## 🏗️ System Architecture

The environment is orchestrated via `docker-compose` and consists of four primary services:

1. **vLLM-B70 (Primary):** Hosts the primary orchestrator model (`Intel/Qwen3.6-27B-int4-AutoRound`) on an Intel Arc B70 GPU (GPU 0).
2. **vLLM-B60 (Secondary):** Hosts the secondary model instance on an Intel Arc Pro B60 GPU (GPU 1) for parallel tasks and sub-agent spawning.
3. **Prime Agent:** The core framework container. It maps a local `workspace` volume, dynamically links custom native skills into a persistent Python kernel managed by `uv`, and handles Gmail MCP server integrations.
4. **Tailscale:** A privileged container acting as an exit node, providing secure remote SSH and network access to the host machine.

## 📋 Prerequisites

* **Hardware:** Intel Arc GPUs with appropriate drivers mapped to `/dev/dri`.
* **Docker:** Docker Engine and Docker Compose installed.
* **Network:** A Tailscale account and Auth Key for remote access.
* **Credentials:** A Google Cloud Platform OAuth client secret JSON (if utilizing the Gmail MCP).

## 🚀 Setup & Installation

**1. Clone the repository**

```bash
git clone <your-repo-url>
cd prime-agent

```

**2. Configure Environment Variables**
Copy the template environment file and populate it with your keys.

```bash
cp .env.example .env

```

*Required variables in `.env`:*

* `TAILSCALE_AUTHKEY`
* `SERPER_API_KEY` (For web search capabilities)
* `CEREBRAS_API_KEY` (Fallback LLM provider)

**3. Configure OAuth (Optional)**
If using the Gmail MCP integration, place your GCP credentials in the `~/.prime/` directory on your host machine:

```bash
mkdir -p ~/.prime
# Place your JSON file here and rename it:
# ~/.prime/gcp-oauth.keys.json

```

**4. Launch the Environment**
Start the containers in detached mode.

```bash
docker compose up -d

```

*Note: On the first boot, the Prime Agent container will automatically clone the latest upstream workspace, build the isolated Python 3.11 virtual environment using `uv`, and link all local packages.*

## 🛠️ Custom Skills

This deployment supports dynamically loaded local skills, allowing the agent to extend its capabilities.

Custom skills (such as the included `pdf-deck` package) are located in their respective subdirectories. The hardened startup script ensures true idempotency by:

1. Scrubbing stale `.pth` editable links to prevent "ghost packages" upon restart.
2. Guaranteeing the core `prime-agent-runtime` installs first to resolve cross-dependencies.
3. Dynamically installing any local directories containing a `pyproject.toml` or `setup.py` directly into the persistent `prime-kernel` volume.

## 🛡️ Idempotency & State Management

This configuration has been explicitly hardened to survive host reboots, branch checkouts, and repository updates without destroying local state:

* **Persistent Kernel:** The Python environment lives in a named Docker volume (`prime-kernel`), preventing heavy rebuilds on every startup.
* **Smart Config Syncing:** Host configurations (like `mcp.json` and OAuth keys) are non-destructively synced into the container using `cp -u` and symbolic links.
* **Locked Dependencies:** Node modules are strictly managed using `npm ci` where applicable to prevent floating version drift.