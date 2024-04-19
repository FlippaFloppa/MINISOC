kubectl delete -f kubernetes/rs.yaml
docker build -t tool .
docker tag tool tool:v1
minikube image rm docker.io/library/tool:v1
minikube image load tool:v1
kubectl apply -f kubernetes/rs.yaml
