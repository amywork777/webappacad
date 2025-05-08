FROM freecad/freecad:latest

RUN apt-get update && apt-get install -y git netgen gmsh calculix-cxx \
    libeigen3-dev libblas-dev liblapack-dev python3-pip && \
    pip3 install --no-cache-dir freecad-mcp pillow opencv-python-headless numpy

RUN git clone https://github.com/neka-nat/freecad-mcp /opt/mcp
ENV PYTHONPATH=/opt/mcp:${PYTHONPATH}