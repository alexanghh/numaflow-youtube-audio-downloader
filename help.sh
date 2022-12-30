# build docker image and load into kind (for deployment in pipeline)
docker build -t test-python-udf:v5 . && kind load docker-image docker.io/library/test-python-udf:v5 --name numaflow-system
# setup / update pipeline
kubectl apply -f pipeline-numaflow.yaml
# port forward http input source
kubectl port-forward web-crawler-input-0-mlxmq 8444:8443
curl -kq -X POST -d '{"playlist_url":"https://www.youtube.com/playlist?list=PLxRjZqOuEn4c85_km96U9Z0rwJI10txUU"}' https://localhost:8444/vertices/input
# send data to http input source endpoint
curl -kq -X POST -d "https://www.facebook.com/" https://localhost:8444/vertices/input

kubectl logs youtube-playlist-dowload-download-youtube-save-0-szj16 numa

# delete flow
kubectl delete -f pipeline-numaflow.yaml

# port forward numaflow ui
kubectl -n numaflow-system port-forward deployment/numaflow-server 8443:8443

# setup numaflow-system
kubectl create namespace numaflow-system
kubectl apply -n numaflow-system -f https://raw.githubusercontent.com/numaproj/numaflow/v0.7.0-rc1/config/install.yaml
