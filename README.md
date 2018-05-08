# Einfach Ambulant WebPortal Prototype

## Installation

1) install Docker and Docker-Compose
2) download/clone this repository
3) run `docker-compose up` 
4) go to http://localhost:5000 and enjoy

## Releasing new Version

1) Improve the Code
2) Build the Docker-Image with `docker build -t einfachambulant/webportal .`
3) Push the Image to Docker-Hub with `docker push einfachambulant/webportal:latest`

## Deploying

See [Installation](#Installation) but `docker pull einfachambulant/webportal:latest` on the server first. 
