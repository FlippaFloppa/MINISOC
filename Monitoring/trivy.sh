#!/bin/bash

helm install trivy-operator aqua/trivy-operator --namespace trivy-system --create-namespace --version 0.20.1 --values trivy-values.yaml
