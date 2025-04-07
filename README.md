# MLOPS_pipeline

Building pipeline:
1) Create a GitHub repo and clone it to local machine (Add experiments)
2) Add src folder along with all components(run them invidually)
3) Add data, models, reports directories to .gitignore file
4) Now git add, commit, push














Logging crash course:
- logging is an inbuilt module
- you make a logging object called a logger
- you then define a handler for this logger. You also specify which sort of a handler you want: console handler to see the informations printed on the terminal or file handler which creates a file with the logs. 
- then you also define a formatter. Formatter helps you define how you want the logs to be viewed in. For example: DD_TT_"message"_success is lets say one format. Its basically a sort of string formatting.
- Once you define the handler and the formatter you add it in the logger object. 
- logging levels:
debug, info, warning, error, critical 
- logger level when set, lets say you set it at error level, then you can log only errors and critical problems only. so you wont be able to see least sensitive problems
