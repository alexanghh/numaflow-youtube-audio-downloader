version=$1
docker build -t wait-test-udf:$version . && kind load docker-image docker.io/library/wait-test-udf:$version --name numaflow-system
