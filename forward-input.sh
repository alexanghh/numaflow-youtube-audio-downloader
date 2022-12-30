#!/bin/bash
pod=$(kubectl get pods | grep youtube | grep input | cut -d ' ' -f 1)
kubectl port-forward $pod 8444:8443

