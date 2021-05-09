# Flask + React Project Template

Project template / boilerplate for a micro-service providing endpoints via Flask (Python) and a frontend via React 
(JavaScript).

**Table of Contents**

1. [Requirements](#requirements)
    1. [Tech Stack](#tech-stack)
2. [Customisation](#customisation)
3. [Installation](#installation)
4. [Running the App](#running-the-app)
    1. [Environment Config](#environment-config)

## Requirements

- Python3.6+
- NodeJS / npm
- HuggingFace

### Tech Stack

**Backend**

- **Flask** framework for hosting API endpoints and delivering the frontend
- **mysql-connector-python** for MySQL access

**Frontend**

- **React** basic framework for the frontend
- **Redux** a global store for the frontend, used for data exchange with the API and to avoid handing down data through
component hierarchies
- **Webpack** and **Babel** to transpile the frontend into a single `index.js`, which gets included by the `index.html`
- **Moment.JS** the standard library for date/time handling in JavaScript
- **S Alert** a basic notification library 
- **ESLint** and **Prettier** for linting Javascript code and auto-format
- Custom **Basic Utilities** and **Style Mixins** (see `frontend/src/util.js` and `frontend/src/mixins.js`)

## Installation

### Install Packages 

First, try to run:

```bash
make install-deps
```

You might have to run it with `sudo`.

That should install the Python (pip) dependencies and Javascript (npm) dependencies.
This assumes, that your Python/Pip binaries are `python3` and `pip3`.

**Manual Installation**

If above doesn't work, install the dependencies separately:

_Javascript:_

```bash
npm install
``` 

_Python:_

```bash
pip install -r requirements.txt
```

### Set Up MySQL

The first thing to do is set up the environment variable files. Create a file called `.env` and 
populate it with the following items: 



The backing database is a MySQL store. To set up the database, you need to 
install mysql. If you are on a mac, you can run: 

`brew install mysql`

After this, you can access the command line as follows: 

`mysql`

Then run the following commands: 

`CREATE DATABASE {database_name}`



## Running the App

If you just want to compile the frontend once and then serve it via the backend (e.g. production mode), simply run:

```bash
npm run build
```

This will produce an index.js containing all the frontend code in the `/static` directory and put the index.html in the 
`/templates` folder. Those 2 directories are used by the Flask app to deliver the frontend components.

The backend's entry point is the script `runner.py` on the root of the project. To run the backend, simply execute:

```bash
make start
```

Again, if your Python binary differs from `python3`, simply run:

```bash
python runner.py
```

(and replace `python` with whatever you use as binary)

- This'll serve the Flask app via: http://localhost:5555

**Frontend Development**

The frontend can be continuously re-compiled whenever you change the code.
In a separate bash window, simply run:

```bash
make frontend
```

Or

```bash
npm run hot-client
```

This will run the `webpack` watcher, which will observe the `/frontend/src` folder for changes and re-compile the 
frontend when changes have occurred. 

In case of compilation errors, this bash window will also tell you what is wrong 
with your code. 

_Do not close this window while you're developing, or you quit the watcher._

### Environment Config

As mentioned before, the Flask app is using an `.env` file to load environment variables which specify database access.
Check the `config.py` for all currently supported environment variables.

You can easily extend this and add getters for additional environment configuration and add those to your `.env` file.
Please provide meaningful defaults for all additional config variables (_except 3rd party service credentials_)
