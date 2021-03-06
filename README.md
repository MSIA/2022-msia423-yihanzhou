# Used Car Price Prediction
Author: Yihan Zhou

# Table of Contents
* [Project Charter ](#Project-Charter)
  * [1. Vision](#1.Vision)
  * [2. Mission](Mission)
  * [3. Success criteria](Success-criteria)
* [Directory structure ](#Directory-structure)
* [Running the app ](#Running-the-app)
    * [1. Initialize the database ](#1.-Initialize-the-database)
    * [2. Running the Pipeline](#2.-Running-the-Pipeline)
    * [3. Configure Flask app ](#3.-Configure-Flask-app)
    * [4. Run the Flask app ](#4.-Run-the-Flask-app)
* [Testing](#Testing)
* [Clean](#Clean-the-data-directory)



## Project Charter

### Vision
Cars serve as an important tool for our foreign students to study in a new country, 
it can make our life more convenient. Although the price of a brand-new car 
is predetermined by the manufacturers and the price will not fluctuate too much 
across countries, the international students tend to purchase a used car instead 
since those used cars have a fairly low price. So it is economic-wise to buy 
a used car for daily life through years of college. Nevertheless, it is hard for students 
to know what a fair price of a used car is based on different conditions of the cars. 
There are lots of factors that affect the price of a used car, for example 
the mileage, the type of fuel, the age of the car, and so on so forth. I am a 
big fan of BMW and I also bought a used BMW car in my college. My friends who studied 
in the UK always complain about the expensive price of transportation in the UK and the used car market
in the UK is hot nowadays. Therefore, I hope this app can help both the buyers and sellers 
estimate the price of a used BMW car. 


### Mission

The project uses the dataset from Kaggle -- 100,000 UK Used Car Data set.
The link to the dataset is [here](https://www.kaggle.com/datasets/adityadesai13/used-car-dataset-ford-and-mercedes). 
The app only used the subset of records for the BMW cars and the dataset 
contains 10781 records with 9 features. The regression methods will then be employed on the data to evaluate the 
price of a used BMW car.

When using this app, it will firstly ask for the following attributes of the car 
from the users: 
- model
- year
- transmission type
- mileage
- fuelType
- mpg
- engine size 

Then, under the supervised learning models used, the app will predict the potential price 
of a certain car for the user. On the buyers' side, the dynamic nature of this app 
is to help them to select the best value when purchasing a used BMW car 
in the UK market. On the side of a dealer, this app will help sellers to set a 
reasonable car price, which would make their sales more attractive to buyers.


### Success criteria

#### Machine Learning Metrics:

The application will be using supervised learning algorithms and the **Random
Forest Classifier/ Linear Regression Model** are good choices. The metrics that will be used to evaluate the 
performance of the classifiers will be R Squared and Mean Squared Error, and a good 
model is intended to generate a higher R Squared and lower MSE by the nature of
regression analysis.

#### Business Metrics:
From a business standpoint, the successful deployment of this app will
help both the sellers and buyers to evaluate the value of a used BMW car, which
in turn to help the buyers to save money and the sellers attract more customers.
So, it is a good way to quantify the apps in several ways:
- The daily active users 
- User engagement level (average time spent)
- Total transactions made
- Sellers' acceptance rate













## Directory structure 

```
????????? README.md                         <- You are here
????????? api
???   ????????? static/                       <- CSS, JS files that remain static
???   ????????? templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs???    
???
????????? config                            <- Directory for configuration files 
???   ????????? local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
???   ????????? logging/                      <- Configuration of python loggers
???   ????????? flaskconfig.py                <- Configurations for Flask API 
???
????????? data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
???   ????????? external/                     <- External data sources, usually reference data,  will be synced with git
???   ????????? sample/                       <- Sample data used for code development and testing, will be synced with git
???
????????? deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
???
????????? docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project.
|
????????? dockerfiles/                      <- Directory for all project-related Dockerfiles 
???   ????????? Dockerfile.app                <- Dockerfile for building image to run web app
???   ????????? Dockerfile.run                <- Dockerfile for building image to execute run.py  
???   ????????? Dockerfile.test               <- Dockerfile for building image to run unit tests
???
????????? figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
???
????????? models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
???
????????? notebooks/
???   ????????? archive/                      <- Develop notebooks no longer being used.
???   ????????? deliver/                      <- Notebooks shared with others / in final state
???   ????????? develop/                      <- Current notebooks being used in development.
???   ????????? template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
???
????????? reference/                        <- Any reference material relevant to the project
???
????????? src/                              <- Source data for the project. No executable Python files should live in this folder.  
???
????????? test/                             <- Files necessary for running model tests (see documentation below) 
???
????????? app.py                            <- Flask wrapper for running the web app 
????????? run.py                            <- Simplifies the execution of one or more of the src scripts  
????????? requirements.txt                  <- Python package dependencies 
```


## Running the app 

Before running the app, pay attention to set the following environment variables:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- SQLALCHEMY_DATABASE_URI

### 1. Initialize the database
#### Build the image 

To build the image, run from this directory (the root of the repo): 

```bash
make model-image
```

#### Upload the data to your S3bucket

The following will upload the file **data/raw/bmw.csv** to your S3bucket, 
assuming that you have environment variables, AWS_ACCESS_KEY_ID and 
AWS_SECRET_ACCESS_KEY, set in your environment:

```bash
make upload_to_s3
```

#### Download the dataset from S3 bucket

The following will download the file, data/raw/bmw.csv from my S3 bucket to data/bmw2.csv, 
assuming you have your environment variables, **AWS_ACCESS_KEY_ID** and **AWS_SECRET_ACCESS_KEY** 
set in your environment:

```bash
make download_from_s3
```

#### Create the database in RDS or local SQLite

```bash
make create_db 
```

#### Ingest data to the database
- Trying an example below:

```bash
docker run --mount type=bind,source="$(pwd)",target=/app/ -e SQLALCHEMY_DATABASE_URI final-project  ingest --model='5 Series' --year=2018 --transmission='Automatic' --mileage=2100 --fuelType='Diesel' --mpg=20 --engineSize=20
```

#### Delete the car information from the database

```bash
make delete_car_info
```

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`


##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/msia_423.db'
```

### 2. Running the Pipeline
The following steps help you running each individual step of the model pipeline:

##### Acquiring the raw data:
```bash
make raw
```

##### Featuring the raw data for modeling:
```bash
make features
```

##### Splitting the Test and Train data
```bash
make split
```

##### Training the model
```bash
make train
```

##### Scoring the model
```bash
make score
```

##### Evaluating the model performance
```bash
make evaluate
```

**You can also use the following command to execute the entire model pipeline**

```bash
make all
```

### 3. Configure Flask app 

`config/flaskconfig.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
HOST = "0.0.0.0" # the host that is running the app. 0.0.0.0 when running locally 
PORT = 5000  # What port to expose app on. Must be the same as the port exposed in dockerfiles/Dockerfile.app 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/tracks.db'  # URI (engine string) for database that contains tracks
APP_NAME = "bmw_price_estimator"
SQLALCHEMY_TRACK_MODIFICATIONS = True 
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
MAX_ROWS_SHOW = 100 # Limits the number of rows returned from the database 
```

### 4. Run the Flask app 

#### Build the image 

To build the image, run from this directory (the root of the repo): 

```bash
make app-image
```

This command builds the Docker image, with the tag `final-project-app`, based on the instructions in `dockerfiles/Dockerfile.app` and the files existing in this directory.

#### Running the app

To run the Flask app, run: 

```bash
make runapp
```

The arguments in the above command do the following: 

* The `--name test-app` argument names the container "test". This name can be used to kill the container once finished with it.
* The `--mount` argument allows the app to access your local `data/` folder so it can read from the SQLlite database created in the prior section. 
* The `-p 5000:5000` argument maps your computer's local port 5000 to the Docker container's port 5000 so that you can view the app in your browser. If your port 5000 is already being used for someone, you can use `-p 5001:5000` (or another value in place of 5001) which maps the Docker container's port 5000 to your local port 5001.

Note: If `PORT` in `config/flaskconfig.py` is changed, this port should be changed accordingly (as should the `EXPOSE 5000` line in `dockerfiles/Dockerfile.app`)


#### Kill the container 

Once finished with the app, you will need to kill the container. If you named the container, you can execute the following: 

```bash
docker kill test-app 
```
where `test-app` is the name given in the `docker run` command.

If you did not name the container, you can look up its name by running the following:

```bash 
docker container ls
```

The name will be provided in the right most column. 

## Testing

Run the following:

```bash
make test-image
```

To run the tests, run: 

```bash
make unit-test
```

The following command will be executed within the container to run the provided unit tests under `test/`:  

```bash
python -m pytest
``` 

## Clean the data directory
If you want to clean all the data and model generated above, you can use the following code to clean the data/raw folder or data/result folder in my repo
```bash
make cleanraw
```
or
```bash
make cleanresult
```