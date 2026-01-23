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


