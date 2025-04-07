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
