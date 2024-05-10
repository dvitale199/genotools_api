# make reqs
pipreqs . --force --ignore .env,.vscode,app/routers/.pytest_cache,app/.pytest_cache,__pycache__,notebooks/*,old/*,.venv


# build image
docker build -t genotools_api .

# test image
docker run -p 8080:8080 c1e4d1b99444

# configure auths
gcloud auth configure-docker us-central1-docker.pkg.dev

# tag
 docker tag c1e4d1b99444 us-central1-docker.pkg.dev/genotools/genotools/genotools_api:v0.0.1

 # push
 docker push us-central1-docker.pkg.dev/genotools/genotools/genotools_api:v0.0.1

 # build
 gcloud builds submit --tag  us-central1-docker.pkg.dev/genotools/genotools/genotools_api:v0.0.1

 