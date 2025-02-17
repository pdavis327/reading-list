FROM python:3.11.10-slim
LABEL maintainer=""

ARG COMMIT="unknown"
ARG REPO="unknown"
ARG BRANCH="unknown"

LABEL commit_sha=${COMMIT}
LABEL commit_branch=${BRANCH}
LABEL commit_repo=${REPO}

ENV COMMIT_SHA=${COMMIT}
ENV COMMIT_BRANCH=${BRANCH}
ENV COMMIT_REPO=${REPO}

WORKDIR /opt/code

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT [ "python", "-u", "main.py" ]
