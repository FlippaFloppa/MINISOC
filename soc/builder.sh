kubectl delete -f kubernetes/soc.yaml
docker build -t soc .
docker tag soc soc:v1
docker save soc:v1 | sudo k3s ctr images import -
kubectl apply -f kubernetes/soc.yaml
