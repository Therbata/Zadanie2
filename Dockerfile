FROM python:3.12-alpine

LABEL org.opencontainers.image.authors="Jakub Kramek"

WORKDIR /app

RUN apk add --no-cache curl

COPY app.py /app
COPY hc.sh /hc
RUN chmod +x /hc

RUN pip install --no-cache-dir flask requests

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["/hc"]

CMD ["python", "app.py"]
