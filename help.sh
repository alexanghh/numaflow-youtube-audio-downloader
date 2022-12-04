# build docker image and load into kind (for deployment in pipeline)
docker build -t test-python-udf:v5 . && kind load docker-image docker.io/library/test-python-udf:v5 --name numaflow-system
# setup / update pipeline
kubectl apply -f pipeline-numaflow.yaml
# port forward http input source
kubectl port-forward web-crawler-input-0-mlxmq 8444:8443
# send data to http input source endpoint
curl -kq -X POST -d "https://www.facebook.com/" https://localhost:8444/vertices/input

# port forward numaflow ui
kubectl -n numaflow-system port-forward deployment/numaflow-server 8443:8443


