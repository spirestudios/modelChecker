name = "modelChecker"

version = "0.0.1"

authors = ["JakobKousholt"]

description = """
    Model Checker UI for Maya from a public github repo
    """

requires = []

variants = [["python-3.7"], ["python-3.9"]]

release_branches = [
    "main"
]

private_build_requires = ["rez_tools-1"]

build_command = "spire_build {install}"


def commands():
    env.PYTHONPATH.append("{root}/python")

def preprocess(this, data):
    # only allow release branches during rez release
    data["config"] = data.get("config", {})
    data["config"]["plugins"] = data["config"].get("plugins", {})
    data["config"]["plugins"].update({"release_vcs" : {"releasable_branches" : release_branches}})
