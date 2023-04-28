FROM --platform=linux/amd64 nvidia/cuda:12.0.1-cudnn8-runtime-ubuntu20.04
ENV GCSFUSE_METADATA_IMAGE_TYPE=DLC
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV GCSFUSE_METADATA_IMAGE_TYPE=DLC
ENV PATH=/opt/conda/bin:$PATH
ENV PATH=/opt/conda:$PATH
ENV DL_ANACONDA_HOME /opt/conda
RUN apt-get update && apt-get install wget -y
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh -O ~/anaconda.sh && /bin/bash ~/anaconda.sh -b -p /opt/conda &&     rm ~/anaconda.sh &&     ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh &&     echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc &&     echo "conda activate base" >> ~/.bashrc &&     find /opt/conda/ -follow -type f -name '*.a' -delete &&     find /opt/conda/ -follow -type f -name '*.js.map' -delete &&     /opt/conda/bin/conda clean -afy
RUN apt-get update && apt-get -y install sudo -y
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B53DC80D13EDEF05 && echo "deb http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /usr/share/keyrings/cloud.google.gpg && apt-get update -y && apt-get install google-cloud-sdk -y
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B53DC80D13EDEF05 && if dpkg -s libnccl2; then echo "deb https://packages.cloud.google.com/apt google-fast-socket main" | tee /etc/apt/sources.list.d/google-fast-socket.list && curl -s -L https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /usr/share/keyrings/cloud.google.gpg && apt-get update -y && apt install -y google-fast-socket; fi
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B53DC80D13EDEF05 && echo "deb http://packages.cloud.google.com/apt gcsfuse-focal main" | tee /etc/apt/sources.list.d/gcsfuse.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | tee /usr/share/keyrings/cloud.google.gpg && apt-get  update -y && apt-get install -y gcsfuse && rm -rf /var/lib/apt/lists/*
RUN apt update -y && apt install -y libnuma-dev
EXPOSE 8080
COPY ["/requirements/run_jupyter.sh", "/run_jupyter.sh"]
COPY ["/requirements//opt/jupyter/.jupyter/jupyter_notebook_config.py", "/opt/jupyter/.jupyter/jupyter_notebook_config.py"]
VOLUME ["/home/jupyter"]
ENTRYPOINT ["/bin/bash"]
CMD ["/run_jupyter.sh"]