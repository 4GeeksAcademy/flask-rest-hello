FROM mcr.microsoft.com/devcontainers/python:3.13

ENV PYTHONUNBUFFERED 1

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# Installs system dependencies required for PostgreSQL and Graphviz, and cleans up to reduce image size
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
&& apt-get -y install --no-install-recommends \
   postgresql-client \
   graphviz \
   graphviz-dev \
&& rm -rf /var/lib/apt/lists/*  


#  Install `pipenv` globally
RUN pip install pipenv

#  Use the same path as `workspaceFolder` in `devcontainer.json`
WORKDIR /workspaces/${localWorkspaceFolderBasename}

#  Copy Pipfile and Pipfile.lock first to leverage Docker cache
COPY Pipfile Pipfile.lock ./

#  Install Python dependencies with `pipenv`
RUN pipenv install --dev --deploy --skip-lock

#  Copy the rest of the code after installing dependencies
COPY . ./
