import git
from kedehub.gitclient.git_utility import get_git_repository
from kedehub import bcolors


def update_repositories(repositories):

    shouldFF = promptForFF()

    try:
        for repo in repositories:
            currentLocation = repo.repository_path
            try:
                repo = get_git_repository(currentLocation)
                assert not repo.bare
                printRepo(repo, currentLocation, shouldFF)
            except git.exc.NoSuchPathError as exception:
                continue
                print("NoSuchPathError: ", exception)
                printSpace()
            except git.exc.InvalidGitRepositoryError as exception:
                continue
                print("InvalidGitRepositoryError: ", exception)
                printSpace()
    except FileNotFoundError as exception:
        print(bcolors.FAIL + "Repo location: \"" + currentLocation + "\" not valid. Please try again." + bcolors.ENDC)


# Prints a space in the console
def printSpace():
    print("\n")

# Ask if the user wants to automatically ff branches when possible
# https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging
# when you try to merge one commit with a commit that can be reached by following the first commit’s history,
# Git simplifies things by moving the pointer forward because there is no divergent work to merge together -
# this is called a “fast-forward.”
# In other words - If Master has not diverged, instead of creating a new commit,
# git will just point master to the latest commit of the feature branch. This is a “fast forward.”
def promptForFF():
    userInput = input(
        bcolors.HEADER + " Automatically fast forward branches when possible? (y/n): " + bcolors.ENDC).lower()
    if (userInput == "y" or userInput == "Y" or userInput == "yes" or userInput == "YES" or userInput == "YEAH"):
        return True
    else:
        return False


def printRepo(repo, repoLocation, shouldFF):
    repoPath = str(repo).split("/")
    repoName = repoPath[len(repoPath) - 2] + ".git"
    print(bcolors.OKBLUE + "Repository Name: ", repoName, bcolors.ENDC)
    print(repoLocation)

    url = getRepositoryUrl(repo)
    print(url)
    # Fetch update each remote in the repo
    print("# Remotes: ", len(repo.remotes))
    for remote in repo.remotes:
        try:
            remote.fetch(prune=True)
        except Exception as e:
            message = e.stderr
            print("\t", bcolors.FAIL, "There was a problem ", str(message), ": ", e, bcolors.ENDC)
            return

    branches, anyBranchBehind = listBranches(repo, url)
    printUncommittedChanges(repo)

    # Only FF if a) user said yes, and b) if any branch is behind HEAD
    if (shouldFF and anyBranchBehind == True):
        print("Now fast-forwarding", len(branches), "branches in this repository:")
        updateBranches(repo, branches)
        printSpace()
    # If the shouldFF flag is on, but none of the branches are behind, then no need to FF.
    elif (shouldFF and anyBranchBehind == False):
        print("No need to fast-forward. No branches are behind in this repository.")
        printSpace()


def updateBranches(repo, branches):
    git = repo.git
    result = ""
    for branch in branches:
        try:
            result = git.pull('origin', branch, "--ff-only")
            # For instance, you are on master and git fetch has brought new upstream commits into origin/master.
            # If your local master has no changes, then it can be fast-forwarded: simply updated to point to the same commit as the latestorigin/master.
            # Usually, no special steps are needed to do fast-forwarding; it is done by merge or rebase in the situation when there are no local commits.
            print("\t" + bcolors.HEADER, str(branch).strip(), bcolors.ENDC, "pulled: " + result)
        except Exception as e:
            message = e.stderr
            if ("Couldn't find remote ref" in message):
                # Local branch only, this branch DNE in remote repository
                print("\t" + bcolors.HEADER, str(branch).strip() + ":", bcolors.ENDC, bcolors.FAIL,
                      "Couldn't find remote ref.", bcolors.ENDC)
            else:
                # Some other kind of issue. for example:
                # Fast forwarding is not possible when the new HEAD is in a diverged state relative to the stream you want to integrate.
                # For instance, you are on master and have local commits, and git fetch has brought new upstream commits into origin/master.
                # The branch now diverges from its upstream and cannot be fast forwarded: your master HEAD commit is not an ancestor of origin/master HEAD.
                # To simply reset master to the value of origin/master would discard your local commits.
                # The situation requires a rebase or merge.
                print("\t", bcolors.FAIL, "There was a problem fast-forwarding ", str(branch), ": ", e, bcolors.ENDC)


def printUncommittedChanges(repo):
    uncommitted = repo.is_dirty()
    if uncommitted:
        # Current repository has uncommitted changes... retrieve a list of changed files
        changed_files = [item.a_path for item in repo.index.diff(None)]
        print([len(changed_files)], "Modified Files:")
        for x in changed_files:
            # Just print out each changed file
            print(bcolors.FAIL + '\t', x + bcolors.ENDC)

        # Print "untracked" files
        untracked_files = repo.untracked_files

        if (len(untracked_files) > 0):
            print([len(untracked_files)], "Untracked Files:")
            for x in untracked_files:
                # Just print out each changed file
                print(bcolors.FAIL + '\t', x + bcolors.ENDC)
        else:
            print("[0] Untracked Files.")
    else:
        print("[0] Uncommitted changes." + bcolors.OKGREEN + "\n\tRepository is clean." + bcolors.ENDC)
    printSpace()


def getRepositoryUrl(repo):
    git = repo.git
    # Command to get URL for repository: (your_remote)
    # git config --get remote.origin.url
    remoteUrl = git.config('--get', 'remote.origin.url')
    return remoteUrl


# Git commands used for this:
# git remote show origin | grep "HEAD branch" | cut -d ":" -f 2
# Gets the default branch of the current repository.
def getDefaultBranch(repo, url):
    git = repo.git
    defaultBranchInfo = git.remote('show', url).split("\n")
    defaultBranch = ""
    for info in defaultBranchInfo:
        if ("HEAD branch" in info):
            defaultBranch = info.split(':')[1].strip()
            break
    if (defaultBranch == ""):
        defaultBranch = "master"
    # print("defaultBranch:", defaultBranch)
    return defaultBranch


# Prints out all of the branches in the repository, along with how far ahead/behind they are to the HEAD branch
def listBranches(repo, url):
    anyBranchBehind = False
    branchList = repo.branches
    defaultBranch = getDefaultBranch(repo, url)

    print([len(branchList)], "Branches:")
    for branch in branchList:
        branchDiffModifier = "origin/" + defaultBranch + "..." + str(branch)
        output = repo.git.rev_list('--left-right', '--count', branchDiffModifier).split()

        behind = output[0]
        ahead = output[1]
        behindLabel = ("-" + behind) if behind == "0" else (bcolors.WARNING + "-" + behind + bcolors.ENDC)
        aheadLabel = ("+" + ahead) if ahead == "0" else (bcolors.OKGREEN + "+" + ahead + bcolors.ENDC)
        commitDifLabel = "[" + behindLabel + "\t" + aheadLabel + " to origin/master]"

        if behind != "0":
            anyBranchBehind = True
        if repo.active_branch == branch:
            print("\t", commitDifLabel, "\t", bcolors.HEADER, branch, bcolors.ENDC, bcolors.WARNING, "(*)",
                  bcolors.ENDC)
        else:
            print("\t", commitDifLabel, "\t", bcolors.HEADER, branch, bcolors.ENDC)
    return branchList, anyBranchBehind;