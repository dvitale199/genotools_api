CLUSTER="gtcluster-eu-west4"
NAMESPACE="gke-ns-gtcluster-eu-west4"
ZONE="europe-west4-a"
PROJECT_ID="gp2-release-terra"

gcloud config set project $PROJECT_ID

gcloud container clusters get-credentials $CLUSTER --zone $ZONE --project $PROJECT_ID

gcloud container clusters delete $CLUSTER --zone $ZONE

kubectl delete namespace $NAMESPACE
