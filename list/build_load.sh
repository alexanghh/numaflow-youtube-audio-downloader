version=$1
docker build -t list-youtube-playlist-udf:$version . && kind load docker-image docker.io/library/list-youtube-playlist-udf:$version --name numaflow-system
