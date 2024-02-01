# Installing Docker on Amazon Linux 2

## Installation

The procedure to install Docker on AMI 2 (Amazon Linux 2) running on either EC2 or Lightsail instance is as follows:

1. Login into remote AWS server using the ssh command:

```ssh ec2-user@ec2-ip-address-dns-name-here```

2.Apply pending updates using the yum command

```sudo yum update```

3. Search for Docker package

```sudo yum search docker```

4. Get version information

```sudo yum info docker```

Outpot:

```commandline
Last metadata expiration check: 0:07:05 ago on Wed Sep 13 05:17:50 2023.
Available Packages
Name         : docker
Version      : 20.10.23
Release      : 1.amzn2023.0.1
Architecture : x86_64
Size         : 42 M
Source       : docker-20.10.23-1.amzn2023.0.1.src.rpm
Repository   : amazonlinux
Summary      : Automates deployment of containerized applications
URL          : http://www.docker.com
License      : ASL 2.0 and MIT and BSD and MPLv2.0 and WTFPL
Description  : Docker is an open-source engine that automates the deployment of any
             : application as a lightweight, portable, self-sufficient container that will
             : run virtually anywhere.
             : 
             : Docker containers can encapsulate any payload, and will run consistently on
             : and between virtually any server. The same container that a developer builds
             : and tests on a laptop will run at scale, in production*, on VMs, bare-metal
             : servers, OpenStack clusters, public instances, or combinations of the above.
```
5. Install docker

```sudo yum install docker```

6. Add group membership for the default ec2-user so you can run all docker commands without using the sudo command

```sudo usermod -a -G docker ec2-user```

7. Enable docker service at AMI boot time

```sudo systemctl enable docker.service```

8. Start the Docker service

```sudo systemctl start docker.service```

## Verification

Now that both required software installed, we need to make sure it is working. Hence, type the following commands.

1. Get the docker service status on your AMI instance

```sudo systemctl status docker.service```

2. See docker version

```sudo docker version```


## How to control docker service

1. Use the systemctl command as follows:

```commandline
sudo systemctl start docker.service #<-- start the service
sudo systemctl stop docker.service #<-- stop the service
sudo systemctl restart docker.service #<-- restart the service
sudo systemctl status docker.service #<-- get the service status
```

2. List images

```sudo docker images```

3. 


