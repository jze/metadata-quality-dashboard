# Deployment

## Reset and Create the `/shared/` volume
```
docker volume rm audit-shared
docker volume create audit-shared
```
A shared volume enables data sharing between containers. For more details, see [Inter-process Communication](../documentation/inter-process-communication.md)

## Build and Run the `data-updater` Container
* Dockerfile.run-now — Run once
* Dockerfile.prod — Run periodically according the `contrab.txt` file
```
docker image build -f Dockerfile.prod -t audit.data-updater.prod .

docker container run \
    --rm \
    --detach \
    --mount source=audit-shared,destination=/shared/ \
    --name audit.data-updater.prod \
        audit.data-updater.prod
```

## Build and Run the `rest-api` Container
```
docker image build -t audit.rest-api .

docker container run \
    --rm \
    --detach \ 
    --publish 8080:8080 \ 
    --mount source=audit-shared,destination=/shared/ \
    --name audit.rest-api.container \ 
    audit.rest-api
```
