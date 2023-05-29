# Iterate over all the arguments
network_name="non"
ip="172.20.63.4"

while [[ $# -gt 0 ]]; do
  case $1 in
    -network)
      if [[ $# -gt 1 ]]; then
        network_name=$2
        shift
      else
        echo "Usage: bash ./prepare_db.sh -ip (assign ip address) -network (assign network name)"
      fi
      ;;
    -ip)
      if [[ $# -gt 1 ]]; then
        ip=$2
        shift
      else
        echo "Usage: bash ./prepare_db.sh -ip (assign ip address) -network (assign network name)"
      fi
      ;;
    *)
      echo "Usage: bash ./prepare_db.sh -ip (assign ip address) -network (assign network name)"
      exit 0
      ;;
  esac
  shift
done

if [ $network_name == "non" ]; then
    docker run --publish 27017:27017 --ip=$ip --name my-mongodb -d mongo
else
    docker run --publish 27017:27017 --network=$network_name --ip=$ip --name my-mongodb -d mongo
fi

echo ""
echo "result: "
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-mongodb
netstat -an $ip | grep 27017