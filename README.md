# Amalgam

A case study of creating a microservices-ready monolith.

In this repo, you can see:

- how to generate microservices-ready monolith
- how to run your application as a monolith
- how to run the same application as microservices
- (soon) how to deploy to Kubernetes (using docker-desktop)

# How to re-generate

```bash
./init.sh
```

Please open [init.sh](init.sh) to see the details.

# How to run your application as a monolith

```bash
cd myProject
zaruba please startMyApp

# (or run as container)
# zaruba pleaase startMyAppContainer
# (ctrl + c)
# zaruba please stopContainers
```

# How to run your application as a microservices

```bash
cd myProject
zaruba please startMyMicroservices

# (or run as containers)
# zaruba please startMyMicroservicesContainer
# (ctrl + c)
# zaruba please stopContainers
```

# How to deploy to Kubernetes

```bash
cd myProject
zaruba please deploy
# (zaruba please destroy)
```


# What is a microservices-ready monolith?

Microservices-ready monolith is a monolith application that can also be deployed as microservices.

We can create a microservices-ready monolith by using:

- Feature flags
- Interface and layered architecture

Please visit [this guide](myProject/myApp/_docs/README.md) for more information.