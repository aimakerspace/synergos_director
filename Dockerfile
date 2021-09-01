##############
# Base Image #
##############

FROM python:3.7.4-slim-buster as base

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    git\
    pciutils

RUN pip install --upgrade setuptools wheel

ADD ./synergos_algorithm /orchestrator/synergos_algorithm
RUN pip install /orchestrator/synergos_algorithm

ADD ./synergos_archive /orchestrator/synergos_archive
RUN pip install /orchestrator/synergos_archive

ADD ./synergos_logger /orchestrator/synergos_logger
RUN pip install /orchestrator/synergos_logger

ADD ./synergos_manager /orchestrator/synergos_manager
RUN pip install /orchestrator/synergos_manager

ADD ./synergos_rest /orchestrator/synergos_rest
RUN pip install /orchestrator/synergos_rest

WORKDIR /orchestrator
ADD . /orchestrator

EXPOSE 5000
EXPOSE 8080

########################
# New Image - Debugger #
########################

FROM base as debug
RUN pip install ptvsd

WORKDIR /orchestrator
EXPOSE 5678
CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait main.py

##########################
# New Image - Production #
##########################

FROM base as prod

WORKDIR /orchestrator
ENTRYPOINT ["python", "./main.py"]
CMD ["--help"]
