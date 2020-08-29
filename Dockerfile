FROM node

RUN apt-get update
RUN apt-get install -y cmake python3-pip ca-certificates wget software-properties-common
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN apt-get update
RUN apt-add-repository "deb http://apt.llvm.org/bionic/ llvm-toolchain-bionic-11 main"
RUN apt-get install -y clang-11


RUN pip3 install clang