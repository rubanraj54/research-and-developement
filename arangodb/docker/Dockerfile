FROM arangodb/arangodb:3.1.13

COPY wait-for-it.sh /opt/
RUN chmod +x /opt/wait-for-it.sh

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ca-certificates \
    python-pip \
    gcc \
    python-dev \
    libev4 \
    libev-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install python-arango
