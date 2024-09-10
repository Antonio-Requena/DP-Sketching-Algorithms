# $\varepsilon$-DP Sketching Algorithims
The current technological landscape requires the continuous collection of information from a large number of users. This is essential for developing personalized products and services, improving operational efficiency, and gaining competitive advantages in the market. However, the ongoing collection of information about a large number of users poses significant challenges in terms of privacy and security. Users are increasingly aware of the risks associated with exposing their personal data and are demanding higher levels of protection. At the same time, cybercrime is constantly growing, with increasingly sophisticated attacks compromising the integrity and security of data. For these reasons, leading technology companies are investing in research focused on developing techniques to obtain efficient analytics from massive datasets, while preserving user privacy and security. 

In this context, $\varepsilon$-differential privacy methods allow for statistical analysis on datasets without revealing specific information about individuals. Their combination with probabilistic data structures, especially data sketches, provides the capability to store information from massive data streams in a compact manner. This repository contains the source code for my Bachelor's Degree Final Project, which focuses on the implementation of algorithms that combine $\varepsilon$-differential privacy and sketching techniques. These algorithms ensure information privacy while using probabilistic data structures to obtain estimated analytics in terms of frequency over various datasets in CSV format.

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

```powershell
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
python algorithm_name.py
```

## Repository Structure :seedling:

The repository is organized into five main directories, each containing the corresponding Python implementation of an algorithm and the experimental results obtained from the experiments described in the final degree project (PDF). Below is a detailed breakdown of the repository structure:
```
.
├── Private Count Mean Sketch/
│   ├── private_cms.py                  # Python file containing the implementation of the "Private Count Mean Sketch" algorithm.
│   └── Experimental results/
│       └── results_*.csv               # CSV files with experimental results for this algorithm.
├── Private Hadamard Count Mean Sketch/
│   ├── private_Hcms.py                 # Python file containing the implementation of the "Private Hadamard Count Mean Sketch" algorithm.
│   └── Experimental results/
│       └── results_*.csv               # CSV files with experimental results for this algorithm.
├── RAPPOR/
│   ├── rappor.py                       # Python file containing the implementation of the "RAPPOR" algorithm.
|   ├── bloomfilter.py                  # Python file containing functions used in the "RAPPOR" algorithm.
│   └── Experimental results/
│       └── results_*.csv               # CSV files with experimental results for this algorithm.
├── Sequence Fragment Puzzle/
│   ├── private_sfp.py                  # Python file containing the implementation of the "Sequence Fragment Puzzle" algorithm.
│   └── Experimental results/
│       └── results_*.csv               # CSV files with experimental results for this algorithm.
├── dBitFlip/
│   ├── dbitflip.py                     # Python file containing the implementation of the "dBitFlip" algorithm.
│   └── Experimental results/
│       └── results_*.csv               # CSV files with experimental results for this algorithm.
├── utils/
│   ├── utils.py                        # Contains utility functions used across the algorithms (e.g., data I/O, graphical result displays).
│   ├── generar_csv_distrib.py          # Script to generate synthetic datasets for numeric distribution experiments.
│   ├── generar_csv_puzzle.py           # Script to generate datasets for the "Sequence Fragment Puzzle" algorithm.
│   └── datasets/
│       └── *.csv                       # Directory with all datasets used in the experiments. Users can add their own datasets here.
├── .gitignore                          # Specifies files and directories to ignore in Git version control.
├── README.md                           # This file, explaining the repository structure and usage.
├── TFG_Document.pdf                    # The final degree project document in PDF format.
└── requirements.txt                    # Lists Python dependencies needed to set up a virtual environment.

```

To execute any of the algorithms, navigate to the corresponding folder of the desired algorithm and follow the instructions provided in the [Available Algorithms](#available-algorithms) section.

For example:
```bash
cd Private Count Mean Sketch/
python3 -u private_cms.py -k 16 -m 1024 -e 0.5 -d norm_distrib_60000
```

### Custom Datasets :page_facing_up:

If you wish to use a custom dataset for the experiments, simply add it to the `utils/datasets/` directory. Ensure that the dataset has the same structure as the existing ones (i.e., the same columns), as described in the final degree project document [TFG_AntonioRequena](./TFG_AntonioRequena.pdf).


## Available Algorithms

This repository contains implementations of several algorithms, each designed for specific tasks. Below is a list of the available algorithms:

1. **Private Count Mean Sketch**
2. **Private Hadmard Count Mean Sketch**
3. **Randomized Aggregatable Privacy-Preserving Ordinal Response (RAPPOR)**
4. **d-Bit Flip**
5. **Sequence Fragment Puzzle**

### How to Run the Algorithms

Each algorithm in this repository can be executed via the command line. The following sections provide detailed instructions on how to run each algorithm, including the necessary parameters and examples.

For a better understanding of the parameters, their possible values, and detailed explanations of each algorithm, it is recommended to refer to the corresponding PDF document of the final degree project. The document provides detailed pseudocode for each algorithm and shows the results of algorithm executions with different parameter values.

---

### **Private Count Mean Sketch** & **Private Hadmard Count Mean Sketch** 

The **Private Count Mean Sketch** algorithm estimates frequencies from a known domain using $\varepsilon$-differential privacy. The **Private Hadmard Count Mean Sketch** algorithm for frequency estimation from a known domain while reducing bandwidth using $\varepsilon$-differential privacy. This section explains how to run both algorithms from the command line, including the required parameters.


##### Required Parameters

- **`-k` (`int`)**: Number of hash functions used (equivalent to the number of rows in the sketch matrix).
- **`-m` (`int`)**: Maximum value of the hash function domain (equivalent to the number of columns in the sketch matrix).
- **`-e` (`float`)**: Epsilon ($\varepsilon$) value for $\varepsilon$-differential privacy.
- **`-d` (`str`)**: Name of the dataset used. The dataset should be available in the `utils/datasets` directory.
- **`--verbose_time` (optional)**: Use this flag if you want to print the execution time of the functions.

##### How to Run 👨🏻‍💻 

For **Mac/Linux**:
```bash
python3 -u private_cms.py -k {`k`} -m {`m`} -e {`e`} -d {`DATASET`} --verbose_time
```
```bash
python3 -u private_hcms.py -k {`k`} -m {`m`} -e {`e`} -d {`DATASET`} --verbose_time
```
For **Windows**:
```powershell
python private_cms.py -k {`k`} -m {`m`} -e {`e`} -d {`DATASET`} --verbose_time
```
```powershell
python private_hcms.py -k {`k`} -m {`m`} -e {`e`} -d {`DATASET`} --verbose_time
```

Replace the placeholders `{`k`}`, `{`m`}`, `{`e`}`, and `{`DATASET`}` with the actual values you intend to use:
- `{`k`}`: The **number of hash functions** (e.g., 16).
- `{`m`}`: The **maximum value of the hash function domain** (e.g., 1024).
- `{`e`}`: The **epsilon value** (e.g., 0.5).
- `{`DATASET`}`: The **name of the dataset** (without the extension **.csv**) (e.g., `norm_distrib_60000`).

##### Example

Here’s an example of how to run the algorithm with specific values:

For **Mac/Linux**:
```bash
python3 -u private_cms.py -k 16 -m 1024 -e 0.5 -d norm_distrib_60000 --verbose_time
```
```bash
python3 -u private_hcms.py -k 16 -m 1024 -e 0.5 -d norm_distrib_60000 --verbose_time
```

For **Windows**:
```powershell
python private_cms.py -k 16 -m 1024 -e 0.5 -d norm_distrib_60000 --verbose_time
```
```powershell
python private_hcms.py -k 16 -m 1024 -e 0.5 -d norm_distrib_60000 --verbose_time
```

---

### **Randomized Aggregatable Privacy-Preserving Ordinal Response (RAPPOR)**
The **RAPPOR** algorithm estimates frequencies from a set of candidates using randomized response techniques. This section explains how to run the algorithm from the command line, including the required parameters.

##### Required Parameters

- **`-k` (`int`)**: The **number of bits** in the Bloom filters (e.g., 16).
- **`-h` (`int`)**: The **number of hash functions** used (e.g., 4).
- **`-f` (`float`)**: The **permanent perturbation probability** (e.g., 0.25).
- **`-p` (`float`)**: The **temporary perturbation probability for bits set to 0** (e.g., 0.4).
- **`-q` (`float`)**: The **temporary perturbation probability for bits set to 1** (e.g., 0.6).
- **`-d` (`str`)**: The name of the dataset used. The dataset should be available in the `utils/datasets` directory.
- **`--verbose_time` (optional)**: Use this flag if you want to print the execution time of the functions.

##### How to Run 👨🏻‍💻 

For **Mac/Linux**:
```bash
python3 -u rappor.py -k {`k`} -h {`h`} -f {`f`} -p {`p`} -q {`q`} -d {`DATASET`} --verbose_time
```

For **Windows**:
```powershell
python rappor.py -k {`k`} -h {`h`} -f {`f`} -p {`p`} -q {`q`} -d {`DATASET`} --verbose_time
```

Replace the placeholders `{`k`}`, `{`h`}`, `{`f`}`, `{`p`}`, `{`q`}`, and `{`DATASET`}` with the actual values you intend to use:
- `{`k`}`: The **number of bits** in the Bloom filters (e.g., 16).
- `{`h`}`: The **number of hash functions** used (e.g., 4).
- `{`f`}`: The **permanent perturbation probability** (e.g., 0.25).
- `{`p`}`: The **temporary perturbation probability for bits set to 0** (e.g., 0.4).
- `{`q`}`: The **temporary perturbation probability for bits set to 1** (e.g., 0.6).
- `{`DATASET`}`: The **name of the dataset** (without the extension **.csv**) (e.g., `norm_distrib_60000`).

##### Example

Here’s an example of how to run the algorithm with specific values:

For **Mac/Linux**:
```bash
python3 -u rappor.py -k 16 -h 4 -f 0.25 -p 0.4 -q 0.6 -d norm_distrib_60000 --verbose_time
```

For **Windows**:
```powershell
python rappor.py -k 16 -h 4 -f 0.25 -p 0.4 -q 0.6 -d norm_distrib_60000 --verbose_time
```

---

### **d-Bit Flip**
The **dbitFlip** algorithm estimates frequencies from a known domain. This section explains how to run the algorithm from the command line, including the required parameters.

##### Required Parameters

- **`-d` (`int`)**: The **number of elements** from the domain sent by clients.
- **`-e` (`float`)**: Epsilon ($\varepsilon$) value for $\varepsilon$-differential privacy.
- **`-D` (`str`)**: The name of the dataset used. The dataset should be available in the `utils/datasets` directory. (Used **-D** because **-d** is in use for the number of elements).
- **`--verbose_time` (optional)**: Use this flag if you want to print the execution time of the functions.

##### How to Run 👨🏻‍💻 

For **Mac/Linux**:
```bash
python3 -u dbitflip.py -d {`d`} -e {`e`} -D {`DATASET`} --verbose_time
```

For **Windows**:
```powershell
python dbitflip.py -d {`d`} -e {`e`} -D {`DATASET`} --verbose_time
```

Replace the placeholders `{`d`}`, `{`e`}`, and `{`DATASET`}` with the actual values you intend to use:

- `{`d`}`: The **number of elements** in the domain sent by clients (e.g., 2).
- `{`e`}`: The **epsilon value** (e.g., 0.5).
- `{`DATASET`}`: The **name of the dataset** (without the extension **.csv**) (e.g., `norm_distrib_60000`).

### Example

Here’s an example of how to run the algorithm with specific values:

For **Mac/Linux**:
```bash
python3 -u dbitflip.py -d 2 -e 0.5 -D norm_distrib_60000 --verbose_time
```

For **Windows**:
```powershell
python dbitflip.py -d 1 -e 2 -D norm_distrib_60000 --verbose_time
```

---

### **Sequence Fragment Puzzle** Algorithm**

The **Sequence Fragment Puzzle** algorithm estimates frequencies from an unknown dictionary. This section explains how to run the algorithm from the command line, including the required parameters.

### Required Parameters

- **`-e` (`int`)**: Epsilon ($\varepsilon$) value for $\varepsilon$-differential privacy.
- **`-e2` (`int`)**: Epsilon prime ($\varepsilon'$) value for $\varepsilon$-differential privacy.
- **`-k` (`int`)**: The number of rows in the sketch matrix for the sequence.
- **`-k2` (`int`)**: The number of rows in the sketch matrix for the fragments.
- **`-m` (`int`)**: The number of columns in the sketch matrix for the sequence.
- **`-m2` (`int`)**: The number of columns in the sketch matrix for the fragments.
- **`-T` (`int`)**: Threshold that upper bounds the number of estimated sequences to generate.
- **`-d` (`str`)**: The name of the dataset used (e.g., `my_dataset.csv`).
- **`--verbose_time` (optional)**: Use this flag if you want to print the execution time of the functions.

##### How to Run 👨🏻‍💻 

For **Mac/Linux**:
```bash
python3 -u private_sfp.py -e {`e`} -e2 {`e2`} -k {`k`} -k2 {`k2`} -m {`m`} -m2 {`m2`} -T {`T`} -d {`DV`} --verbose_time
```

For **Windows**:
```cmd
python -u private_sfp.py -e {`e`} -e2 {`e2`} -k {`k`} -k2 {`k2`} -m {`m`} -m2 {`m2`} -T {`T`} -d {`DV`} --verbose_time
```

Replace the placeholders `{`e`}`, `{`e2`}`, `{`k`}`, `{`k2`}`, `{`m`}`, `{`m2`}`, `{`T`}`, and `{`DV`}` with the actual values you intend to use:

- `{`e`}`: The **epsilon value** (e.g., 2).
- `{`e2`}`: The **epsilon prime value** (e.g., 6).
- `{`k`}`: The **number of rows in the sketch matrix for the sequence** (e.g., 64).
- `{`k2`}`: The **number of rows in the sketch matrix for the fragments** (e.g., 32).
- `{`m`}`: The **number of columns in the sketch matrix for the sequence** (e.g., 1024).
- `{`m2`}`: The **number of columns in the sketch matrix for the fragments** (e.g., 512).
- `{`T`}`: The **threshold for the number of estimated sequences** (e.g., 15).
- `{`DV`}`: The **name of the dataset** (e.g., `anglicismo_1M`).

### Example

Here’s an example of how to run the algorithm with specific values:

For **Mac/Linux**:
```bash
python3 -u private_sfp.py -e 2 -e2 6 -k 64 -k2 32 -m 1024 -m2 512 -T 15 -d anglicismo_1M --verbose_time
```

For **Windows**:
```powershell
python private_sfp.py -e 2 -e2 6 -k 64 -k2 32 -m 1024 -m2 512 -T 15 -d anglicismo_1M --verbose_time
```
