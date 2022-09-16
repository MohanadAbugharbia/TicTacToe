FROM python:3.10

ARG SERVER_PORT=5555

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 123 ubuntu



RUN apt-get update && \
    apt-get install net-tools

COPY ./* /home/ubuntu/
RUN mkdir /home/ubuntu/base_game && \
    mv /home/ubuntu/base_game.py /home/ubuntu/base_game

EXPOSE ${SERVER_PORT}/tcp


WORKDIR /home/ubuntu
USER ubuntu

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD netstat -tulpn |grep -i python |grep -i 0.0.0.0 |grep -i listen || exit 1

ENTRYPOINT ["python", "/home/ubuntu/server.py"]
# ENTRYPOINT [ "/bin/bash" ]