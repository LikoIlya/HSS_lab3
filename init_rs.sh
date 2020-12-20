#! /bin/bash
docker-compose exec configsvr01 sh -c "mongo < /scripts/init-configserver.js"

docker-compose exec shard01-a sh -c "mongo < /scripts/init-shard1.js"
docker-compose exec shard02-a sh -c "mongo < /scripts/init-shard2.js"
docker-compose exec shard03-a sh -c "mongo < /scripts/init-shard3.js"
