import pandas as pd
import warnings
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
from sklearn.model_selection import GridSearchCV
import joblib

import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s')


class ProductPredictor:
    def __init__(self, data_file='orders_data.xlsx'):
        self.data_file = data_file
        self.model = None

    def load_data(self):
        try:
            data = pd.read_excel(self.data_file)
            data.dropna(subset=['order_date', 'order_time', 'product'], inplace=True)
            data['order_datetime'] = pd.to_datetime(data['order_date'] + ' ' + data['order_time'])
            data['hour'] = data['order_datetime'].dt.hour
            data['minute'] = data['order_datetime'].dt.minute
            data['second'] = data['order_datetime'].dt.second
            X = data[['hour', 'minute', 'second']]
            y = data['product']
            return X, y
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.data_file} not found.")
        except Exception as e:
            raise ValueError(f"Data loading error: {e}")


    def load_trained_model(self):
        try:
            self.model = joblib.load('random_forest_model.pkl')
        except FileNotFoundError:
            raise ValueError("Trained model not found. Please train the model first.")
    

    def train_model(self, X, y):
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5, 10]
        }
        grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=5, n_jobs=-1)
        grid_search.fit(X, y)
        self.model = grid_search.best_estimator_

        # Save the trained model
        joblib.dump(self.model, 'random_forest_model.pkl')


    def predict_next_hour(self, interval='2T'):
        logging.info("Starting prediction for the next hour")
        try:
            current_datetime = pd.Timestamp.now()
            end_datetime = current_datetime + pd.Timedelta(hours=1)
            prediction_interval = pd.date_range(start=current_datetime, end=end_datetime, freq=interval)

            predictions = []
            for timestamp in prediction_interval:
                hour = timestamp.hour
                minute = timestamp.minute
                second = timestamp.second
                prediction = self.model.predict([[hour, minute, second]])[0]
                predictions.append(prediction)
                logging.info(f"Prediction for {timestamp}: {prediction}")

            logging.info("Prediction completed successfully")
            return predictions
        except Exception as e:
            logging.error(f"Error during prediction: {e}")



    def most_common_prediction(self, predictions):
        most_common_prediction = Counter(predictions).most_common(1)[0][0]
        print(f"\nMost common predicted product: {most_common_prediction}")
        return most_common_prediction