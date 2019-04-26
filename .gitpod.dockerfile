FROM gitpod/workspace-full

RUN sudo apt-get update -q \
    && sudo apt-get install -y --no-install-recommends \
        libpq-dev \
        python3-dev