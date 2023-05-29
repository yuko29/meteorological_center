docker network create --subnet=172.18.0.0/16 st-final
docker run --publish 27017:27017\
           --ip 172.20.63.46 \
--name my-mongodb \
           -d mongo



docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-mongodb
netstat -an 172.17.0.2 | grep 27017