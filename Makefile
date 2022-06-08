EXAMPLE_PATH=data/

model-image:
	docker build -f dockerfiles/Dockerfile.run -t final-project .

create_db:
	docker run -it --env SQLALCHEMY_DATABASE_URI final-project create_db

delete_car_info:
	docker run -it --env SQLALCHEMY_DATABASE_URI final-project delete

download_from_s3:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY final-project download_file_from_s3 --local_path=data/bmw2.csv --s3_path=s3://2022-msia423-zhou-yihan/raw/bmw.csv

upload_to_s3:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY final-project upload_file_to_s3 --local_path=data/raw/bmw.csv --s3_path=s3://2022-msia423-zhou-yihan/raw/bmw.csv

data/raw/bmw2.csv: config/config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run_model_pipeline acquire --config=config/config.yaml --output 'data/raw/bmw2.csv'
raw: data/raw/bmw2.csv

data/raw/input_data.csv: data/bmw2.csv config/config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run_model_pipeline prepare_feature --input 'data/raw/bmw2.csv' --config=config/config.yaml --output 'data/raw/input_data.csv'
features: data/raw/input_data.csv

data/raw/X_test.csv data/rwa/X_train.csv data/raw/y_test.pkl data/raw/y_train.pkl: data/raw/input_data.csv config/config.yaml
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run_model_pipeline split --input 'data/raw/input_data.csv' --config=config/config.yaml --output 'data/raw/X_train.csv' 'data/raw/X_test.csv' 'data/raw/y_train.pkl' 'data/raw/y_test.pkl'
split: data/raw/X_test.csv data/raw/X_train.csv data/raw/y_test.pkl data/raw/y_train.pkl

data/raw/rf.sav: data/raw/X_test.csv data/raw/y_test.pkl
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run_model_pipeline train --input 'data/raw/X_train.csv' 'data/raw/y_train.pkl' --config=config/config.yaml --output 'data/raw/rf.sav'
train: data/raw/rf.sav

data/result/ypred.npy: data/raw/rf.sav data/raw/y_test.pkl
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run_model_pipeline score --input 'data/raw/rf.sav' 'data/raw/X_test.csv' --config=config/config.yaml --output 'data/result/ypred.npy'
score: data/result/ypred.npy

data/result/result.csv: data/raw/y_test.pkl data/result/ypred.npy
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ final-project run_model_pipeline evaluate --input 'data/raw/y_test.pkl' 'data/result/ypred.npy' --output 'data/result/result.csv'
evaluate: data/result/result.csv

test-image:
	docker build -f dockerfiles/Dockerfile.test -t  final-project-test .

unit-test:
	docker run final-project-test

app-image:
	docker build -f dockerfiles/Dockerfile.app -t final-project-app .

runapp:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ -e SQLALCHEMY_DATABASE_URI -p 5000:5000 final-project-app

cleanraw:
	rm data/raw/*

cleanresult:
	rm data/result/*

all: download_from_s3 raw features split train score evaluate

get_clean: download_from_s3 raw

trainall: split train












