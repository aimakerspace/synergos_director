# FROM python:3.7.4-slim-buster

# ##################
# # Configurations #
# ##################

# ARG PYSYFT_CHECKPOINT=PySyft-v0.2.4_aisg
# ARG SYFT_PROTO_CHECKPOINT=syft-proto-v0.2.5.a1_aisg

# ##########################################################
# # Step 1: Install Linux dependencies for source-building #
# ##########################################################

# RUN apt-get update
# RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
#         build-essential \
#         libz-dev \
#         libbz2-dev \
#         libc6-dev \
#         libdb-dev \
#         libgdbm-dev \
#         libffi-dev \
#         liblzma-dev \
#         libncursesw5-dev \
#         libreadline-gplv2-dev \
#         libsqlite3-dev \
#         libssl-dev \
#         tk-dev \
#         git \
#         unzip

# #########################################
# # Step 2: Clone, build & setup REST-RPC #
# #########################################

# ADD . /director
# WORKDIR /director

# RUN pip install --upgrade pip setuptools wheel \
#  && pip install --no-cache-dir -r requirements.txt

# RUN unzip -q '/director/etc/*.zip' -d /director/etc/tmp \
#  && pip install /director/etc/tmp/${PYSYFT_CHECKPOINT} \
#  && pip install /director/etc/tmp/${SYFT_PROTO_CHECKPOINT}

# #######################################################
# # Step 3: Expose relevant connection points & run app #
# #######################################################

# EXPOSE 5000
# EXPOSE 8020

# ENTRYPOINT ["python", "./main.py"]

# CMD ["--help"]

##############
# Base Image #
##############

FROM python:3.7.4-slim-buster as base

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    git\
    pciutils

RUN pip install --upgrade pip \
 && pip install --upgrade setuptools wheel

ADD ./synergos_algorithm /director/synergos_algorithm
RUN pip install /director/synergos_algorithm

ADD ./synergos_archive /director/synergos_archive
RUN pip install /director/synergos_archive

ADD ./synergos_logger /director/synergos_logger
RUN pip install /director/synergos_logger

ADD ./synergos_manager /director/synergos_manager
RUN pip install /director/synergos_manager

ADD ./synergos_rest /director/synergos_rest
RUN pip install /director/synergos_rest

WORKDIR /director
ADD . /director

EXPOSE 5000
EXPOSE 8080

########################
# New Image - Debugger #
########################

FROM base as debug
RUN pip install ptvsd

WORKDIR /director
EXPOSE 5678
CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait main.py

##########################
# New Image - Production #
##########################

FROM base as prod

WORKDIR /director
ENTRYPOINT ["python", "./main.py"]
CMD ["--help"]
