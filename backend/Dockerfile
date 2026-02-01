FROM ubuntu:22.04

# Install system dependencies (matching original working Dockerfile)
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

# Upgrade pip
RUN pip3 install --upgrade pip

# Copy everything to working directory
COPY . /home/GazeTracking
WORKDIR /home/GazeTracking

# Install base requirements (dlib, numpy, opencv)
RUN pip3 install -r requirements.txt

# Install Flask backend requirements
RUN pip3 install -r backend/requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the Flask application
CMD ["python3", "backend/app.py"]
