FROM ubuntu:16.04
MAINTAINER Carl Njoku "flavoursoft@yahoo.com"
RUN apt-get update -y
# pip has to be installed before setuptools, setuptools has to be installed before tensorflow
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y python3.6 python3.6-dev python3-pip

RUN ln -sfn /usr/bin/python3.6 /usr/bin/python3 && ln -sfn /usr/bin/python3 /usr/bin/python && ln -sfn /usr/bin/pip3 /usr/bin/pip
# also useful
RUN python3.6 -m pip install --no-cache-dir ipython requests numpy pandas quandl
RUN python3.6 -m pip install --no-cache-dir tensorflow-gpu==1.3.0rc0
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["image_upload.py"]

#19290


