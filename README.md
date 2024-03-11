# ayapingping-py

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ayapingping-py)
![PyPI - Version](https://img.shields.io/pypi/v/ayapingping-py)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ayapingping-py)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/dalikewara/ayapingping-py)
![GitHub license](https://img.shields.io/github/license/dalikewara/ayapingping-py)

**ayapingping-py** generates standard project structure to build applications in Python that follow Clean
Architecture and Feature-Driven Design concept.

> Golang Version: [ayapingping-go](https://github.com/dalikewara/ayapingping-go)

## Getting started

### Requirements

- Python>=3.10.12

### Installation

You can use the `pip install` method:

```bash
pip install ayapingping-py
```

#### Possible issue

If you're facing a warning or an issue like this, for example:

```text
WARNING: The script ayapingping-py is installed in '/home/dalikewara/.local/bin' which is not on PATH.
Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

Then you can install it using the `--user` option, for example:

```bash
pip install --user --force-reinstall ayapingping-py
```

Or if it doesn't work, you can add the directory containing the scripts to your **PATH** manually.
Open your shell configuration file (e.g., `.bashrc`, `.zshrc`, or similar) and add the following line:

```bash
export PATH=$PATH:/home/dalikewara/.local/bin
```

Then, restart your shell or run:

```bash
source ~/.bashrc   # or source ~/.zshrc
```

This will make the changes take effect immediately.

### Usage

To generate a new project, simply run the `ayapingping-py` command:

```bash
ayapingping-py
```

Then enter your project name. After you confirm your inputs, the **ayapingping-py** generator will set up the project for you.

![Alt Text](https://lh3.googleusercontent.com/drive-viewer/AKGpihZVKfRP1YbgPEilKjEypqE84gyuFpsONb8qqVY2qrnZsAkBo68gqR1UioKlq0G2gW_kCZqFVIPYA7kbRJBrRqb-vl3OnA=w840-h939)

> The animated example uses the Golang version, but it essentially follows the same approach

### What's next?

Simply start working on your project and make changes.

## Project Structure

To implement the concept of Clean Architecture and ~~Domain-Driven Design~~ Feature-Driven Design, and to keep them understandable, we structure the project like this:

### main.py

- In this file, you initialize dependencies, injections, and anything required to start and run your application.
- You can use the command `venv/bin/python main.py`, `python main.py` or `make start` to run your application.

### domain

- The **Domain** represents your primary business model or entity
- Define your main object models or properties for your business here, including database models, DTOs (Data Transfer Objects), etc
- Keep this package as straightforward as possible. Avoid including any code that is not directly related to the model itself
- If a **Feature** imports anything from this location, and you want the **Feature** to be accessible through the `importFeature` command 
without the risk of missing package errors, **DON'T FORGET** to include them in the `features/yourFeature/dependency.json` file

### features

- A **Feature** encapsulates your main business feature, logic, or service
- Here, you include everything necessary to ensure the proper functioning of the feature
- Please prioritize **Feature-Driven Design**, ensuring that features can be easily adapted and seamlessly integrated and imported into different projects
- If another **Feature** imports anything from this location (the current **Feature**), and you want the current **Feature** to be 
accessible through the `importFeature` command without the risk of missing package errors, **DON'T FORGET** to include them in the `dependency.json` file
- The `dependency.json` is **OPTIONAL**, and **ONLY USEFUL WHEN** you use the `importFeature` command. It serves to define
the **Feature** dependencies and avoids possible missing package errors
- A standard **Feature** comprises the following parts: `delivery`, `repositories`, `usecases` and `utility`
  - **delivery**
    - Hosts feature handlers like HTTP handlers, gRPC handlers, cron jobs, or anything serving between the client and your application or feature
    - For config variables, external clients, or use cases, pass or inject them as dependencies
  - **repositories**
    - Handles communication with external data resources like databases, cloud services, or external services
    - Keep your repositories as simple as possible; avoid adding excessive logic
    - If necessary, separate operations into smaller methods
    - Changes outside the `repositories` should not affect them (except changes for business domain/model/entity)
    - For config variables, database frameworks, or external clients, pass or inject them as dependencies
  - **usecases**
    - Contains the main feature logic
    - Changes outside the `usecases` should not impact them (except changes for business domain/model/entity and repositories)
    - For config variables, external clients, or repositories, pass or inject them as dependencies
  - **utility**
    - Accommodates functions tailored to help with common tasks specifically for the **Feature**—treat them as helpers
- Feel free to adopt your own style as long as it aligns with the core concept

### common

- In this place, you can implement various functions to assist you in performing common tasks—consider them as helpers
- Common functions can be directly called from any location
- If a **Domain** or **Feature** imports anything from this location, and you want the **Feature** to be accessible through 
the `importFeature` command without the risk of missing package errors, **DON'T FORGET** to include them in the `features/yourFeature/dependency.json` file

### infra

- This is the location to house infrastructure configurations or scripts to facilitate the deployment of your project on a server or VM

### Make It Your Own

Feel free to create your own style to suit your requirements, as long as you still follow the main architecture concept. 
You can create folders such as `migration` to store your database migrations, `tmp` for temporary files, etc.

## Importing Features from Another Project

To seamlessly incorporate or import features from another project, use the `importFeature` command:

```bash
ayapingping-py importFeature [feature1,feature2,...] from [/local/project or https://example.com/user/project.git or git@example.com:user/project.git]
```

For example:

```bash
ayapingping-py importFeature exampleFeature from /path/to/your/project
```

```bash
ayapingping-py importFeature exampleFeature1,exampleFeature2 from git@github.com:username/project.git
```

### Feature dependency

If your feature relies on external packages, it's crucial to address dependencies properly during the import process. 
Failure to import necessary dependencies may result in missing packages. To prevent this, please document your feature 
dependencies in the `dependency.json` file. Supported dependencies are limited to the following directories: `domain`, `common`, and `features`.
Ensure that your feature dependencies strictly adhere to these directories, avoiding reliance on other locations.
You can also include any external packages to `requirements` param to install them automatically.

Example `dependency.json` file:

```json
{
  "domains": [
    "example.py"
  ],
  "features": [],
  "commons": [
    "time_now.py",
    "validate_username.py"
  ],
  "requirements": [
    "python-dotenv==1.0.1",
    "mysql-connector-python==8.3.0",
    "Flask==3.0.2"
  ]
}

```

## Importing Domains from Another Project

To import domains from another project, use the `importDomain` command:

```bash
ayapingping-py importDomain [domain1.py,domain2.py,...] from [/local/project or https://example.com/user/project.git or git@example.com:user/project.git]
```

For example:

```bash
ayapingping-py importDomain example.py from /path/to/your/project
```

```bash
ayapingping-py importDomain example.py,example2.py from git@github.com:username/project.git
```

## Importing Common Functions from Another Project

To import common functions from another project, use the `importCommon` command:

```bash
ayapingping-py importCommon [commonFunction1.py,commonFunction2.py,...] from [/local/project or https://example.com/user/project.git or git@example.com:user/project.git]
```

For example:

```bash
ayapingping-py importCommon example_function.py from /path/to/your/project
```

```bash
ayapingping-py importCommon example_function1.py,example_function2.py from git@github.com:username/project.git
```

## Release

### Changelog

Read at [CHANGELOG.md](https://github.com/dalikewara/ayapingping-py/blob/master/CHANGELOG.md)

### Credits

Copyright &copy; 2024 [Dali Kewara](https://www.dalikewara.com)

### License

[MIT License](https://github.com/dalikewara/ayapingping-py/blob/master/LICENSE)
