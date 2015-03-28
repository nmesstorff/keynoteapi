# Create RPM packages for keynoteapi and dependencies.
# For deployment targets without pip.

FROM centos:6.6
MAINTAINER marthjod@gmail.com

RUN yum upgrade -y
RUN yum install -y tar rpm-build git

# https://pypi.python.org/packages/source/s/setuptools/setuptools-14.3.1.tar.gz
COPY resources/setuptools-14.3.1.tar.gz /data/
# https://pypi.python.org/packages/source/a/argparse/argparse-1.3.0.tar.gz
COPY resources/argparse-1.3.0.tar.gz /data/
# https://pypi.python.org/packages/source/n/nagiosplugin/nagiosplugin-1.2.2.tar.gz
COPY resources/nagiosplugin-1.2.2.tar.gz /data/

WORKDIR /data

RUN tar xfz argparse-1.3.0.tar.gz
RUN tar xfz nagiosplugin-1.2.2.tar.gz
RUN tar xfz setuptools-14.3.1.tar.gz
RUN git clone https://github.com/marthjod/keynoteapi.git

RUN cd setuptools-14.3.1 && python setup.py install
RUN cd argparse-1.3.0 && python setup.py bdist --format=rpm
RUN cd nagiosplugin-1.2.2 && python setup.py bdist --format=rpm
RUN cd keynoteapi && python setup.py bdist --format=rpm

RUN mkdir /dists
RUN find -name '*.noarch.rpm' -exec cp {} /dists \;

RUN rpm -i /dists/argparse*.noarch.rpm
RUN rpm -i /dists/nagiosplugin*.noarch.rpm
RUN rpm -i /dists/keynoteapi*.noarch.rpm

RUN check_keynote

VOLUME /data