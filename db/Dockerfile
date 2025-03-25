FROM mysql:8.0-debian AS builder

RUN mkdir -p /etc/mysql/conf.d

FROM mysql:8.0-debian

COPY --from=builder /etc/mysql/conf.d/ /etc/mysql/conf.d/

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD mysqladmin ping -h localhost || exit 1
