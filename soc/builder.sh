kubectl delete -f kubernetes/rs.yaml
docker build -t soc .
docker tag soc soc:v1
minikube image rm docker.io/library/soc:v1
minikube image load soc:v1
kubectl apply -f kubernetes/rs.yaml
