FROM orientdb:2.2.29

RUN apk update && apk add --no-cache python && \
    python -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip install pyorient && \
    apk add nano && \
    apk add htop
