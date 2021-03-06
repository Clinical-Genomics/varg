# Contributing to Varg

## Versioning
Varg adheres to [semantic versioning].

## Branch Model

Varg is using a github flow branching model as described in our [development manual][development-branch-model].

Files will be blacked automatically with each push to github. If you would like to automatically [Black][black-url] format your commits on your local machine:

```
pre-commit install
```

## Publishing

Bump the version according to semantic versioning locally on branch `master` using [bumpversion]:

```
bumpversion [major | minor | patch ]
```

Reinstall the application with the new version:

```
poetry install
```

Build and publish to PyPi:

```
poetry build
poetry publish
```

Push to git:
```
git push
git push --tag
```

This will trigger a new docker build using the git release tag as name.

[black-url]: https://github.com/psf/black
[bumpversion]: https://github.com/c4urself/bump2version
[development-branch-model]: http://www.clinicalgenomics.se/development/dev/models/
[semantic versioning]: https://semver.org/