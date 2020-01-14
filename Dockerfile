################## BASE IMAGE ######################

FROM clinicalgenomics/mip:latest

################## METADATA ######################

################## MAINTAINER ######################

COPY . /source/varg

RUN conda install pip python=3.7 cython=0.29.13 cyvcf2=0.11.5

## Clean up after conda
RUN /opt/conda/bin/conda clean -tipsy

RUN pip install -e /source/varg

WORKDIR /data/
