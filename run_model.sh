
python3 run_model.py acquire --config=config/config.yaml --output 'data/raw/bmw2.csv'

python3 run_model.py prepare_feature --input 'data/raw/bmw2.csv' --config=config/config.yaml --output 'data/raw/input_data.csv'

python3 run_model.py split --input 'data/raw/input_data.csv' --config=config/config.yaml --output 'data/raw/X_train.csv' 'data/raw/X_test.csv' 'data/raw/y_train.pkl' 'data/raw/y_test.pkl'

python3 run_model.py train --input 'data/raw/X_train.csv' 'data/raw/y_train.pkl' --config=config/config.yaml --output 'data/result/rf.sav'

python3 run_model.py score --input 'data/raw/rf.sav' 'data/raw/X_test.csv' --config=config/config.yaml --output 'data/result/ypred.npy'

python3 run_model.py evaluate --input 'data/raw/y_test.pkl' 'data/result/ypred.npy' --output 'data/result/result.csv'
