FROM mysql

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ca-certificates \
    python-pip \
    gcc \
    python-dev \
    libev4 \
    libev-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install PyMySQL
