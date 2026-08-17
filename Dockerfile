FROM node:22-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    curl \
    git \
    util-linux \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Pre-build Python 3.11 virtual environment for the kernel
# (matches the path used in docker-compose)
RUN uv venv --python 3.11 /opt/prime-kernel && \
    uv pip install --python /opt/prime-kernel/bin/python \
        ipykernel \
        requests \
        httpx \
        pyyaml \
        tomli \
        python-dotenv \
        pandas \
        numpy \
        scipy \
        beautifulsoup4 \
        lxml \
        pydantic \
        fpdf2

ENV PRIME_AGENT_KERNEL_PYTHON=/opt/prime-kernel/bin/python

WORKDIR /app
