FROM python:3.10
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install gcc -y && \
    pip install --upgrade pip && \
    apt-get install cron -y && \
    apt-get install supervisor -y && \
    apt-get install bind9-host -y && \
    apt install dnsutils -y && \
    apt-get install openssh-server -y

RUN mkdir -p /opt/back_dnsrbl
RUN mkdir -p /opt/flags
RUN touch /opt/database.bd
WORKDIR /opt/back_dnsrbl

COPY requirements.txt /opt/back_dnsrbl/requirements.txt
COPY src/ /opt/back_dnsrbl
RUN pip install --no-cache-dir -r requirements.txt

COPY conf/supervisord.conf /etc/supervisord.conf
COPY conf/cron /var/spool/cron/crontabs/root
COPY scripts/start.sh /start.sh

#SSH
RUN echo "root:Docker!" | chpasswd
RUN mkdir -p /var/run/sshd
COPY conf/sshd_config /etc/ssh

ENV TZ=America/Santiago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN chmod 755 /start.sh
RUN chmod 755 /opt/back_dnsrbl/cron/*

EXPOSE 8080 2222

CMD ["/start.sh"]