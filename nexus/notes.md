# notes

- Nexus is a centralized software used to store, manage and control software artifacts (Any file produced as a result of the software build process) which are used during software development like maven, npm, pypi (pip), docker images etc.
- Think like: I send my code to git repo. I send my build to nexus repo.
- It downloads once and all other users will get the packages from it (like a cache, mirror server). This is perfect because: network optimization, faster build, overall control and security (perfect for air-gapped systems)
- For overall control and security: we can trigger AV scan for new downloaded artifacts once than distribute it. if it is malicious block it.

- There are 3 types of repos: Hosted: you store your own artifacts. Proxy: cache artifacts from external repositories. Group: you do both. good for simplicity.
- For the best use case, create group repo and give that url to devices. Because later you can freely add or remove hosted/proxy repos to that group but the URL of that group will never change.

- To use Nexus on the air-gapped systems, create hosted repo instead of proxy. Download the packages on the low network and transfer those files to high network using design that I mention in air-gapped-systems folder. After that packages will be uploaded to the Nexus repo.

- There are many kind of repo types: Maven: Java artifacts (JARs, WARs) and plugins. Used by Maven or Gradle. npm: Stores JavaScript packages. Used by npm and yarn. Docker: Container images. Private docker registry. PyPI: Python packages, used by pip. NuGet: .NET packages, used by VS or dotnet CLI. Raw: zip, tar.gz etc. APT/YUM: linux packages.

## Example with Maven

- Nexus already created Maven repos by default. We have maven-public, this is a maven2 group. In this group we have 1 proxy (maven central) and 2 hosted repos (releases and snapshots). Normally, we have 1 hosted and 1 proxy. But for java we generally have second hosted repo "snapshots". This repo is for nightly builds, which means you can change the release but name it with same release number. (you cannot do this in releases repo).

- In the dev computer, edit ~/.m2/settings.xml file. We configure as two parts, downloading and uploading. For the download part, we will use maven public which already combines central, releases and snapshots. For the upload part, we cannot directly write to a group (maven-public), instead we must specify which repo to write. 
- in the xml file, we first have mirror section, we put our url there. Then we have servers section which is for auth. We must have 3 server section for our example here.  One for downloading from public repo, one for uploading to  snapshots and one for uploading to releases repo.

<settings>
  <servers>
    <server>
      <id>nexus-public</id> <username>admin</username>
      <password>YOUR_PASSWORD</password>
    </server>

    <server>
      <id>nexus-snapshots</id> <username>admin</username>
      <password>YOUR_PASSWORD</password>
    </server>

    <server>
      <id>nexus-releases</id> <username>admin</username>
      <password>YOUR_PASSWORD</password>
    </server>
  </servers>

  <mirrors>
    <mirror>
      <id>nexus-public</id>
      <mirrorOf>*</mirrorOf> <url>http://192.168.1.175:8081/repository/maven-public/</url>
    </mirror>
  </mirrors>
</settings>

- Then in the project dir, we have pom.xml, we put our release and snapshot repos there in distributionManagement section:

  <distributionManagement>
    <snapshotRepository>
      <id>nexus-snapshots</id>
      <url>http://192.168.1.175:8081/repository/maven-snapshots/</url>
    </snapshotRepository>

    <repository>
      <id>nexus-releases</id>   <url>http://192.168.1.175:8081/repository/maven-releases/</url>
    </repository>


  </distributionManagement>


- And now when we deploy the project, mvn deploy, our artifact goes to releases or snapshots according to our version 1.0.0-SNAPSHOT OR 1.0.0 


## Example with .NET

dotnet pack


- This is for upload

dotnet nuget add source http://192.168.1.175:8081/repository/nuget-hosted/ \
  --name nexus-hosted \
  --username admin \
  --password PASSWORD \
  --store-password-in-clear-text

-Upload the artifact
dotnet nuget push bin/Release/*.nupkg --source nexus-hosted --api-key 123  #api key is just for syntax


- This is for download

dotnet nuget add source http://192.168.1.175:8081/repository/nuget-group/index.json \
  --name nexus-group \
  --username admin \
  --password PASSWORD \
  --store-password-in-clear-text

- Install the artifact
dotnet add package MyDotnetLib --version 1.0.0


## Example with Docker


- nano /etc/docker/daemon.json, paste this to allow http access if no nginx. These are ip and port of nexus server.
{
  "insecure-registries" : ["<ip>:<port>"]
}



- Set http connector to a port in the docker repo in nexus

- docker login <ip>:<port>
- docker tag <local-image> <ip>:<port>/<remote-image-name>
- docker push <ip>:<port>/<remote-image-name>


- docker pull <ip>:<port>/<remote-image-name>



## Summary

- With nexus, we put our artifact to a local repo. 
- Use cache so that everything is fast.
- Team sharing: one team writes a module, release it and other team install it and use in their own code.
- You cannot push private code to public Docker Hub, so you push to your private nexus Docker Registry.
- Security and governance 
