FROM ubuntu:18.04 as base
EXPOSE 5050 80
USER root
ADD --chown=root:root cfg/sources.list /etc/apt/sources.list

RUN apt-get update \
    && apt-get install -y nginx vim python3.8 python3-pip curl sudo git lib32z1 python-dev libldap2-dev libsasl2-dev libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --upgrade pip \
    && useradd --create-home --no-log-init --shell /bin/bash htek \
    && adduser htek sudo \
    && echo 'htek:htek' | chpasswd
COPY . /home/lic_maker
ADD --chown=root:root /requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn
ADD --chown=root:root cfg/nginx.conf /etc/nginx/nginx.conf
ADD --chown=root:root cfg/sudoers /etc/sudoers

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/lic_maker
ENV PATH=/home/lic_maker:$PATH
ENV PYTHONPATH=/home/lic_maker:$PYTHONPATH

CMD ["/bin/bash", "/home/lic_maker/init.sh"]
