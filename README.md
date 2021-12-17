
---

## Setup

* Create a swarm of docker nodes
    - Initialize master node: ` docker swarm init`
    - For multi-host setup add workers: `docker swarm join --token <master-token> <master-ip>:2377`

* Build and run the docker image
    ```
    ./setup.sh -a deploy
    ```

* Stop and delete all docker image and volumes
    ```
    ./setup.sh -a clean
    ```

---

## Connect to grafana
  Access the browser on `localhost:80`
  
  Username: `admin`   
  Password: `admin`

---

## Run a simple test with an attacker

    python3 attacker.py

---