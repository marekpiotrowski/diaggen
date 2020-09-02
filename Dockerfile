FROM node

RUN apt-get update
RUN apt-get install -y cmake python3-pip ca-certificates wget software-properties-common apt-transport-https
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN apt-add-repository "deb http://apt.llvm.org/stretch/ llvm-toolchain-stretch-11 main"
RUN apt-get update
RUN apt-get install -y clang-11

RUN cp /usr/lib/llvm-11/lib/libclang-11.so.1 /usr/lib/libclang-11.so

RUN pip3 install clang
RUN echo 'alias python="python3"' >> ~/.bashrc