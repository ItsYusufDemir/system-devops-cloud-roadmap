# source

- https://www.geeksforgeeks.org/devops/what-is-ci-cd/

# notes

- Continues Integration (CI): 1. commit. 2. build to get an artifact (executable file). 3. auto test
- Continues Delivery/Deployement: Then, send the build to stagin area. Then goes to prod environement. if manuel: continues delivery, if auto: continues deployement

- so CI/CD pipeline: new commit => build => test => deploy
- Truth: No test = No CI
- Also, when there is a new feature, dev also must commit its tests. However, you might think it is nonsense if he deos not. But actually, even he does not commit new tests, with CI we test the integration with older test files so that any bad change in the code make other tests fail.

- on GitHub you can simply use GitHub Actions for CI. Just find a template and change parts according to your needs. Lets see some of the keywords. on: when to trigger the job (generally when I push or merge). jobs: what to run. steps: specific commands. uses: use a plugin like actions/setup-python@v4. run: runs code directly in the machine.

- I created an example config. In that example, we have two jobs: CI and then CD. In the CD part, we first set where to run this code (ubuntu-lates is ok). Then in the steps container, there is "uses: actions/checkout@v3", this line checks out to the triggered commit by using checkout plugin version 3. Then we add a name for next one (just for readibility in the config and Github Actions page) and it uses setup-python version 4 plugin to setup python environment. With "with" keyword, we determine which python version.
- Later, we first install our dependencies by using the requirements.txt. This time we directly run code on the ubuntu machine, not using a plugin.
- Later, we run our test_app.py here and we are done with the CI part.

- Now, lets look at to the CD job. Here have a new keyword "needs: test-code" This keyword make this job wait until test is done. Then we use a appleboy/ssh-action@master plugin (master means latest version). I provide some info by using the "with" keyword like host, username, ssh key and script to run. But be careful, do not these as plain text! Instead, use GitHub Secrets. In the script part, we pull the latest code, dockerize our code and run the docker app.

- once you create your yaml file, you can upload it from GitHub actions page or manually by uploading .gihub/workflows/*.yaml dir in your repo. 
- After a commit, this workflow will run and we are done with implementing CI/CD by using GitHub Actions.