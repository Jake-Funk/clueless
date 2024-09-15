# Clueless Backend Code	
This directory contains all server code and backend logic for the game. 
The main server is built using [FastAPI](https://fastapi.tiangolo.com/) and the python environment is managed by [uv](https://docs.astral.sh/uv/) follow these links to their respective documentation.

### Building the Image  
To build a docker/podman image run:
```bash
docker build -t clueless-server .
```

then to run it:
```bash
docker run -p 8000:80 clueless-server
```

