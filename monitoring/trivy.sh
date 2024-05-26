#!/bin/bash

helm install trivy-operator aqua/trivy-operator --namespace monitoring --create-namespace --version 0.20.1 --values trivy-values.yaml

