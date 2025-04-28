# Create a virtual environment with all tools installed
# ref: https://hub.docker.com/_/fedora
FROM fedora:latest AS env

# Install system build dependencies
ENV PATH=/usr/local/bin:$PATH
RUN dnf -y update \
&& dnf -y install \
 git wget \
 @development-tools \
 gcc-c++ cmake \
&& dnf clean all

# Install Python
RUN dnf -y update \
&& dnf -y install \
 python3 python3-devel python3-pip python3-wheel \
 python3-virtualenv \
 python3-numpy python3-pandas \
&& dnf clean all
RUN python3 -m pip install \
 absl-py mypy mypy-protobuf

# Add the library src to our build env
FROM env AS devel
WORKDIR /home/project
COPY . .

FROM devel AS build
RUN cmake --version
RUN cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release
RUN cmake --build build --target all -v
RUN cmake --build build --target install -v

FROM build AS test
RUN CTEST_OUTPUT_ON_FAILURE=1 cmake --build build --target test -v
