# Versa EDM Backend README

The backend server for the Versa Election Data Manager system, also known as **VersaDM**.

VersaDM is the part of [ElectOS](https://electos.org/) that provides a back-end API to a web UI front-end. VersaDM also validates JSON data using pydantic. Written in Python, distributed in Docker.

## More Information about VersaDM

* Check out the [RELEASE-NOTES](RELEASE-NOTES.md) for the latest technical info on VersaDM features.
* Read the [NIST Special Publication 1500-100, Election Results Common Data Format Specification (Revision 2.0: PDF, 11.3MB)](docs/NIST.SP.1500-100r2.pdf) for a detailed description of the election data model this software implements, or check it out on GitHub: [usnistgov/ElectionResultsReporting at version2](https://github.com/usnistgov/ElectionResultsReporting/tree/version2). VersaDM conforms to this NIST specification.
* Review the [docs](docs/) folder in this repo for more helpful documentation and other useful information about this project and the data specification it implements.
* The VersaDM software is licensed under the [OSET Public License v2.1.1](LICENSE.md)

## Getting Started

To run the code in this repo, you need Python 3.9 or greater installed correctly on your development workstation.

### Using Poetry

We use [Poetry for Python dependency management and packaging](https://python-poetry.org/) for continuous development and integration work. If you're interested in working with the code in this repo, follow the instructions to [install poetry on your development workstation](https://python-poetry.org/docs/#installation).

Then, you can [set up your development environment with poetry](https://python-poetry.org/docs/basic-usage/). This consists of entering the following command in the project root directory:

```bash
poetry install
```

Once the poetry installation is complete, you may invoke your new virtual environment by entering:

```bash
poetry shell
```

Some editors or IDEs, such as VSCode, will open the poetry shell automatically if you specify the Python interpreter in the same direcory as the poetry-created virtual environment.

## Installing package releases from code

For package releases of VersaDM, we use the following Python tools:

* `pip`
* `venv`

First, create your virtual environment with `venv`.

### Set up venv

This Python repo supports using the virtual environment tool, `venv`, included by default with Python. To set up `venv`, **go to the project root directory** and enter:

```bash
python -m venv ./venv
```

This command works on Windows, Mac and Linux (although you may need to substitute `python3` for your platform, or use the backslash for Windows).

This project's `.gitignore` file already includes a line to ignore the entire `./venv/` directory, which is an excellent reason to use it as your virtual environment directory name.

Depending on your platform, you'll need to activate your virtual environment after it's created. Note that some code editors and IDEs, like VSCode, will start the virtual environment automatically if you point to the Python interpreter in in your `venv` directory.

Generally, it's best to use only one type of virtual environment at a time, (for example, either `poetry` or `venv`) even though this repo supports multiple Python packaging tools.

#### Activating venv in Windows 10 with PowerShell

In the repo root directory, enter these commands in PowerShell:

```bash
cd .\venv\Scripts\
.\Activate.ps1
```

These commands should also work in Windows 11.

#### Activating venv in Linux or Mac with bash

At a bash prompt, enter this command at the root of the project folder:

```bash
source ./venv/bin/activate 
```

This command will work in any bash environment, including WSL (Windows Subsystem for Linux).

#### Activating venv in Linux or Mac with fish or other shells besides bash

Venv includes activation scripts for other shells besides bash. For example, if you're using fish as your shell, you can activate venv like this:

```fish
set VIRTUAL_ENV "/home/myname/repos/forks/VersaEDM-Backend/venv"
```

Note the use of an absolute path to set this environment variable; yours will of course be different.

Check the contents of the `./venv/bin/activate` directory for other shell-specific activation scripts.

### Installing required packages

Once `venv` is active, your command line should display `(venv)` at the beginning of the command prompt. Installing `venv` will also install `pip` in your virtual environment, which you can then use to install the required Python packages, as follows:

```bash
pip install -r requirements.txt
```

Or, you can install the development requirements, which will also install the basic requirements.

```bash
pip install -r requirements-dev.txt
```

Either command will ensure you've installed the correct versions of each required package.

## Setup Docker

To run the API, you'll also need to install Docker.

### Installing Docker in Windows 10

We recommend using [chocolately](https://chocolatey.org/) to install the current version of the Docker Desktop package.

### Installing Docker in Linux

Install the latest docker using snap:

```bash
sudo snap install docker
```

### Installing Docker on the Mac

You'll need to install a specific build of Docker on your Mac, depending on which type of CPU you have (Apple Silicon or Intel). See [Install Docker Desktop on Mac | Docker Documentation](https://docs.docker.com/desktop/mac/install/) for detailed instructions.

### Build and Run Your Own Docker Instance

Once you've installed the packages you need using `venv` and `pip`, and have Docker installed as well, you can run the app locally on port 8080 by entering the following commands in the project root directory:

```bash
sudo docker build -t versadm .
sudo docker run -it --rm --name versadm -p 8080:8080 versadm
```

When your Docker instance starts and runs, you'll see some status `[INFO]` messages appear in the terminal. Leave this terminal window open so you can shut down the Docker instance with `Ctrl-C` when you're done. Don't do that now, or you'll miss all the fun!

Once you've run the `docker build` command (above), you won't need to run it again unless you update the code. You just need to use the `docker run` command to start the Docker instance -- but it doesn't hurt to rebuild your Docker instance with the `docker build` command, either.

Note that you can skip `sudo` when running these commands in PowerShell on Windows 10.

Once you've got your Docker instance up and running, open your favorite browser to consume the API endpoints you specify. For example, paste this URL in your browser's address bar: `http://localhost:8080/parties`

You won't see much until you add some data to the API, but you will get a response if the Docker instances is running. Read on to learn how to add sample election data to the API.

## Populate and test the API with curl

There are a number of API testing GUIs, such as [Swagger](https://swagger.io/) or [Postman](https://www.postman.com/), you could use to test the VersaDM API -- although these tools may have licensing or pricing restrictions that don't match your requirements.

If you've gotten this far, you know how to use the command line, so to test the VersaDM API, you can always use `curl`.

First, you'll want to populate the API with some test data. You can use the sample `jetsons.json` data file included in this repo. Open a new command prompt or terminal window and go to the directory that contains the `jetsons.json` file. Then enter this command:

```bash
`curl --header "Content-Type: application/json" --header "Accept: application/json" --request PUT --data @jetsons.json http://localhost:8080/admin/load_election_data`
```

If everything is set up correctly, you'll see a response that looks something like this:

```bash
{"errors":null,"data":true,"changeId":"","refId":"6a580c3a-fff9-49e9-b111-72f2587c4365"}
```

Note the critical `"errors":null,"data":true,` part of the response.

Now you can issue GET commands with curl, like this:

```bash
curl http://localhost:8080/parties
```

Or you can enter similar URLs in your favorite browser.

Storage is currently all in-memory, nothing persists after you stop the server. To update the data in memory, use POST, PUT or DELETE commands with `curl` or your favorite API testing too.

To stop the Docker server, go to the terminal where you started Docker and press `Ctrl-C` to shut down the Docker instance.
