#!/bin/bash
#boot services.
source ${SDP_HOME}/global.func
[ -z $portmap ] && ERROR
[ -z $user_id ] && ERROR
[ -z $SERVER_IP ] && ERROR
[ -z $init_passwd ] && ERROR
[ -z $init_service_type ] && ERROR

container_memcached=registry.saintic.com/memcache
container_mongodb=registry.saintic.com/mongodb
container_mysql=registry.saintic.com/mysql
container_redis=registry.saintic.com/redis

case $init_service_type in
memcached)
  container_id=`docker run -tdi --restart=always --name $init_user -p ${SERVER_IP}:${portmap}:11211 $container_memcached | cut -c 1-12`
  docker exec -i $container_id /usr/local/bin/memcached -d -u root
  ;;
mongodb)
  container_id=`docker run -tdi --restart=always --name $init_user -p ${SERVER_IP}:${portmap}:27017 $container_mongodb | cut -c 1-12`
  docker exec -i $container_id /data/app/mongodb/bin/mongod -f /data/app/mongodb/mongod.conf &
  ;;
mysql)
  container_id=`docker run -tdi --restart=always --name $init_user -p ${SERVER_IP}:${portmap}:3306 $container_mysql | cut -c 1-12`
  docker exec -i $container_id /etc/init.d/mysqld start
  docker exec -i $container_id mysql -e "grant all on *.* to 'root'@'%' identified by \"${init_passwd}\" with grant option;"
  docker exec -i $container_id mysql -e "grant all on *.* to 'root'@'localhost' identified by \"${init_passwd}\";"
  docker exec -i $container_id /etc/init.d/mysqld restart
  ;;
redis)
  container_id=`docker run -tdi --restart=always --name $init_user -p ${SERVER_IP}:${portmap}:6379 $container_redis | cut -c 1-12`
  #docker exec -i sed -i 's/appendonly no/appendonly yes/' /etc/redis.conf
  docker exec -i $container_id /etc/init.d/redis start
  ;;
*)
  echo -e "\033[31mUnsupported service type！\033[0m"
  DoubleError
  ;;
esac

container_ip=$(docker inspect --format '{{ .NetworkSettings.IPAddress }}' $init_user)
container_pid=$(docker inspect --format '{{.State.Pid}}' $init_user)

source ${SDP_HOME}/.end.sh
