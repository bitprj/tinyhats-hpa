# HPA (Horizontal Pod Autoscaling) Version 1

## The Premise
In many microservice applications, there's often one service that experiences the most latency and occaisionally struggles to keep up with an amount of requests. It is an option to manually increase the number of pods running on that service, but to conserve resources, we can autoscale.

Horizontal Pod Autoscaling will increase pods when metrics hit a entire threshold level. In our case, it will be when `manipulation-service` hits a threshold for CPU usage.

## Prerequisites
HPA Version 1 utilizes Kubernetes `metrics-server` to determine when to scale up or down. Let's enable it on minikube:
```
minikube addons enable metrics-server  
```

> **Tip:** If this produces an error, run `rm -rf ~/.minikube` and then `minikube start`. Try enabling the add on again.

Next, allocate usage for the cluster's resources. This way, Kubernetes will be able to calculate when the CPU usage reaches the specified threshold. (Example: Using 50% of the CPU resources)

Add the below snippet to the `manipulation.yaml` in your `kube` folder.
```
resources:
limits:
    cpu: 500m
requests:
    cpu: 200m
```

Below is an example of where it should go:
```
...
      containers:
        - name: manipulation-service
          image: bitprj/mini-manipulation-service
          ports:
          - containerPort: 80
          imagePullPolicy: Always
          resources:
            limits:
              cpu: 500m
            requests:
              cpu: 200m
---
...
```

## Deploying HPA
Go ahead and start your minikube cluster if it isn't up and running yet.
```
minikube start
```

We're now going to start autoscaling!
```
kubectl autoscale deployment manipulation-service --cpu-percent=10 --min=1 --max=10
```

## HPA in Action
Our locust service will generate requests to the point where it will hit the usage threshold for CPU. You can use `kubectl get hpa --watch` to see when the target is met and the `REPLICAS` increase from 1.

```
➜  locust-service git:(master) ✗ kubectl get hpa --watch
NAME                   REFERENCE                         TARGETS    MINPODS   MAXPODS   REPLICAS   AGE
manipulation-service   Deployment/manipulation-service   250%/10%   1         10        4          5m59s
```