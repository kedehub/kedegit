1. Build the Docker Image

Navigate to the directory containing kedegit project and run the following command:

docker build --no-cache -t kedegit-image:latest -f kedegit/dockerize/Dockerfile .

docker image inspect kedegit-image --format '{{.Architecture}}'

2. Run the Docker Container

docker run --rm --add-host=host.docker.internal:host-gateway --name kedegit-container -v ~/git/kedegit/docs:/root/.config/KedeGit kedegit-image:latest list-projects

