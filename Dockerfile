FROM ubuntu:20.04

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y cmake python3-pip ca-certificates wget software-properties-common apt-transport-https
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN apt-add-repository "deb http://apt.llvm.org/focal/ llvm-toolchain-focal-16 main"
RUN apt-get update
RUN apt-get install -y plantuml clang-16

RUN cp /usr/lib/llvm-16/lib/libclang-16.so.1 /usr/lib/libclang-16.so

RUN pip3 install clang
RUN pip3 install md2pdf
RUN pip3 install pytest
RUN pip3 install pytest-mock
RUN echo 'alias python="python3"' >> ~/.bashrc

# useful commands:
# docker build --tag diaggen_image:1.0 .
# docker run -it --volume /home/mpiotrowski/Projects/diaggen/:/diaggen diaggen_image:1.0 /bin/bash
# python3 -m diaggen --project-dir=/diaggen/example/engine_controller --doc=doc/detailed_design.md.in