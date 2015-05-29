# sentinel-graylog

A simple script which pipes Redis Sentinel messages into Graylog

## Usage

```bash
$ docker build -t sentinel-graylog .
$ docker run -e SENTINEL_HOST=10.0.0.1 -e GRAYLOG_HOST=10.0.0.10 sentinel-graylog
```

## Available Environment Variables

* `SENTINEL_HOST`: Sentinel hostname/IP (default: `localhost`)
* `SENTINEL_PORT`: Sentinel port (default: `6379`)
* `GRAYLOG_HOST`: Graylog hostname/IP (default: `localhost`)
* `LOGGING_HOSTNAME`: Graylog 'localname'  (default: none)
* `VERBOSE`: Print messages to stdout (default: `false`)
