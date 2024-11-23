docker buildx build --platform linux/amd64 -t europe-west4-docker.pkg.dev/gp2-release-terra/genotools/genotools-api . --load

docker push europe-west4-docker.pkg.dev/gp2-release-terra/genotools/genotools-api

# gcloud run deploy genotools-api \
#   --image europe-west4-docker.pkg.dev/gp2-release-terra/genotools/genotools-api \
#   --platform managed \
#   --region europe-west4 \
#   --service-account genotools-server@gp2-release-terra.iam.gserviceaccount.com

gcloud run deploy genotools-api \
  --image europe-west4-docker.pkg.dev/gp2-release-terra/genotools/genotools-api \
  --platform managed \
  --region europe-west4 \
  --service-account genotools-server@gp2-release-terra.iam.gserviceaccount.com \
  --set-env-vars API_KEY="your_api_key_value",API_KEY_NAME="X-API-KEY" \
  --allow-unauthenticated