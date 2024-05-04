kubectl delete -f kubernetes/tool.yaml
docker build -t tool .
docker tag tool tool:v1
docker save tool:v1 | sudo k3s ctr images import -
kubectl apply -f kubernetes/tool.yaml
