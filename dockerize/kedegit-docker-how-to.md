1. Build the Docker Image

Navigate to the directory containing kedegit project and run the following command:

docker build --no-cache -t kedegit-image:latest -f kedegit/dockerize/Dockerfile .

docker image inspect kedegit-image --format '{{.Architecture}}'

2. Run the Docker Container

docker run --rm --name kedegit-container -v /Users/dimitarbakardzhiev/git/kedegit/docs:/root/.config/KedeGit kedegit-image:latest list-projects

