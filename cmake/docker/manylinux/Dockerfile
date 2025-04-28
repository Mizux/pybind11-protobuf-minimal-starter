# ref: https://github.com/pypa/manylinux
FROM quay.io/pypa/manylinux_2_28_x86_64:latest AS env
# note: Almalinux:8 based image with
# CMake 3.31.2 and SWIG 4.3.0 already installed

# Install system build dependencies
RUN dnf -y update \
&& dnf -y install \
 curl wget \
 git patch \
 which pkgconfig autoconf libtool \
 make gcc-c++ \
 redhat-lsb openssl-devel pcre2-devel \
 zlib-devel unzip zip \
&& dnf clean all \
&& rm -rf /var/cache/dnf
ENTRYPOINT ["/usr/bin/bash", "-c"]
CMD ["/usr/bin/bash"]

# Add the library src to our build env
FROM env AS devel
WORKDIR /home/project
COPY . .
COPY ./cmake/docker/manylinux/build-manylinux.sh .

FROM devel AS build
RUN ./build-manylinux.sh build

FROM build AS test
RUN ./build-manylinux.sh test
