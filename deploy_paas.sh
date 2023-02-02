#!/bin/bash 

# Provide path for charts

PAAS_PATH=$1

#Untar charts

for i in $PAAS_PATH/*.tgz; do tar -xvf $i --directory $PAAS_PATH; done

# Changing repo in charts

HARBOR_URL=$2

sed -i "s/artifactory.mavenir.com/$HARBOR_URL/g" $PAAS_PATH/kube-prometheus-stack/values.yaml
sed -i "s/artifactory.mavenir.com/$HARBOR_URL/g" $PAAS_PATH/kube-prometheus-stack/charts/dellhw-exporter/values.yaml
sed -i "s/artifactory.mavenir.com/$HARBOR_URL/g" $PAAS_PATH/kube-prometheus-stack/charts/etcd-forwarder/values.yaml
sed -i "s/artifactory.mavenir.com/$HARBOR_URL/g" $PAAS_PATH/kube-prometheus-stack/charts/missing-container-metrics/values.yaml
sed -i "s/artifactory.mavenir.com/$HARBOR_URL/g" $PAAS_PATH/istio-operator/values.yaml
sed -i "s/artifactory.mavenir.com/$HARBOR_URL/g" $PAAS_PATH/istio-stack/values.yaml
sed -i "s/artifactory.mavenir.com/$HARBOR_URL/g" $PAAS_PATH/traefik/values.yaml

sed -i "s/ngn-mwppaas-docker-dev/mwppaas/g" $PAAS_PATH/kube-prometheus-stack/values.yaml
sed -i "s/ngn-mwppaas-docker-dev/mwppaas/g" $PAAS_PATH/kube-prometheus-stack/charts/dellhw-exporter/values.yaml
sed -i "s/ngn-mwppaas-docker-dev/mwppaas/g" $PAAS_PATH/kube-prometheus-stack/charts/etcd-forwarder/values.yaml
sed -i "s/ngn-mwppaas-docker-dev/mwppaas/g" $PAAS_PATH/kube-prometheus-stack/charts/missing-container-metrics/values.yaml
sed -i "s/ngn-mwppaas-docker-dev/mwppaas/g" $PAAS_PATH/istio-operator/values.yaml
sed -i "s/ngn-mwppaas-docker-dev/mwppaas/g" $PAAS_PATH/istio-stack/values.yaml
sed -i "s/ngn-mwppaas-docker-dev/mwppaas/g" $PAAS_PATH/traefik/values.yaml



#Deploying Prometheus

echo "Deploying Prometheus"

NAME=$(hostname)
clustername=${NAME%-master*}

/usr/local/bin/helm upgrade --install kube-prometheus-stack $PAAS_PATH/kube-prometheus-stack/ -n mwppaas --set-string kube-prometheus-stack.alertmanager.alertmanagerSpec.nodeSelector.paas="true" --set-string kube-prometheus-stack.prometheusOperator.admissionWebhooks.patch.nodeSelector.paas="true" --set-string kube-prometheus-stack.prometheusOperator.nodeSelector.paas="true" --set-string kube-prometheus-stack.prometheus.prometheusSpec.nodeSelector.paas="true" --set-string kube-prometheus-stack.grafana.nodeSelector.paas="true" --set-string kube-prometheus-stack.kube-state-metrics.nodeSelector.paas="true" --set=kube-prometheus-stack.defaultRules.additionalRuleLabels.clustername="$clustername" --set=missing-container-metrics.rules.additionalRuleLabels.clustername="$clustername" --set=dellhw-exporter.prometheusRules.additionalRuleLabels.clustername="$clustername" --set=portworx.rules.additionalRuleLabels.clustername="$clustername"

#Deploying Istio

echo "Deploying Istio"

/usr/local/bin/helm upgrade --install istio-operator $PAAS_PATH/istio-operator/ -n mwppaas-operators --set-string=nodeSelector.paas="true"

/usr/local/bin/helm upgrade --install istio-stack $PAAS_PATH/istio-stack/ -n mwppaas --set=istio.namespace='mwppaas' --set-string=istio.components.ingressGateway.k8s.nodeSelector.paas="true" --set-string=istio.components.egressGateway.k8s.nodeSelector.paas="true" --set-string=istio.components.pilot.k8s.nodeSelector.paas="true" --set-string=kiali-server.deployment.node_selector.paas="true" --set-string=tracing.nodeSelector.paas="true"

#Deploying Traefik

echo "Deploying Traefik"

/usr/local/bin/helm upgrade --install traefik $PAAS_PATH/traefik/ -n mwppaas --set-string=nodeSelector.paas="true"
