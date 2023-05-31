FROM nvidia/cuda:11.6.0-devel-ubuntu20.04

MAINTAINER weikai

ENV PATH="/opt/conda/bin:${PATH}"
ARG PATH="/opt/conda/bin:${PATH}"

SHELL ["/bin/bash", "-c"]

COPY . /home
WORKDIR /home

RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install apt-utils -y
RUN apt-get update -y
RUN DEBIAN_FRONTEND=noninteractive apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install wget -y
RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-py310_22.11.1-1-Linux-x86_64.sh
RUN bash Miniconda3-py310_22.11.1-1-Linux-x86_64.sh -u -b -p /opt/conda
RUN rm -f Miniconda3-py310_22.11.1-1-Linux-x86_64.sh
RUN echo "export PATH=/opt/conda/bin:$PATH" >> ~/.bashrc
RUN source ~/.bashrc
RUN conda init bash
RUN apt-get install git -y
RUN conda env create -f environment.yaml
RUN git clone https://github.com/alexandrosstergiou/SoftPool.git && cd SoftPool && git checkout 2d2ec6d
SHELL ["conda", "run", "-n", "mos3d", "/bin/bash", "-c"]
RUN cd /home/SoftPool/pytorch && make install
RUN apt install libsparsehash-dev
RUN pip install --upgrade git+https://github.com/mit-han-lab/torchsparse.git@v1.4.0
RUN pip install protobuf==3.20.*

RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /home/*
RUN conda clean -a
RUN pip cache remove *
RUN mkdir -p /home/wzhoea/Desktop/

CMD cd /home/wzhoea/Desktop

# docker build -t mos3d:1 .
# docker run --gpus all -it --name mos3d -v /home/wzhoea/Desktop/:/home/wzhoea/Desktop/ -v /media/wzhoea/T7:/media/wzhoea/T7 --shm-size 8G mos3d:1 /bin/bash

# conda activate mos3d && cd /home/wzhoea/Desktop/mos3d

# To inference the predictions.
# python infer.py -d ./toydata -m ./log/motionseg3d_pointrefine -l ./pred/oursv1 -s valid
# python infer.py -d ./toydata -m ./log/motionseg3d_pointrefine -l ./pred/oursv2 -s valid --pointrefine

# Visualize the predictions.
# python utils/visualize_mos.py -d ./toydata -p ./pred/oursv2 --offset 0 -s 38
