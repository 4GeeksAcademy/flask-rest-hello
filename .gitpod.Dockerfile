FROM gitpod/workspace-mysql:branch-mysql

# install python3-dev to make sure the pip package "mysqlclient" works fine.
USER root
RUN apt-get update && apt-get install -y pkg-config python3-dev