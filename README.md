# MLOPS_pipeline

Building pipeline:
1) Create a GitHub repo and clone it to local machine (Add experiments)
2) Add src folder along with all components(run them invidually)
3) Add data, models, reports directories to .gitignore file
4) Now git add, commit, push

Setting up dvc pipeline (without params)
5) Create dvc.yaml file and add stages to it
6) "dvc init" then do "dvc repro" to test the pipeline automation. (check dvc dag)
7) Now git add, commit, push


Setting up dvc pipeline (with params)
8) add params.yaml file
9) add the params setup
----------------------------------------------------------------
params.yaml setup

1. import yaml
2. add the load_params function 

def load_params(param_path: str) -> dict:
    """Load parameters from a YAML file"""
    try: 
        with open(param_path, "r") as f:
            params = yaml.safe_load(f)
        logger.debug("Parameters retrieved from %s", param_path)
        return params
    except FileNotFoundError:
        logger.error("File not found: %s", param_path)
        raise
    except yaml.YAMLError as e:
        logger.error("YAML Error: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise

3. Load the params in the main()

----------------------------------------------------------------
10) Do "dvc repro" again to test the pipeline along with the params
11) Now git add, commit, push



Experiments with DVC:
12) pip install dvclive
13) Add the dvclive code block
----------------------------------------------------------------

dvclive code block:

1) Import dvclive and yaml

from dvclive import Live
import yaml

2) Add the load_params function and initiate "params" var in main()
3) Add code below to main():
with Live(save_dvc_exp=True) as live:
    live.log_metric("accuracy", accuracy_score(y_test, y_pred))
    live.log_metric("precision", precision_score(y_test, y_pred))
    live.log_metric("recall", recall_score(y_test, y_pred))

    live.log_params(params)

----------------------------------------------------------------
14) Do "dvc exp run", it will create a new dvc.yaml(if already not there) and dvclive directory(each run will be considered as an experiment)
15) Do "dvc exp show" on terminal to see the experiments or use extension on VSCode(install dvc extension)
16) Do "dvc exp remove {exp-name}" to remove exp(optional) | "dvc exp apply {exp-name}" to reproduce prev exp
17) Change params, re-run code(produce new experiments)
18) Now git add, commit, push


Adding a remote S3 storage to DVC:
19) Login to AWS console
20) Create an IAM user
21) Create S3 (enter unique name and create)
22) pip install "dvc[s3]"
23) pip install awscli
24) "aws configure" - on terminal
25) dvc remote add -d dvcstore s3://bucketname (Instead of dvcstore, you could have added some other name as well)
26) dvc commit-push the exp outcome that you want to keep
27) Finally git add, commit, push


Logging crash course:
- logging is an inbuilt module
- you make a logging object called a logger
- you then define a handler for this logger. You also specify which sort of a handler you want: console handler to see the informations printed on the terminal or file handler which creates a file with the logs. 
- then you also define a formatter. Formatter helps you define how you want the logs to be viewed in. For example: DD_TT_"message"_success is lets say one format. Its basically a sort of string formatting.
- Once you define the handler and the formatter you add it in the logger object. 
- logging levels:
debug, info, warning, error, critical 
- logger level when set, lets say you set it at error level, then you can log only errors and critical problems only. so you wont be able to see least sensitive problems

YAML Crash Course:
- Its sort of like a dict, but is even easier to read. It uses Key-Value pairs. 
- Has an indentation of 2 spaces. The hierarchy is done through indentation.
- YAML is a superset of JSON
- There are stages in our pipeline, like "data_ingestion", "preprocessing", "feature_engineering", "model_training", "model_evaluation". These will be added stagewise into the yaml file
- Every stage will have the command to run it, the dependencies, might have parameters, and the output file location
- 
