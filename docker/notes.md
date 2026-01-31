# source

I already have some docker knowledge but I will first refresh my current knowledge and then go further with docker.
I will use docker run -dp 80:80 docker/getting-started getting started image to learn it.

# notes

- definition: containerization is isolating a process from other processes in a OS. It uses Linux's feature called kernel namespaces and cgroups. Multiple containers run in the same machine and they share the OS kernel. It is like virtualizing the OS. Similar to chroot.
- Namespaces control what can a process see: its PID, network, storage.
- Cgroups control how much hardware a process can use. We dont want our containers try to use more than we want not to crash the bare metal computer. Developed by Google software engineers in 2006.

- Why? It solves "it works on my machine" problem. A container run in any container regardless of hardware and environment of that OS.

- Container were invented before docker. LXC (Linux Containers) was released in 2008, the first containerization tool. Docker just made it easy to use and it become industrial standart.

- docker run -dp 80:80 docker/getting-started, here -d: run in bacground mode (detached), -p map ports. left one local machine right one docker container network.

- container image: a custom file system provided by a container image. It is custom as it have specific dependencies, env variables, configurations for that specific app we use. This is actually what Docker bring, made it super easy.

- I downloaded a sample node.js app. Then I created a Dockerfile:

FROM node:18-alpine
WORKDIR /app
COPY . .
RUN yarn install --production
CMD ["node", "src/index.js"]


- Here, FROM selects which image to to use as base. WORKDIR specifies dir in the container. COPY copies current folder to container current folder. RUN runs a terminal command to install needed packages. CMD part is the default command to start our app.

- we start the app by: docker run -dp 3000:3000 getting-started

- Suppose a code change needed in the app,what to do? We just stop and remove the current container, and then build again: docker build -t getting-started .  then start it: docker run -dp 3000:3000 getting-started
- In this example, we lost our database after removing the old one.

- How to upload our image to Docker Hub (official docker image registry)? First login to Docker Hub from terminal: docker login -u <user-name>
- If you want your repo to be private, Go to Docker Hub and create the repo as private. If it is public, skip this part since next step already auto create public repo.
- Then create a tag for that image on the remote side: docker tag <image-name-local> <username>/<remote-repo-name>    If the repo does not exist, docker create the repo as public (!!! Be careful!!! You might sent your API keys to public!)
- Lastly, push it to the hub: docker push <username>/<remote-repo-name>


- Our image is now accessible from another machine by: docker run -dp 3000:3000 <username>/<remote-repo-name>
- For the remote repo side, we can also specify versioning while creating the tag: docker tag <image-name-local> <username>/<remote-repo-name>:<version-number> If you dont provide it, docker automatically set it as "latest"

- To run a command inside a docker, use this: docker exec <container-id> <command>

- To make docker data persistent we must use volumes. Because container data gone after the container stopped. Volumes are basically data on the host machine and not removed even container stops. There two kinds of volume: named volume and bind mounts. There also additional volume drivers for Ceph, SFTP, S3 etc.

- Named volume is simply a bucket of data. Create a volum by: docker volume create <volume-name>        Then assign it when you start the container: docker run -dp 3000:3000 -v <volume-name>:<path-in-container-to-be-saved> <image-name>     Now, our data will be persistent.
- Where does my data actually being kept in my machine? use: docker volume inspect <volume-name>        It will show you the Mountpoint, probably starts with /var/lib/docker/volumes/xx

- In bind mount, we can also select where to store the data by: -v <path-in-machine>:<path-in-container>    Bind mount becomes so efficient for devoplment. We can bind the source code to the container and put a restarting server like nodemon. As devs change the code, it immediately serve the current code.


## Multi-container apps

- Generally, each container should do one thing and do it well. Therefore, for example we must seperate database from the backend. There are lots of advantages of that like, restarting a container does not effect others, multiple version containers etc.
- How will containers communicate each other while they are isolated from the host machine? By creating docker networks. docker network create <network-name>

- Now when we run our container we also specify: --network <network-name>       Also we can specify: --name <container-name>      This name is then can be used by other containers to communicate with this container! It is happening because docker has a internal dns A record that maps <container-name> to this container IP addresses. Pretty nice, you dont have to memorize the IP of that container.
- Now in our app container, we give parameter MYSQL_HOST=<container-name-of-mysql-container>.
- Carefull! <IP-of-mysql-container> would also work but every time container restarts its IP changes, therefore you must use names!

- We also have --network-alias but this is slightly different then name. Because name must be unique for each container, however this alias can be used by many containers. Why? To make something like a load balancer. When a container ping to an alias (ex: frontend), docker return one of the container with this alias by using round robin algorithm. This is load balancing.


## Networking

- Three types of networks; 1. Bridged (default), 2. Host: Use same IP of host machine with specified port. 3. Macvlan: Container gets its own IP from your router.

- 1) Bridged: We have software level network interface docker bridge network. User maps (NAT) local IP to docker network (generally 172.x.x.x) when he runs a container: docker run -p 80:3000 . . . . etc.

- 2) Host: Container share the IP of host machine directly. For example fronend accessible at <host-ip>:80. Why I would use this? Performance. No need NAT like in above type, which is less complex, much faster. Also some protocols does not like NAT, so you should use this type.

- 3) Macvlan: Container gets its own IP from the router just like a virtual machine. The only thing you should know is that host machine and container cannot communicate each other for security reasons in linux kernel.



### Multi- Server Communication (The Overlay Network)

- Everything above are in a single computer, what if we have multiple computers around the world? We need an overlay network, which creates virtual subnet across multiple pyshical servers. It encapsulates traffic so that containers think they are in the same network.

- This is the foundation of Kubernetes and Docker Swarm.


## Docker compose

- We used commands like: 
docker run -dp 3000:3000 \
  -w /app -v "$(pwd):/app" \
  --network todo-app \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=secret \
  -e MYSQL_DB=todos \
  node:18-alpine \
  sh -c "yarn install && yarn run dev"

- But it is difficult to remember or edit this command, therefore we have docker-compose.yml file look like this:
services:
  app:
    image: node:18-alpine
    command: sh -c "yarn install && yarn run dev"
    ports:
      - 3000:3000
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos

  mysql:
    image: mysql:8.0
    volumes:
      - todo-mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: todos

volumes:
  todo-mysql-data:


- In the services part we have two containers: app and mysql. Mysql is fetched from remote but app is run by our Dockerfile. For the named volumes, we must also add it to the volumes at the end so that docker creates it before use.

## Best Practices

### Scanning

- To scan our image for vulnerabilities use docker scout (you must install scout plugin first). Then use command: docker scout quickview <image-name>       This will show vulnerab categorized by critical, high, medium, low and unspecified. To see what are the problems in detail use: docker scout cves <image-name>      This will show all problems with cvss score etc.


### Image Layering

- we can see how our image composed of in history by: docker image history <image-name>

IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
4ac38f2e4b6b   5 days ago      CMD ["node" "src/index.js"]                     0B        buildkit.dockerfile.v0
<missing>      5 days ago      RUN /bin/sh -c yarn install --production # b…   85.3MB    buildkit.dockerfile.v0
<missing>      5 days ago      COPY . . # buildkit                             4.59MB    buildkit.dockerfile.v0
<missing>      4 weeks ago     WORKDIR /app                                    0B        buildkit.dockerfile.v0
<missing>      10 months ago   CMD ["node"]                                    0B        buildkit.dockerfile.v0
<missing>      10 months ago   ENTRYPOINT ["docker-entrypoint.sh"]             0B        buildkit.dockerfile.v0
<missing>      10 months ago   COPY docker-entrypoint.sh /usr/local/bin/ # …   388B      buildkit.dockerfile.v0
<missing>      10 months ago   RUN /bin/sh -c apk add --no-cache --virtual …   5.37MB    buildkit.dockerfile.v0
<missing>      10 months ago   ENV YARN_VERSION=1.22.22                        0B        buildkit.dockerfile.v0
<missing>      10 months ago   RUN /bin/sh -c addgroup -g 1000 node     && …   114MB     buildkit.dockerfile.v0
<missing>      10 months ago   ENV NODE_VERSION=18.20.8                        0B        buildkit.dockerfile.v0
<missing>      11 months ago   CMD ["/bin/sh"]                                 0B        buildkit.dockerfile.v0
<missing>      11 months ago   ADD alpine-minirootfs-3.21.3-x86_64.tar.gz /…   7.83MB    buildkit.dockerfile.v0

- Each line is a layer.



### Layer Caching

- Once a layer changes, all layers above it recreated. Therefore seqeunce in your Dockerfile is important! For example, put the installion of packages to the top of the file, so that if code changes, package installion files are cached!

FROM node:18-alpine
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --production
COPY . .                                  # do this after installing packages, so that even code changes below layers stay same
CMD ["node", "src/index.js"]

- Also add some files to be ignored like node_modules not to override new packages. Create a .dockerignore file and put the name there. Check this out after a build:

 => CACHED [2/4] WORKDIR /app  
 => CACHED [3/4] COPY . .            
 => CACHED [4/4] RUN yarn install --production   


- These are cached, so much for faster builds.

