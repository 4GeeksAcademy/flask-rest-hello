FROM node:16

RUN apt update \
    && apt install software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update \
    && apt install python3.10

WORKDIR /opt/app
COPY --from=build /opt/app/venv /venv

ENV PATH="/opt/app/venv/bin:$PATH"
ENV NODE_ENV=container