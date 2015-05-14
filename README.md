# sentinel-graylog

A simple script which pipes Redis Sentinel messages into Graylog

## Usage

```bash
$ docker build -t sentinel-graylog .
$ docker run -e SENTINEL_ADDRESS=127.0.0.1 -e SENTINEL_PORT=26379 -e GRAYLOG_ADDRESS=10.0.0.1 sentinel-graylog
```
