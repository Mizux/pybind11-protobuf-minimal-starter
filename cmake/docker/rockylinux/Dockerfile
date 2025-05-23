# Create a virtual environment with all tools installed
# ref: https://hub.docker.com/_/rockylinux
FROM rockylinux:9 AS env

# Install system build dependencies
ENV PATH=/usr/local/bin:$PATH
RUN dnf -y update \
&& dnf -y install git wget openssl-devel cmake \
&& dnf -y groupinstall "Development Tools" \
&& dnf clean all \
&& rm -rf /var/cache/dnf
CMD [ "/usr/bin/bash" ]

# Install Python
RUN dnf -y update \
&& dnf -y install python3-devel python3-pip \
&& dnf clean all \
&& rm -rf /var/cache/dnf
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
