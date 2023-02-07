from setuptools import setup, find_packages

# import spire.build to initiate the monkeypatch
import spire.build

from package import name, version

setup(
    name=name,
    version=version,
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    package_data={"": ["*.jpg", "*.cmd", "*.ui"]},
)
