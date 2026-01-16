# hafsa_depl


## Please read
## Info
Running the following command: docker compose up -d will build and run all the containers

Running python OR python3 build-script.py builds and pushes the images to Dockerhub (they are already up in Dockerhub repo)

Dockerfiles have been modified so docker compose builds the normal image aka "dev" stage while the build-script builds with the additional commands in Dockerfile aka "prod" stage


## To DEPLOY project in minikube
Minikube should be installed including the following addons:

- minikube addons enable registry

- minikube addons enable ingress

- minikube adddons enable dashboard

Open hafsa_depl directory within visual studio code and open three terminals
- Run the following commands in one terminal in that directory:
    - cd manifests
    - kubectl apply -k .
    - minikube start

- In the second terminal run:
    minikube dashboard

- In the third terminal run:
    minikube tunnel

To see the deployment working in browser, write the following in the url:
    localhost/register

## Authors and acknowledgment
Hafsa Moin

## License
Hafsa Moin Limited®

