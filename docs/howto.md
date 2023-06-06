# How to use KEDEGit

This document shows how to use only the most used commands.
Detailed information can be found [here](https://docs.kedehub.io/kedehub/kedehub-kedegit.html)

## Provision a new company

### Configuration directory

KEDEGit uses [Confuse](https://confuse.readthedocs.io/en/latest/index.html) for managing its configuration.
In our case the application name is KedeGit.
The configuration paths for different platforms are listed [here](https://confuse.readthedocs.io/en/latest/usage.html#search-paths). 
Users can also add an override configuration directory with an environment variable. 
The environment variable name for KEDEGit is KEDEGITDIR.

This guide shows how to use KEDEGit on Amazon EC2 

For EC2 the configuration directory is: 
```commandline
/home/ec2-user/.config/KedeGit
```
You need to create it before proceeding further.

````commandline
mkdir ~/.config/KedeGit
````

### Configure KEDEGit

#### Allowed and excluded file types
```commandline
cp docs/kede-config.json /home/ec2-user/.config/KedeGit

nano /home/ec2-user/.config/KedeGit/kede-config.json
```
Change the file if needed to match your architecture, technology and preferences.

#### Set configuration file 
```commandline

cp docs/empty_config.yaml /home/ec2-user/.config/KedeGit/config.yaml
```
Open <em>config.yaml</em> and add values for company name, user and token from your invitation email.
```commandline
nano /home/ec2-user/.config/KedeGit/config.yaml
```
```commandline
server:
    protocol: https
    host: api.kedehub.io
    port: 443

company:
    name:
    user:
    token:
```

### Instal virtualenv
```commandline
pip install virtualenv
```

### Install KEDEGit in virtual environment
```commandline
git clone https://github.com/kedehub/kedegit.git kedegit

cd kedegit/

python3 -m virtualenv env

source ~/kedegit/env/bin/activate

pip install pip --upgrade

pip install -r requirements.txt

pip3 install python-Levenshtein

pip3 install numpy --upgrade

deactivate
```
#### Test if everything is OK
```commandline
source ~/kedegit/env/bin/activate

python3 -m kedehub list-projects

deactivate
```
That command should list all projects for a company. 
If the company has no projects yet nothing will be listed. 

## Initializing a New Project

Create a new project called NEW_PROJECT, consisting of a local Git repository located at  `~/git/repo_1`.


```commandline
python3 -m kedehub init-project NEW_PROJECT ~/git/repo_1
```


## Adding a New Repository to an Existing Project

Add a new local Git repository located at `~/git/repo_2` to `NEW_PROJECT`.
```commandline
python3 -m kedehub add-repository NEW_PROJECT ~/git/repo_2
```

## Updating Project Statistics

The <strong>update-projects</strong> ccommand performs the following actions:

- Analyzes all new commits
- Calculates KEDE and other statistics for the new commits

### Updating Specific Project Statistics
To update the statistics for a single existing project, execute:
```commandline
python3 -m kedehub update-projects -p NEW_PROJECT
```

To update the statistics for multiple existing projects, execute:
```commandline
python3 -m kedehub update-projects -p NEW_PROJECT_1 NEW_PROJECT_2
```
### Updating All Project Statistics
To update the statistics for all projects within a company with new code contributions, execute:
```commandline
python3 -m kedehub update-projects
```
## Fixing Incorrectly Calculated KEDE for a Project
After completing the addition of repositories to a project, it is recommended to recalculate KEDE. Recalculate KEDE for `NEW_PROJECT`.
```commandline
python3 -m kedehub fix-kede -p NEW_PROJECT
```

## Updating Local Project Repositories
New code is constantly contributed to all company repositories. To update local repositories from remote sources (performing a git pull), use the following command for all company projects:
```commandline
python3 -m kedehub update-repos
```
`


