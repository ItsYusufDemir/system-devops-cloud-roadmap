# Notes

- Kubernetes (k8n, 8 means letter number between first and last letter) is an orchestration tool for container nodes.
- One master node (control plane) and many worker nodes.
- Pod: deployable object. One pod can have 1 to many containers.
- Worker nodes has kubelet, a demanon to communicate with master. Master node has API server to communicate with kubelets.
- Worker nodes has container runtime (not docker deamon, containerd). Starts, stops containers. There is also kube-proxy, it routes traffic to correct pods. Also load balance between pods.

- Self healing (HA), automatic rollbacks, hoziontal scaling (many nodes).
- Portable, can transport to cloud.
- complex to setup and operate. 
- Overkill for small organizations. Mid to high level is ok.
- Managed kubernetes services by cloud: Amazon EKS, Google Kubernetes Engine (GKE), Azure kubernetes service (AKS)

- Control plane (master node) components: API server, etcd, scheduler, controller manager
- Worker node components: Kubelet, kube-proxy, container runtime