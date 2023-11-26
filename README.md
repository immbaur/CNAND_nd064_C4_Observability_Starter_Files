## Cloud Native Architecture Nanodegree (CNAND): Observability

This is the public repository for the Observability course of Udacity's Cloud Native Architecture Nanodegree (CNAND) program (ND064).

The  **Exercise_Starter_Files** directory has all of the files you'll need for the exercises found throughout the course.

The **Project_Starter_Files** directory has the files you'll need for the project at the end of the course.


Steps:
    1  curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    2  kubectl create namespace monitoring
    3  kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_alertmanagers.yaml
    4  kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_prometheusrules.yaml
    5  kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_servicemonitors.yaml
    6  kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_thanosrulers.yaml
    7  kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_podmonitors.yaml
    8  kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_probes.yaml
    9  kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/prometheus-operator/release-0.42/example/prometheus-operator-crd/monitoring.coreos.com_prometheuses.yaml
   15  helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   18  helm repo add stable https://charts.helm.sh/stable
   19  helm repo update
   20  helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig /etc/rancher/k3s/k3s.yaml 
   23  kubectl delete crd alertmanagerconfigs.monitoring.coreos.com
   24  kubectl delete crd alertmanagers.monitoring.coreos.com
   25  kubectl delete crd podmonitors.monitoring.coreos.com
   26  kubectl delete crd probes.monitoring.coreos.com
   27  kubectl delete crd prometheuses.monitoring.coreos.com
   28  kubectl delete crd prometheusrules.monitoring.coreos.com
   29  kubectl delete crd servicemonitors.monitoring.coreos.com
   30  kubectl delete crd thanosrulers.monitoring.coreos.com
   31  helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig /etc/rancher/k3s/k3s.yaml 
   32  kubectl get pods -n monitoring
   33  kubectl patch svc "prometheus-grafana" -n monitoring -p '{"spec": {"type":"LoadBalancer"}}'
   35  kubectl --namespace monitoring port-forward svc/prometheus-grafana --address 0.0.0.0 3000:80