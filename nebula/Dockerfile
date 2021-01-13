FROM nebulabroadcast/nebula-base

ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID nebula
USER nebula

WORKDIR /opt/nebula
