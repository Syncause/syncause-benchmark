<<<<<<< HEAD
# Raceval



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin http://192.168.1.22/kindling/raceval.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](http://192.168.1.22/kindling/raceval/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
=======
# 🕵️ RCAEval: A Benchmark for Root Cause Analysis of Microservice Systems

[![DOI](https://zenodo.org/badge/840137303.svg)](https://doi.org/10.5281/zenodo.13294048)
[![pypi package](https://img.shields.io/pypi/v/RCAEval.svg)](https://pypi.org/project/RCAEval)
[![Downloads](https://static.pepy.tech/personalized-badge/rcaeval?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/rcaeval)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/phamquiluan/RCAEval/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/phamquiluan/RCAEval/tree/main)
[![Build and test](https://github.com/phamquiluan/RCAEval/actions/workflows/build-and-test.yml/badge.svg)](https://github.com/phamquiluan/RCAEval/actions/workflows/build-and-test.yml)
[![Upload Python Package](https://github.com/phamquiluan/RCAEval/actions/workflows/python-publish.yml/badge.svg)](https://github.com/phamquiluan/RCAEval/actions/workflows/python-publish.yml)


RCAEval is an open-source benchmark that offers three datasets (RE1, RE2, RE3) with 735 failure cases, and an evaluation framework for root cause analysis (RCA) in microservice systems. It includes 15 reproducible baselines covering metric-based, trace-based, and multi-source RCA methods.



**_NOTE:_** The [main branch](https://github.com/phamquiluan/RCAEval/tree/main) is now under extensive development. Please refer to [CHANGE LOGS](https://github.com/phamquiluan/RCAEval/blob/main/README.md#change-logs) to find the code for our previous publications.

<p align="center">
<img width=1000 src= "./docs/readme.jpg"/>
</p>

[IEEE/ACM ASE 2024](https://dl.acm.org/doi/abs/10.1145/3691620.3695065)
[ACM WWW 2025](https://dl.acm.org/doi/10.1145/3701716.3715290)

**Table of Contents** 
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [How-to-use](#how-to-use)
    + [Data format](#data-format)
    + [Basic usage example](#basic-usage-example)
  * [Available Datasets](#available-datasets)
  * [Available Baselines](#available-baselines)
  * [Reproducibility](#reproducibility)
    + [RCAEval Benchmark Paper](#rcaeval-benchmark-paper)
    + [For ASE Paper](#for-ase-paper)
  * [Creating New RCA Datasets or Methods](#creating-new-rca-datasets-or-methods)
  * [Licensing](#licensing)
  * [Acknowledgments](#acknowledgments)
  * [Change Logs](#change-logs)
  * [Citation](#citation)
  * [Contact](#contact)

## Prerequisites

We recommend using machines equipped with at least 8 cores, 16GB RAM, and ~50GB available disk space with Ubuntu 22.04 or Ubuntu 20.04, and **Python3.12**.

## Installation

The `default` environment, which is used for most methods, can be easily installed as follows. Detailed installation instructions for all methods are in [SETUP.md](docs/SETUP.md).


Open your terminal and run the following commands

```bash
sudo apt update -y
sudo apt install -y build-essential \
  libxml2 libxml2-dev zlib1g-dev \
  python3-tk graphviz
```

Clone RCAEval from GitHub

```bash
git clone https://github.com/phamquiluan/RCAEval.git && cd RCAEval
```

Create virtual environment with Python 3.12 (refer [SETUP.md](docs/SETUP.md) to see how to install Python3.12 on Linux)

```bash
python3.12 -m venv env
. env/bin/activate
```

Install RCAEval using pip

```bash
pip install -e .[default]
```

Or, install RCAEval from PyPI

```bash
# Install RCAEval from PyPI
pip install RCAEval[default]
```

Test the installation

```bash
python -m pytest tests/test.py::test_basic
```

Expected output after running the above command (it takes less than 1 minute)

```bash 
$ pytest tests/test.py::test_basic
============================== test session starts ===============================
platform linux -- Python 3.12.12, pytest-7.3.1, pluggy-1.0.0
rootdir: /home/ubuntu/RCAEval
plugins: dvc-2.57.3, hydra-core-1.3.2
collected 1 item                                                                 

tests/test.py .                                                            [100%]

=============================== 1 passed in 3.16s ================================
```

## How-to-use

### Data format

The telemetry data must be presented as `pandas.DataFrame`. We require the data to have a column named `time` that stores the timestep. A sample of valid data could be downloaded using the `download_data()` or `download_multi_source_data()` method that we will demonstrate shortly below.

### Basic usage example

A basic example to use BARO, a metric-based RCA baseline, to perform RCA are presented as follows,

```python
# You can put the code here to a file named test.py
from RCAEval.e2e import baro
from RCAEval.utility import download_data, read_data

# download a sample data to data.csv
download_data()

# read data from data.csv
data = read_data("data.csv")
anomaly_detected_timestamp = 1692569339

# perform root cause analysis
root_causes = baro(data, anomaly_detected_timestamp)["ranks"]

# print the top 5 root causes
print("Top 5 root causes:", root_causes[:5])
```

Expected output after running the above code (it takes around 1 minute)

```
$ python test.py
Downloading data.csv..: 100%|████████████████████| 570k/570k [00:00<00:00, 19.8MiB/s]
Top 5 root causes: ['emailservice_mem', 'recommendationservice_mem', 'cartservice_mem', 'checkoutservice_latency', 'cartservice_latency']
```

A tutorial of using Multi-source BARO to diagnose failure using multi-source telemetry data (metrics, logs, and traces) is presented in [docs/multi-source-rca-demo.ipynb](docs/multi-source-rca-demo.ipynb). 

A tutorial of using BARO to diagnose code-level faults is presented in [docs/code-level-rca.ipynb](docs/code-level-rca.ipynb).


## Available Datasets

RCAEval benchmark includes three datasets: RE1, RE2, and RE3, designed to comprehensively support benchmarking RCA in microservice systems. Together, our three datasets feature 735 failure cases collected from three microservice systems (Online Boutique, Sock Shop, and Train Ticket) and including 11 fault types. Each failure case also includes annotated root cause service and root cause indicator (e.g., specific metric or log indicating the root cause). The statistics of the datasets are presented in the Table below.

|   Dataset   |   Systems  |   Fault Types            |   Cases  |   Metrics  |   Logs (millions)  |   Traces (millions)  |
|-------------|------------|--------------------------|----------|------------|--------------------|----------------------|
|   RE1       |   3        |   3 Resource, 2 Network  |   375    |   49-212   |   N/A              |   N/A                |
|   RE2       |   3        |   4 Resource, 2 Network  |   270    |   77-376   |   8.6-26.9         |   39.6-76.7          |
|   RE3       |   3        |   5 Code-level           |   90     |   68-322   |   1.7-2.7          |   4.5-4.7            |

Our datasets and their description are publicly available in Zenodo repository with the following information:
- Dataset DOI: https://doi.org/10.5281/zenodo.14590730
- Dataset URL: [https://zenodo.org/records/14590730](https://zenodo.org/records/14590730)

We also provide utility functions to download our datasets using Python. The downloaded datasets will be available at directory `data`.

```python
from RCAEval.utility import (
    download_re1_dataset,
    download_re2_dataset,
    download_re3_dataset,
)

download_re1_dataset()
download_re2_dataset()
download_re3_dataset()
```
<details>
<summary>Expected output after running the above code (it takes half an hour to download and extract the datasets. )</summary>

```
$ python test.py
Downloading RE1.zip..: 100%|█████████████████████| 390M/390M [01:02<00:00, 6.22MiB/s]
Downloading RE2.zip..: 100%|███████████████████| 4.21G/4.21G [11:23<00:00, 6.17MiB/s]
Downloading RE3.zip..: 100%|█████████████████████| 534M/534M [01:29<00:00, 5.97MiB/s]
```
</details>


## Available Baselines 

RCAEval stores all the RCA methods in the `e2e` module (implemented in `RCAEval.e2e`). There are 16 RCA baselines available: RUN, CausalRCA, CIRCA, RCD, MicroCause, EasyRCA, MSCRED, BARO, 𝜖-Diagnosis, TraceRCA, MicroRank, PDiagnose, Multi-source BARO, Multi-source RCD, Multi-source CIRCA, and SREChat RCA.

### SREChat RCA

**SREChat RCA** is a novel RCA method that differs from traditional approaches:
- **No data required**: Only needs detection time, not time series data
- **Remote API-based**: Fetches root cause reports via remote API calls
- **AI-powered**: Uses DeepSeek LLM to parse reports and extract top 5 root causes

For detailed usage instructions, see [SREChat-RCA使用说明.md](SREChat-RCA使用说明.md) or run the demo:

```python
from RCAEval.e2e import srechat_rca

# Basic usage - only needs detection time
result = srechat_rca(detect_time="2025-09-23T17:20:42+08:00")
print("Top 5 root causes:", result["ranks"])
```

Run the demo script:
```bash
python demo_srechat_rca.py
```

## Reproducibility

### RCAEval Benchmark Paper

We provide a script named `main.py` to assist in reproducing the results from [our RCAEval paper](https://arxiv.org/pdf/2412.17015). This script can be executed using Python with the following syntax: 

```
python main.py [-h] [--dataset DATASET] [--method METHOD]
```

The available options and their descriptions are as follows:

```
options:
  -h, --help            Show this help message and exit
  --dataset DATASET     Choose a dataset. Valid options:
                        [re2-ob, re2-ss, re2-tt, etc.]
  --method METHOD       Choose a method (`causalrca`, `microcause`, `e_diagnosis`, `baro`, `rcd`, `circa`, etc.)
```

For example, in Table 6, BARO achieves Avg@5 of 0.72, 0.99, 1, 0.83, 0.64, and 0.8 for CPU, MEM, DISK, SOCKET, DELAY, LOSS, and AVERAGE on the Train Ticket dataset. To reproduce these results, you can run the following commands:

```bash
python  main.py --method baro --dataset re2-tt
```

The expected output should be exactly as presented in the paper (it takes less than 1 minute to run the code)

```
$ python  main.py --method baro --dataset re2-tt --length 20
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 90/90 [00:45<00:00,  1.98it/s]
--- Evaluation results ---
Avg@5-CPU:   0.72
Avg@5-MEM:   0.99
Avg@5-DISK:  1.0
Avg@5-SOCKET: 0.83
Avg@5-DELAY: 0.63
Avg@5-LOSS:  0.64
---
Avg speed: 0.51
```

We can replace the baro method with other methods (e.g., circa) and substitute re2-tt with other datasets to replicate the corresponding results shown in Table 6. This reproduction process is also integrated into our Continuous Integration (CI) setup. For more details, refer to the [.circleci/config.yml](.circleci/config.yml) file.



### For ASE Paper
We provide a script named `main-ase.py` to assist in reproducing the results from [our ASE paper](https://dl.acm.org/doi/abs/10.1145/3691620.3695065). This script can be executed using Python with the following syntax: 

```
python main-ase.py [-h] [--dataset DATASET] [--method METHOD] [--tdelta TDELTA] [--length LENGTH] [--test] 
```

The available options and their descriptions are as follows:

```
options:
  -h, --help            Show this help message and exit
  --dataset DATASET     Choose a dataset. Valid options:
                        [online-boutique, sock-shop-1, sock-shop-2, train-ticket,
                         circa10, circa50, rcd10, rcd50, causil10, causil50]
  --method METHOD       Choose a method (`pc_pagerank`, `pc_randomwalk`, `fci_pagerank`, `fci_randomwalk`, `granger_pagerank`, `granger_randomwalk`, `lingam_pagerank`, `lingam_randomwalk`, `ntlr_pagerank`, `ntlr_randomwalk`, `causalrca`, `causalai`, `run`, `microcause`, `e_diagnosis`, `baro`, `rcd`, `nsigma`, and `circa`)
  --tdelta TDELTA       Specify $t_delta$ to simulate delay in anomaly detection (e.g.`--tdelta 60`)
  --length LENGTH       Specify the length of the time series (used for RQ4)
  --test                Perform smoke test on certain methods without fully run
```

For example, in Table 5, BARO [ $t_\Delta = 0$ ] achieves Avg@5 of 0.97, 1, 0.91, 0.98, and 0.67 for CPU, MEM, DISK, DELAY, and LOSS fault types on the Online Boutique dataset. To reproduce these results, you can run the following commands:

```bash
python main-ase.py --dataset online-boutique --method baro 
```

The expected output should be exactly as presented in the paper (it takes less than 1 minute to run the code)

```
--- Evaluation results ---
Avg@5-CPU:   0.97
Avg@5-MEM:   1.0
Avg@5-DISK:  0.91
Avg@5-DELAY: 0.98
Avg@5-LOSS:  0.67
---
Avg speed: 0.07
```

As presented in Table 5, BARO [ $t_\Delta = 60$ ] achieves Avg@5 of 0.94, 0.99, 0.87, 0.99, and 0.6 for CPU, MEM, DISK, DELAY, and LOSS fault types on the Online Boutique dataset. To reproduce these results, you can run the following commands:

```bash
python main-ase.py --dataset online-boutique --method baro --tdelta 60
```

The expected output should be exactly as presented in the paper (it takes less than 1 minute to run the code)

```
--- Evaluation results ---
Avg@5-CPU:   0.94
Avg@5-MEM:   0.99
Avg@5-DISK:  0.87
Avg@5-DELAY: 0.99
Avg@5-LOSS:  0.6
---
Avg speed: 0.07
```

We can replace the baro method with other methods (e.g., nsigma, fci_randomwalk) and substitute online-boutique with other datasets to replicate the corresponding results shown in Table 5. This reproduction process is also integrated into our Continuous Integration (CI) setup. For more details, refer to the [.github/workflows/reproducibility.yml](.github/workflows/reproducibility.yml) file.

## Creating New RCA Datasets or Methods

For detailed guidance, refer to [EXTENDING.md](docs/EXTENDING.md).

## Licensing

This repository includes code from various sources with different licenses. We have included their corresponding LICENSE into the [LICENSES](LICENSES) directory:

- **BARO**: Licensed under the [MIT License](LICENSES/LICENSE-BARO). Original source: [BARO GitHub Repository](https://github.com/phamquiluan/baro/blob/main/LICENSE).
- **CausalRCA**: No License. Original source: [CausalRCA GitHub Repository](https://github.com/AXinx/CausalRCA_code).
- **CIRCA**: Licensed under the [BSD 3-Clause License](LICENSES/LICENSE-CIRCA). Original source: [CIRCA GitHub Repository](https://github.com/NetManAIOps/CIRCA/blob/master/LICENSE).
- **E-Diagnosis**: Licensed under the [BSD 3-Clause License](LICENSES/LICENSE-E-Diagnosis). Original source: [PyRCA GitHub Repository](https://github.com/salesforce/PyRCA/blob/main/LICENSE).
- **MicroCause**: Licensed under the [Apache License 2.0](LICENSES/LICENSE-MicroCause). Original source: [MicroCause GitHub Repository](https://github.com/PanYicheng/dycause_rca/blob/main/LICENSE).
- **RCD**: Licensed under the [MIT License](LICENSES/LICENSE-RCD). Original source: [RCD GitHub Repository](https://github.com/azamikram/rcd).
- **RUN**: No License. Original source: [RUN GitHub Repository](https://github.com/zmlin1998/RUN).

**For the code implemented by us and for our datasets, we distribute them under the [MIT LICENSE](LICENSE)**.

## Acknowledgments

We would like to express our sincere gratitude to the researchers and developers who created the baselines used in our study. Their work has been instrumental in making this project possible. We deeply appreciate the time, effort, and expertise that have gone into developing and maintaining these resources. This project would not have been feasible without their contributions.

## Change Logs
- [Mar 2025] The version of RCAEval used in our WWW'25 paper are available in the [www25 branch](https://github.com/phamquiluan/RCAEval/tree/www25).
- [Dec 2024] The prior version of RCAEval used in our ASE'24 paper are available in the [ase24 branch](https://github.com/phamquiluan/RCAEval/tree/ase24).

## Citation


```bibtex
@inproceedings{pham2025rcaeval,
  title={RCAEval: A Benchmark for Root Cause Analysis of Microservice Systems with Telemetry Data},
  author={Pham, Luan and Zhang, Hongyu and Ha, Huong and Salim, Flora and Zhang, Xiuzhen},
  booktitle={Companion Proceedings of the ACM on Web Conference 2025},
  pages={777--780},
  year={2025}
}
```

```bibtex
@inproceedings{pham2024root,
  title={Root Cause Analysis for Microservice System based on Causal Inference: How Far Are We?},
  author={Pham, Luan and Ha, Huong and Zhang, Hongyu},
  booktitle={Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering},
  pages={706--715},
  year={2024}
}
```

```bibtex
@inproceedings{pham2024baro,
  title={BARO: Robust root cause analysis for microservices via multivariate bayesian online change point detection},
  author={Pham, Luan and Ha, Huong and Zhang, Hongyu},
  journal={Proceedings of the ACM on Software Engineering},
  volume={1},
  number={FSE},
  pages={2214--2237},
  year={2024},
}
```

## Contact

[phamquiluan\@gmail.com](mailto:phamquiluan@gmail.com?subject=RCAEval)
>>>>>>> new-main
