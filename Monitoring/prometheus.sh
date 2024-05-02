#!/bin/bash

helm upgrade --install prometheus prometheus-community/kube-prometheus-stack -n monitoring --values monitoring.yaml
