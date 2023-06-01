FROM mongo:latest AS DB

COPY db-dump /db-dump
COPY mongo.sh /home/mongo.sh
COPY config/mongod.yml /resource/mongod.yml
RUN chmod 777 /home/mongo.sh

CMD /home/mongo.sh