## Versa EDM Backend README

The backend server for VersaEDM, part of the ElectOS Versa Election Data Manager, that provides an API to a web UI front-end. Also validates JSON data using pydantic. Written in Python, distributed in Docker.

## Getting Started

To run the code in this repo, you need Python 3.4 or greater installed correctly on your development workstation, as well as pip.

## Set up venv

This Python repo uses the built-in virtual environment, venv. To set up venv, go to the repo root directory and enter:

```
python -m venv ./venv
```

This command works on Windows, Mac and Linux (although you may need to substitute `python3` for your platform, or use the backslash for Windows).

Depending on your platform, you'll need to activate your virtual environment.

### Windows 10 with PowerShell

In the repo root directory, enter these commands in PowerShell:

```
cd .\venv\Scripts\
.\Activate.ps1
```

### Linux or Mac with bash

Activate your venv with this bash command entered at the root of the project folder:

```
source ./venv/bin/activate 
```

### Linux or Mac with fish

If you're using fish as your shell, you can activate venv like this:

```
set VIRTUAL_ENV "/home/neil/repos/oset/VersaEDM-Backend/venv"
```

### Installing required packages

Once venv is active, your command line should display `(venv)` before the prompt. Then, use pip to install the required Python packages:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
This will ensure you've installed the correct versions of each package.

## Setup: Docker

You'll also need to install docker.

### Installing Docker in Windows 10

We recommend using chocolately to install the most current version of the Docker Desktop package.

### Installing Docker in Linux

Install the latest docker using snap:

```bash
sudo snap install docker
```
### Build and Run Your Own Docker Instance

Once you've installed the packages you need using venv, and have docker installed as well, you can run the app locally on port 8080 using the following Bash commands from the project root:

```bash
sudo docker build -t versa .
sudo docker run -it --rm --name versa-app -p 8080:8080 versa
```

Note that you can skip `sudo` when running these commands in PowerShell on Windows 10.

## Test the API

Then you can run the browser app to consume the API endpoints defined in it. Currently only POST /party and GET /parties are defined. 

To test the API, you can use curl:

```bash
curl http://localhost:8080/party
curl http://localhost:8080/parties
```

Storage is all in-memory at this point, nothing persisted to or read from disk/DB, so for the time being, you'll need to call POST methods to put data in before getting data out.
