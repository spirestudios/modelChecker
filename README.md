<h1 align="center">modelChecker</h1>

modelChecker is a python plug-in written for Autodesk Maya to sanity check digital polygon models. It is unopinionated, provides concise reporting, and lets you select your error nodes easily. Maya_ext uses it to validate assemblies and components on publish, but offers it as a standalone validation tool as well.

![modelChecker](./modelChecker.png)

## Usage

There are three ways to run the checks.

1. If you have objects selected, the checks will run on the current selection. Select objects in object mode. (component mode won't work).
2. On a hierarchy by declaring a root node in the UI.
3. The checks will run on the entire scene if nothing is selected and the root node field is left empty.

## Repo forked from original authors
- [**Jakob Kousholt**](https://www.linkedin.com/in/jakobjk/) - Software Engineer
- [**Niels Peter Kaagaard**](https://www.linkedin.com/in/niels-peter-kaagaard-146b8a13) - Senior Modeler at Weta Digital

## Spire Maintainer
- [**Grant Bowlds**]


## License

modelChecker is licensed under the [MIT](https://rem.mit-license.org/) License.
