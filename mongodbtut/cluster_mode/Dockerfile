FROM mvertes/alpine-mongo

RUN apk update && apk add --no-cache python && \
    python -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
    rm -r /root/.cache && \
    pip install pymongo==2.8.1 && \
    pip install mongoengine==0.14.3 && \
    apk add nano && \
    apk add htop
