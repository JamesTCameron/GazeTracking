FROM ubuntu:22.04
RUN apt-get update
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y cmake
RUN apt install -y libsm6
RUN apt install -y libxext6
RUN apt install -y libxrender1
RUN apt install -y libfontconfig1
RUN apt install -y libgl1-mesa-glx
RUN apt install -y libglib2.0-0
RUN pip3 install --upgrade pip
COPY .  /home/GazeTracking
WORKDIR /home/GazeTracking
RUN pip3 install -r requirements.txt
