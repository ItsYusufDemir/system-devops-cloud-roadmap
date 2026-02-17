# Notes

- Basically, we have 4-repos as a standart arhitecture in a company.

1. Infrastructure Repo: IaC, it builds servers, configure networks, empty kubernetes cluster. Used techs: Terraform, Ansible. Done by: Infrastructure, Network, Cloud Engineers, DevOps.

2. The Platform Repo: It installs mandatory services inside the empty kubernetes cluster. Cluster-wide ingress, services meshes, monitoring stacks, cert managers, ArgoCD core config etc. Used techs: ArgoCD, Helm. Done by: DevOps, Platform Engineers, SRE.

3. App source Repo: Developers write the code in this repo. DevOps implement CI and containerize the app here.

4. App Delivery Repo: Holds the kubernetes YAML files. Used techs: ArgoCD, Kustomize, Helm. Done by DevOps.

- DevOps Engineer can do all of these according to the seperation of roles in the company.
- GitOps: is the repo 2 and 4. Agent in the cluster watches these repos and pull these to match the cluster with these configs. This is called GitOps.

- In my eShop project there will be 4 repos as well.

1. homelab-infra: IaC for my proxmox setup. Secondary
2. k8s-platform: Represents platform laters. Secondary
3. eshop: already forked this. Impelement CI here. Primary
4. eshop-delivery: Move all k8s files to here. Primary

- Currently I have k8s folder inside eshop repo. But this violates GitOps principles. Therefore I will move k8s folder to another repo.
- This arhitecture shows a seperation of concerns in the software development process.



