# Docker
## Useful Commands
- `docker exec -it <container-name> <term>`
- `docker stop/rm/start <id>`
- `docker ps -a`
- `docker pull <image>`
- `docker run --name <name> -d <image>`
- `docker images`
- `docker rmi <image-id>`

## Docker Networks
- `docker network ls`
- `docker network create <net-name>`

## Docker Compose
- `docker-compose -f <file.yaml> up -d`
- `docker-compose -f <file.yaml> down`

## Docker Repo
- `docker login`
- FQDN for an image is of the form - `registryDomain/imageName:tag`
- `docker tag <old-name>:<old-tag> <new-name>:<new-tag>`

## Docker Volumes
- `docker volume ls`
- `docker volume rm <volume>`

## Dockerfile
- RUN vs CMD
    - CMD is for entrypoint
    - There can be only one CMD command but multiple RUN commands
- `docker build -t <name>:<tag> <Dockerfile>`

## Tutorial
```bash
docker run -d \
    -p27017:27017 \
    -e MONGO_INITDB_ROOT_USERNAME=admin \
    -e MONGO_INITDB_ROOT_PASSWORD=secret \
    --name mongodb \
    --net mongo_network \
    mongo

docker run -d \
    -p8081:8081 \
    -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin \
    -e ME_CONFIG_MONGODB_ADMINPASSWORD=secret \
    --net mongo_network \
    --name mongo_express \
    -e ME_CONFIG_MONGODB_SERVER=mongodb \
    mongo-express
```
