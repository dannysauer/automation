FROM opensuse/leap:15.0
RUN zypper in -y python python-pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /results