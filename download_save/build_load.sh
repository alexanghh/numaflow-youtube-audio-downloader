version=$1
docker build -t download-youtube-to-s3-udf:$version . && kind load docker-image docker.io/library/download-youtube-to-s3-udf:$version --name numaflow-system
