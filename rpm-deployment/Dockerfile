# Create RPM packages for keynoteapi and dependencies.
# For deployment targets without pip.

FROM centos:6.6
MAINTAINER marthjod@gmail.com

RUN yum upgrade -y
RUN yum install -y tar rpm-build git


WORKDIR /data

RUN curl -s https://pypi.python.org/packages/source/s/setuptools/setuptools-14.3.1.tar.gz > /data/setuptools-14.3.1.tar.gz
# COPY resources/setuptools-14.3.1.tar.gz /data/
RUN curl -s https://pypi.python.org/packages/source/a/argparse/argparse-1.3.0.tar.gz > /data/argparse-1.3.0.tar.gz
# COPY resources/argparse-1.3.0.tar.gz /data/
RUN curl -s https://pypi.python.org/packages/source/n/nagiosplugin/nagiosplugin-1.2.2.tar.gz > /data/nagiosplugin-1.2.2.tar.gz
# COPY resources/nagiosplugin-1.2.2.tar.gz /data/
RUN curl -s https://pypi.python.org/packages/source/r/requesocks/requesocks-0.10.8.tar.gz > /data/requesocks-0.10.8.tar.gz
# COPY resources/requesocks-0.10.8.tar.gz /data/
RUN curl -s https://pypi.python.org/packages/source/c/certifi/certifi-14.05.14.tar.gz > /data/certifi-14.05.14.tar.gz


RUN tar xfz argparse-1.3.0.tar.gz
RUN tar xfz nagiosplugin-1.2.2.tar.gz
RUN tar xfz setuptools-14.3.1.tar.gz
RUN tar xfz requesocks-0.10.8.tar.gz
RUN tar xfz certifi-14.05.14.tar.gz
RUN git clone https://github.com/marthjod/keynoteapi.git

RUN cd setuptools-14.3.1 && python setup.py install
RUN cd argparse-1.3.0 && python setup.py bdist --format=rpm
RUN cd nagiosplugin-1.2.2 && python setup.py bdist --format=rpm
RUN cd requesocks-0.10.8 && python setup.py bdist --format=rpm
RUN cd certifi-14.05.14 && python setup.py bdist --format=rpm
RUN cd keynoteapi && python setup.py bdist --format=rpm

RUN mkdir /dists
RUN find -name '*.noarch.rpm' -exec cp {} /dists \;

RUN rpm -i /dists/argparse*.noarch.rpm
RUN rpm -i /dists/nagiosplugin*.noarch.rpm
RUN rpm -i /dists/requesocks*.noarch.rpm
RUN rpm -i /dists/certifi*.noarch.rpm
RUN rpm -i /dists/keynoteapi*.noarch.rpm

# RUN check_keynote

VOLUME /data
