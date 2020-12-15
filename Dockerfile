# Base image
FROM python:3.7

################## METADATA ######################

LABEL base_image="python:3.7"
LABEL version="1.0"
LABEL software="varg"
LABEL about.summary="Varg is a application to benchmark vcf-files against a truth-set of positive controls"
LABEL about.home="https://github.com/Clinical-Genomics/varg"
LABEL about.license_file="https://github.com/Clinical-Genomics/varg/blob/master/LICENSE"
LABEL about.license="MIT License (MIT)"
LABEL about.tags="variant validation report generator "
LABEL maintainer="Henrik Stranneheim <henrik.stranneheim@scilifelab.se>"
LABEL maintainer="Anders Jemt <anders.jemt@scilifelab.se>"

RUN pip install -U pip

RUN pip install micropipenv[toml]

COPY ./pyproject.toml ./poetry.lock ./

RUN micropipenv requirements --method poetry > requirements.txt

RUN pip install -r requirements.txt

RUN pip install varg

CMD ["varg", "--help"]

