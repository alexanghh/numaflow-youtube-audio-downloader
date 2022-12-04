version=$1
docker build -t convert-webm-mp3-udf:$version . && kind load docker-image docker.io/library/convert-webm-mp3-udf:$version --name numaflow-system
