# CSCI461 — Assignment 1: Dockerized SMS Spam Analysis

**Course:** Introduction to Big Data — Fall 2026  
**Dataset:** [UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection)  
**Team:** Hana Nasser and Maya Mohamed

Each record in the dataset is one SMS message labeled `ham` (non-spam) or `spam`.

## 1. Prerequisites and dataset setup (on the host)

You need Docker Desktop running in Linux containers mode, internet access to retrieve the UCI dataset (if it is not already included), and several GB of free disk space. Host Python is optional: the download script can run in a temporary Python container.

From the `bd-a1` project directory, with Python installed:

```powershell
python download_dataset.py
```

**Windows PowerShell without Python installed:**

```powershell
docker run --rm -v "${PWD}:/work" -w /work python:3.11-slim sh -c "pip install pandas && python download_dataset.py"
```

Confirm that `data/dataset.csv` exists **before** building the image. If downloading fails, obtain the original SMS Spam Collection from UCI and convert the tab-separated `SMSSpamCollection` file into `data/dataset.csv` with the columns `label,text`. Do not substitute synthetic data. A source dataset is included in the submitted project ZIP if its redistribution is permitted.

## 2. Build the Docker image

In a PowerShell terminal, from `bd-a1`:

```powershell
docker build -t bd-a1:latest .
docker images
```

The Dockerfile uses `quay.io/jupyter/scipy-notebook:latest` as its base image, installs additional dependencies from `requirements.txt`, copies the dataset and notebook, and sets the project working directory inside the image.

## 3. Run JupyterLab with persistent output

From `bd-a1` in **Windows PowerShell**:

```powershell
docker run --rm --name bd-a1-jupyter -p 8888:8888 -v "${PWD}/output:/home/jovyan/bd-a1/output" bd-a1:latest
```

Then open http://localhost:8888/lab?token=assignment1 , navigate to `notebook/analysis.ipynb`, and select **Kernel → Restart Kernel and Run All Cells**. The complete analysis and both ML tasks must execute inside the container, not just on the host.

For Bash (Linux/macOS), replace the volume argument with:

```bash
-v "$(pwd)/output:/home/jovyan/bd-a1/output"
```

If host port 8888 is occupied, map another host port, for example `-p 8890:8888`, then open `http://localhost:8890/lab?token=assignment1`.

**Image vs. container:** A Docker image is the packaged, reusable template composed of layers. A container is a running or stopped instance created from that image. The mapping `-p 8888:8888` means `HOST_PORT:CONTAINER_PORT`; the host's port 8888 forwards to port 8888 inside the container. The `-v` option creates a **bind mount** from a chosen host directory to the container, preserving generated outputs on the host even after removing the container. A Docker-managed volume stores data in a location managed by Docker rather than the explicit host path.

## 4. Data analysis and machine learning

The notebook covers:

1. Dataset understanding: `head`, shape, columns, data types, `info`, and descriptive statistics.
2. Missing-value and duplicate checks, cleaning decisions, and before/after row counts.
3. Conditional `loc`, positional `iloc`, including an `iloc[np.r_[...]]` selection.
4. At least three data transformations or derived features.
5. Simple random, stratified, and illustrative cluster sampling using text-length bands; comparison of category distributions.
6. Numerical text features and correlation matrix/heatmap; an explanation that correlation is not causation.
7. Original text retained and a separate `cleaned_text` column, tokenization, word frequencies, top-word chart, ham/spam comparison, and written insights.
8. TF-IDF text classification with Logistic Regression and Multinomial Naive Bayes, including a train/test split, accuracy, precision, recall, F1-score, and confusion matrix.
9. Unsupervised TF-IDF clustering with MiniBatchKMeans (`k=2`), cluster counts, quality measure, representative terms, and a comparison against known labels.
10. Saving and verifying all required artifacts.

**Interpretation cautions:** The length-band groups used for cluster sampling are proxy groups rather than native source-defined clusters. K-Means cluster numbers are not the actual class labels. The historic English SMS data and text preprocessing choices limit generalization to newer messages or other languages.

## 5. Required output files

After successfully running the notebook, the host's `output/` directory should contain:

```text
output/
├── cleaned_data.csv
├── model_metrics.txt
├── cluster_summary.txt
└── figures/
    ├── 01_correlation_heatmap.png
    ├── 02_top_words.png
    ├── 03_group_comparison.png
    └── 04_confusion_matrix.png
```

These files were observed in the host output directory following the local run. To inspect them in PowerShell:

```powershell
dir .\output
dir .\output\figures
Get-Content .\output\model_metrics.txt
Get-Content .\output\cluster_summary.txt
```

## 6. Container lifecycle evidence

While `bd-a1-jupyter` is running, execute these commands in a **second host terminal** and capture real screenshots:

```powershell
docker images
docker ps
docker ps -a
docker logs bd-a1-jupyter
docker inspect bd-a1-jupyter
```

Note: `--rm` deletes the stopped container. To show a *stopped* example in `docker ps -a`, optionally run a separate evidence container without `--rm`:

```powershell
docker run -d --name bd-a1-evidence -p 8890:8888 bd-a1:latest
docker stop bd-a1-evidence
docker ps -a
```

Use actual screenshots in `screenshots/`, including the Docker build, image listing, running container, and Jupyter execution. Screenshots must reflect real completed actions.

## 7. Docker Hub distribution

**Published repository:** [`hnasser2320/bd-a1`](https://hub.docker.com/r/hnasser2320/bd-a1)  
**Published tag:** `latest`  
**Push digest (October 30, 2026):** `sha256:7b1bf7f360e81ff6aa0cec66b648eb55aa6a2ea24527f1496c3201d609e0eff2`

Commands used to publish:

```powershell
docker login
docker tag bd-a1:latest hnasser2320/bd-a1:latest
docker push hnasser2320/bd-a1:latest
```

### Independent verification on another team member's Windows computer

With Docker Desktop running, open PowerShell and execute:

```powershell
docker pull hnasser2320/bd-a1:latest
mkdir bd-a1-verification
cd bd-a1-verification
mkdir output
docker run --rm --name bd-a1-test -p 8889:8888 -v "${PWD}/output:/home/jovyan/bd-a1/output" hnasser2320/bd-a1:latest
```

Open http://localhost:8889/lab?token=assignment1 , select `notebook/analysis.ipynb`, and run **Kernel → Restart Kernel and Run All Cells**. From a second PowerShell terminal, run `docker ps`, and inspect the generated results in `C:\Users\User\bd-a1-verification\output` (assuming that was the chosen project directory). Save screenshots of the pull, running container, notebook results, and host output files.

**Observed verification:** Maya Mohamed ran the published image in JupyterLab on another computer and generated output files, including the four figures, under the bind-mounted Windows output directory. The screenshots should be kept as evidence in the submission.

## 8. Team members

- Hana Nasser
- Maya Mohamed

**Team-size note:** The assignment handout specifies teams of 3–4. This project currently lists two members; confirm that a two-person team is accepted by the instructor or teaching assistant.

## 9. Final submission checklist

- [x] Approved UCI dataset downloaded as `data/dataset.csv` before building the image.
- [x] Custom Docker image built successfully.
- [x] Notebook executed successfully inside Docker, generating the output files and four figures.
- [x] Docker image pushed to `hnasser2320/bd-a1:latest`.
- [x] Another team member ran the published image and verified output generation.
- [x] All original screenshots copied into the project's `screenshots/` directory.
- [ ] Confirm instructor approval for a two-person team if required.
- [ ] Final ZIP created from the **entire `bd-a1/` folder** and inspected for all required files.

**Verification status (October 30, 2026):** Local Docker build, notebook execution, result generation, Docker Hub push, and independent team-member execution were reported and supported by terminal results or screenshots. Team screenshots have been collected in the project submission folder. The final ZIP still needs to be created and checked.
## GitHub Repository

https://github.com/hana20nasser/SMS-Spam-Detection