from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.ci import GitlabCI
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git
from diagrams.programming.flowchart import Inspection
from diagrams.programming.language import Python

with Diagram(
    "Code Quality Assurance Workflow",
    show=False,
    direction="LR",
    curvestyle="curved",
):
    developer = Inspection("Developer")
    vcs = Git("Version Control")
    precommit = Python("Pre-Commit Hooks")
    localdev = Docker("Local Development Environment")

    with Cluster("GitLab CI/CD"):
        gitlabci = GitlabCI("GitLab CI/CD")
        ruff = Docker("Ruff Checks")
        black = Docker("Black Checks")

    further = Inspection("Merge to master")
    # Developer writes code and adds changes to stage
    developer >> Edge(label="Develop Code and\nAdd Changes to Stage") >> vcs

    # Changes are committed and pre-commit hooks are run
    (
        vcs
        >> Edge(label="Commit Changes")
        >> precommit
        >> Edge(label="Pre-Commit Checks")
        >> localdev
    )

    # Fixes from pre-commit hooks are added to stage
    localdev >> Edge(label="Add fixes from Pre-Commit to Stage") >> vcs

    # Changes are pushed to remote and CI/CD pipeline is triggered
    vcs >> Edge(label="Push to Remote and\nTrigger CI/CD Pipeline") >> gitlabci

    # Automated quality checks are run
    gitlabci >> Edge(label="Automated Quality Checks") >> [ruff, black]

    # If checks pass, changes are merged to master
    [ruff, black] >> further
