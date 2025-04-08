# 🧪 MLOps Pipeline using DVC & Git

This project is a structured MLOps pipeline template that integrates **Git**, **DVC**, **AWS S3**, **experimentation tracking**, and **parameterization**. The goal is to modularize ML workflows, track experiments, version datasets/models, and enable reproducibility and collaboration.

---

## 🧱 Project Structure & Setup

### Step 1: Initialize Git Repository

```bash
git init
```

- Create a GitHub repository and clone it locally.
- This allows version control of your source code and infrastructure (e.g., `dvc.yaml`, scripts).
- Commit an initial project structure with:

```bash
.
├── src/              # All Python code and modular components
├── data/             # Raw and processed data (ignored in Git)
├── models/           # Trained models (ignored in Git)
├── reports/          # Visualizations, evaluation metrics (ignored in Git)
├── .gitignore        # Exclude bulky/untracked files from Git
```

- Add `data/`, `models/`, and `reports/` to your `.gitignore`.

Then:
```bash
git add .
git commit -m "Initial commit with pipeline structure"
git push origin main
```

---

## 📦 Set up DVC for pipeline automation

### Step 2: Initialize DVC

```bash
dvc init
```

- This sets up `.dvc/` config directory and tracks data/model versioning.
- Add your pipeline stages using `dvc.yaml`.

### Step 3: Define Your Pipeline Stages

Manually create a `dvc.yaml` file or use `dvc stage add`. Each stage might look like:

```yaml
stages:
  data_ingestion:
    cmd: python src/data_ingestion.py
    deps:
      - src/data_ingestion.py
    outs:
      - data/raw.csv
```

Repeat similarly for preprocessing, feature engineering, model training, etc.

### Step 4: Run and Test Pipeline

```bash
dvc repro
dvc dag  # Visualize your pipeline graphically
```

Then:

```bash
git add dvc.yaml dvc.lock
git commit -m "Add DVC pipeline stages"
git push
```

---

## 📌 Parameterize the Pipeline with `params.yaml`

To control parameters dynamically (e.g., train-test split, model hyperparameters):

### Step 5: Add `params.yaml`

```yaml
train:
  test_size: 0.2
  random_state: 42
model:
  n_estimators: 100
  max_depth: 10
```

### Step 6: Load Parameters in Code

Create a helper function like:

```python
import yaml
import logging

logger = logging.getLogger(__name__)

def load_params(param_path: str) -> dict:
    try:
        with open(param_path, "r") as f:
            params = yaml.safe_load(f)
        logger.debug("Parameters retrieved from %s", param_path)
        return params
    except FileNotFoundError:
        logger.error("File not found: %s", param_path)
        raise
```

Use `load_params("params.yaml")` inside your `main()` function or relevant script.

### Step 7: Re-run Pipeline with Parameters

```bash
dvc repro
```

Changes in `params.yaml` will now automatically trigger reruns only of affected stages.

Then:

```bash
git add .
git commit -m "Add parameterized pipeline"
git push
```

---

## 📊 Run and Track Experiments with DVCLive

### Step 8: Install DVCLive

```bash
pip install dvclive
```

### Step 9: Add Live Logging to Your Scripts

In `model_training.py`:

```python
from dvclive import Live

with Live(save_dvc_exp=True) as live:
    live.log_metric("accuracy", acc)
    live.log_metric("precision", prec)
    live.log_metric("recall", rec)
    live.log_params(params)
```

This creates a `dvclive/` directory that tracks metrics over time.

### Step 10: Run and View Experiments

```bash
dvc exp run
dvc exp show  # View experiment results in CLI table
```

You can manage experiments using:

```bash
dvc exp apply <exp-name>     # Apply specific experiment
dvc exp remove <exp-name>    # Remove specific experiment
```

---

## ☁️ Add Remote Storage with AWS S3

### Step 11: AWS Setup

- Go to the [AWS IAM Console](https://console.aws.amazon.com/iam/)
- Create a user with **programmatic access**.
- Attach a policy (e.g., `AmazonS3FullAccess`)
- Note down **Access Key** and **Secret Key**

### Step 12: Configure AWS CLI

```bash
pip install awscli
aws configure
```

Input your access/secret keys and region.

### Step 13: Install DVC S3 Plugin

```bash
pip install "dvc[s3]"
```

### Step 14: Add S3 Remote for DVC

```bash
dvc remote add -d dvcstore s3://your-bucket-name
dvc remote modify dvcstore endpointurl https://s3.amazonaws.com
```

### Step 15: Push Artifacts to Cloud

```bash
dvc push  # Push datasets/models tracked by DVC
git add .dvc/config
git commit -m "Add S3 remote"
git push
```

---


## 🧾 Logging Crash Course

Logging is a built-in Python module used to capture runtime information about your code, which helps with debugging, monitoring, and understanding what happened and when.

- ✅ **Logger**: A central object that you'll use to log messages. You create one using `logging.getLogger(__name__)`.
  
- 🧱 **Handlers**: Decide *where* your logs will go:
  - **StreamHandler**: Sends logs to the terminal/console.
  - **FileHandler**: Saves logs to a file (like `pipeline.log`), useful for persistent tracking.

- 🎨 **Formatters**: Define *how* your logs look:
  - You can format logs to show time, log level, filename, message, etc.
  - Example: `%(asctime)s - %(levelname)s - %(message)s` ➝ `2025-04-08 10:00:00 - INFO - Model training started`

- 🚦 **Log Levels**: Specify the severity of the message:
  - `DEBUG`: Detailed diagnostic information, useful for development.
  - `INFO`: General runtime events (e.g., "model training started").
  - `WARNING`: Something unexpected happened but the program can still run.
  - `ERROR`: A serious problem; something failed.
  - `CRITICAL`: A fatal error that will stop execution.

- ⚙️ **Set Log Level**: You can control what gets printed/logged:
  - If you set `logger.setLevel(logging.WARNING)`, only warnings and above will be shown.

> 💡 Tip: Use logging instead of `print()` in production code. It’s more flexible, scalable, and professional.

---


## 📄 YAML Crash Course

YAML (YAML Ain’t Markup Language) is a simple and human-readable way to store structured data. It's used extensively for configurations (e.g., `params.yaml`, `dvc.yaml`).

- 📘 **Syntax**:
  - Based on **key-value pairs**.
  - Hierarchies are defined using **indentation** (2 spaces recommended).
  - Comments start with `#`.

- ✨ **Key Features**:
  - Easier to read and write than JSON.
  - Supports strings, integers, lists, and nested dictionaries.
  - No commas or braces required.

- 📁 **Used in DVC**:
  - `params.yaml` holds hyperparameters and configuration settings that can be used across different scripts.
  - `dvc.yaml` defines pipeline stages, commands, dependencies, and outputs for automation and reproducibility.

- 🔍 **Example**:
  ```yaml
  train:
    test_size: 0.2
    random_state: 42
  model:
    max_depth: 5
    learning_rate: 0.01
  ```

- 🔄 **Used in Code**:
  - You can load YAML data in Python using `yaml.safe_load()` and use it just like a Python dictionary.

> 💡 Tip: YAML is more readable than JSON, but remember — **indentation matters!** Always use consistent spacing.


---

## ✅ Summary of Commands

```bash
git init
dvc init
dvc repro
dvc dag
dvc exp run
dvc exp show
dvc push
aws configure
```

---


