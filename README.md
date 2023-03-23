# KEDEHub Git client

## KEDEHub

KEDEHub is a software as a service platform that has three main functions: analyzing Git repositories, calculating KEDE, and presenting results visually. KEDE calculation is based on the only scientific method for measuring the capability of software development organizations and is patented technology.

## Architecture

KEDEHub comprises three major components - Local client, SaaS platform, Organizational dashboard.

KEDE calculation is the heart of KEDEHub. It is based on the one and only scientific method for measuring capability of software development organizations. The technology is patented.

After KEDE is calculated it is presented in visual formats. There are many reports ready for use to compare the capability of developers, projects, teams and even companies.

### Local Git client
Local Git client is an application responsible for the analysis of local Git repositories. The client application needs to be installed on a computer with network access to the folders where the target Git repositories are cloned. One organization can have many such client applications installed on different computers. Each such client application can analyze a different set of Git repositories. For instance, eacn department can have their own Git repositories and their own KEDEHub client application. However, all data collected by all client applications will be stored under the company name. Hence we recommend organizations to maintain only one KEDEHub client application.

Tip: We recommend you to install only one KEDEHub local client for all your repositories.

In addition, Local client can connect to popular code-sharing platforms like GitHub, GitLab, and Bitbucket and clone Git repositories from there. Organizations can use this feature if they want to have all things related to KEDEHub isolated on a single computer. Such a computer can be maintained not by the developers and their line managers but by the operations or system administrators from another department.

Analysis is performed on local clones of Git repositories:

- Your source code and commit messages stay secure on your premisses with no transfer to KEDEHub.
- No capture of your intellectual property through analysis of the source code.
- No analysis of the commit messages.

Local client sends the results from the analysis to SaaS platform.

More informatio can be found [here](https://docs.kedehub.io/get-started/how-does-kedehub-work.html)

## How to provision a new company (example for EC2)

 Confing dir is: /home/ec2-user/.config/KedeGit

```commandline
cp docs/kede-config.json /home/ec2-user/.config/KedeGit
nano /home/ec2-user/.config/KedeGit/kede-config.json
```

```commandline
cp docs/empty_config.yaml /home/ec2-user/.config/KedeGit/config.yaml
nano /home/ec2-user/.config/KedeGit/config.yaml
```
Add values for name, user and token from your invitation email.

```commandline
cd ~/kedegit/
pip install -r requirements.txt 

```

```commandline
source ~/kedegit/env/bin/activate
python3 -m kedehub list-projects
deactivate
```

