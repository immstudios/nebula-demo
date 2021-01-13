#!/bin/bash

docker-compose down -v
docker-compose rm
rm ./data/hls/*.ts
rm ./data/hls/*.m3u8
rm ./data/log/*.txt
