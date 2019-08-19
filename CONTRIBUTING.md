# Contributing

Contributions are welcomed!

When contributing to this repository, please first discuss the change you wish to make via a GitHub
issue before making a change.  This saves everyone from wasted effort in the event that the proposed
changes need some adjustment before they are ready for submission.

## Building and Testing

To setup your environment with the required dependencies:
```
pip install -r requirements.txt
pip install -r dev-requirements.txt
```

Note that we follow PEP8 standards with a 120 character line limit. This is enforced by the Travis build system on all
pull requests.

To build and run all tests:
```
pytest
```

We also run a number of additional scans to ensure the security of this package.  See [.travis.yml](/.travis.yml) for
the full set of tests run by our build system.

## Pull Request Process

1. If your changes include multiple commits, please squash them into a single commit.  Stack Overflow
   and various blogs can help with this process if you're not already familiar with it.
2. Update the README.md where relevant.
3. Update the CHANGELOG.md with details of the change and referencing the issue you worked on.
4. When submitting your pull request, please provide a comment which describes the change and the problem
   it is intended to resolve. If your pull request is fixing something for which there is a related GitHub issue,
   make reference to that issue with the text "Closes #<issue-number>" in the pull request description.
5. You may merge the pull request to master once a reviewer has approved it. If you do not have permission to
   do that, you may request the reviewer to merge it for you.

## Releasing

As a project maintainer you will need to release this project to push a new Docker image to Docker Hub, e.g. once a pull request has been merged.

Create a release in GitHub, with the contents of the Changelog for that release version. This will create a tag, for
which Travis will build and publish an image.

This project follows the [Semantic Versioning](https://semver.org/) specification, and version numbers
should be chosen accordingly.

## Contributor Code of Conduct

As contributors and maintainers of this project, and in the interest of fostering an open and
welcoming community, we pledge to respect all people who contribute through reporting issues,
posting feature requests, updating documentation, submitting pull requests or patches, and other
activities.

We are committed to making participation in this project a harassment-free experience for everyone,
regardless of level of experience, gender, gender identity and expression, sexual orientation,
disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery
* Personal attacks
* Trolling or insulting/derogatory comments
* Public or private harassment
* Publishing other's private information, such as physical or electronic addresses, without explicit
  permission
* Other unethical or unprofessional conduct.

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits,
code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct. By
adopting this Code of Conduct, project maintainers commit themselves to fairly and consistently
applying these principles to every aspect of managing this project. Project maintainers who do not
follow or enforce the Code of Conduct may be permanently removed from the project team.

This code of conduct applies both within project spaces and in public spaces when an individual is
representing the project or its community.

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by opening an
issue or contacting one or more of the project maintainers.

This Code of Conduct is adapted from the [Contributor Covenant](http://contributor-covenant.org),
version 1.2.0, available at
[http://contributor-covenant.org/version/1/2/0/](http://contributor-covenant.org/version/1/2/0/)

