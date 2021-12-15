
---

## Setup

* Create a swarm of docker nodes
    - Initialize master node: ` docker swarm init`
    - Add workers: `docker swarm join --token <master-token> <master-ip>:2377`

* Build and run the docker image
    ```
    ./setup.sh -a deploy
    ```

* stop and delete all docker image and volumes
    ```
    ./setup.sh -a clean
    ```

---

## Connecting to grafana
  Access the browser on `localhost:80`
  
  Username: `admin`   
  Password: `admin`

---
