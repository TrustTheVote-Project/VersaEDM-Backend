# Versa EDM Backend README

The backend server for the Versa Election Data Manager system, also known as **VersaDM**.

VersaDM is the part of [ElectOS](https://electos.org/) that provides a back-end API to a web UI front-end. VersaDM also validates JSON data using pydantic. Written in Python, distributed in Docker.

## More Information about VersaDM

* The VersaDM software is licensed under the [OSET Public License v2](LICENSE.md)
* Read the [NIST Special Publication 1500-100, Election Results Common Data Format Specification (Revision 2.0: PDF, 11.3MB)](docs/NIST.SP.1500-100r2.pdf) for a detailed description of the election data model this software implements, or check it out on GitHub: [usnistgov/ElectionResultsReporting at version2](https://github.com/usnistgov/ElectionResultsReporting/tree/version2). VersaBE conforms to this specification.
* Check the `docs` folder in this repo for more helpful documentation and other useful information about this project and the data specification it implements.

## Getting Started

To run the code in this repo, you need Python 3.9 or greater installed correctly on your development workstation.

### Using Poetry

We use [Poetry for Python dependency management and packaging](https://python-poetry.org/) for continuous development and integration work. If you're interested in working with the code in this repo, follow the instructions to [install poetry on your development workstation](https://python-poetry.org/docs/#installation).

Then, you can [set up your development environment using the poetry.lock file](https://python-poetry.org/docs/basic-usage/#installing-with-poetrylock). This consists of entering the following command in the project root directory:

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

Once pip is installed, create your virtual environment.

### Set up venv

This Python repo uses the built-in virtual environment, `venv`. To set up `venv`, **go to the project root directory** and enter:

```bash
python -m venv ./venv
```

This command works on Windows, Mac and Linux (although you may need to substitute `python3` for your platform, or use the backslash for Windows).

This project's `.gitignore` file already includes a line to ignore the entire `./venv/` directory, which is an excellent reason to use it as your virtual environment directory name.

Depending on your platform, you'll need to activate your virtual environment after it's created. Note that some code editors and IDEs, like VSCode, will start the virtual environment automatically if you point to the Python interpreter in in your `venv` directory.

Generally, it's best to use only one type of virtual environment at a time, even though this repo supports multiple Python packaging tools.

### Windows 10 with PowerShell

In the repo root directory, enter these commands in PowerShell:

```bash
cd .\venv\Scripts\
.\Activate.ps1
```

### Linux or Mac with bash

Activate your venv with this bash command entered at the root of the project folder:

```bash
source ./venv/bin/activate 
```

### Linux or Mac with fish

If you're using fish as your shell, you can activate venv like this:

```fish
set VIRTUAL_ENV "/home/neil/repos/oset/VersaEDM-Backend/venv"
```

### Installing required packages

Once venv is active, your command line should display `(venv)` before the prompt. Then, use pip to install the required Python packages:

```bash
pip install -r requirements.txt
```

Or, you can install the development requirements, which will also install the basic requirements.

```bash
pip install -r requirements-dev.txt
```

Either command will ensure you've installed the correct versions of each package.

## Setup: Docker

You'll also need to install docker.

### Installing Docker in Windows 10

We recommend using [chocolately](https://chocolatey.org/) to install the current version of the Docker Desktop package.

### Installing Docker in Linux

Install the latest docker using snap:

```bash
sudo snap install docker
```

### Build and Run Your Own Docker Instance

Once you've installed the packages you need using venv, and have docker installed as well, you can run the app locally on port 8080 using the following Bash commands from the project root:

```bash
sudo docker build -t versadm .
sudo docker run -it --rm --name versadm -p 8080:8080 versadm
```

Note that you can skip `sudo` when running these commands in PowerShell on Windows 10.

## Test the API

Then you can run the browser app to consume the API endpoints defined in it.

To test the API, you can use curl:

```bash
curl http://localhost:8080/party
curl http://localhost:8080/parties
```

Storage is all in-memory at this point, nothing persists after you stop the server.  For now, you'll need to call POST methods to put data in before getting data out.
