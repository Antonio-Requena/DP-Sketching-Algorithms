# DP-Sketching-Algorithims
This repository contains several Python scripts that require specific dependencies to run correctly. Follow the instructions below to set up the environment.

## Prerequisites

Make sure you have Python 3.6 or higher installed on your machine. You will also need `pip`, which usually comes with Python.

## Setup Instructions (Virtual Enviorment)

### 1. Clone the repository

First, clone this repository to your local machine using the following command:

```bash
git clone https://github.com/Antonio-Requena/DP-Sketching-Algorithms
cd DP-Sketching-Algorithms
```

### 2. Create and activate a virtual environment

It’s recommended to use a virtual environment to install dependencies in an isolated environment. This prevents conflicts with other Python installations on your system.

On Windows:

```bash
python -m venv env
.\env\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install the dependencies

With the virtual environment activated, install the necessary dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Run the algorithms

Once the dependencies are installed, you can run any of the Python algoritmhs in the repository without any issues:

```bash
python your_script_name.py
```

### 5. Deactivate the virtual environment (optional)

When you’re done working on the project, you can deactivate the virtual environment with the following command:

```bash
deactivate
```

On Windows, you can either close the terminal or use:

```bash
.\env\Scripts\deactivate
```
