# KEDEHub Git client (KEDEGit)

## KEDEHub

KEDEHub is a software as a service platform that has three main functions: analyzing Git repositories, calculating KEDE, and presenting results visually. KEDE calculation is based on the only scientific method for measuring the capability of software development organizations and is patented technology.

## Architecture

KEDEHub comprises three major components - Local client, SaaS platform, Organizational dashboard.

KEDE calculation is the heart of KEDEHub. It is based on the one and only scientific method for measuring capability of software development organizations. The technology is patented.

After KEDE is calculated it is presented in visual formats. There are many reports ready for use to compare the capability of developers, projects, teams and even companies.

More information can be found [here](https://docs.kedehub.io/get-started/how-does-kedehub-work.html)

### Local Git client (KEDEGit)

KEDEGit is a local Python application responsible for:
- Analyzing local Git repositories
- Sending commands to the KEDEHub SaaS

The client application KEDEGit must be installed on a computer with network access to the folders where the target Git repositories are cloned. 
One organization can have multiple client applications installed on different computers, each analyzing a different set of Git repositories. 
For example, each department may have its own Git repositories and its own KEDEGit client application. 
However, all data collected by all KEDEGit client applications will be stored under the company name. 
Therefore, we recommend organizations maintain only one KEDEGit client application.

Tip: We recommend installing only one KEDEGit local client for all your repositories.

Furthermore, the KEDEGit client can connect to popular code-sharing platforms like GitHub, GitLab, and Bitbucket, and clone Git repositories from these platforms. 
Organizations can use this feature if they want to centralize all KEDEHub-related activities on a single computer. 
This computer can be maintained by operations or system administrators from another department, instead of developers and their line managers.

Analysis is performed on local clones of Git repositories, ensuring:

- Your source code and commit messages remain secure on your premises, with no transfer to KEDEHub
- No capture of your intellectual property through source code analysis
- No analysis of commit messages

Local client sends the results from the analysis to the SaaS platform.

More information can be found [here](https://docs.kedehub.io/kedehub/kedehub-kedegit.html)

## Using KEDEGit

All you need to know is in the [How to use KEDEGit](./docs/howto.md) document.

## Get involved

Contributions are welcome! Go ahead and file Issues or open Pull Requests.

## License

[Apache 2.0](https://github.com/kedehub/kedegit/blob/master/LICENSE)
