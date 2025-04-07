import os
import logging
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import yaml

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger = logging.getLogger("feature_engineering")
logger.setLevel("DEBUG")

console_handler = logging.StreamHandler()
console_handler.setLevel("DEBUG")

log_file_path = os.path.join(log_dir, "feature_engineering.log")
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel("DEBUG")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)



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


def load_data(file_path: str) -> pd.DataFrame:
    """Load the preprocessed csv file"""
    try:
        df = pd.read_csv(file_path)
        df.fillna('', inplace=True)
        logger.debug("Data loaded and NaN values filled %s", file_path)
        return df
    except pd.errors.ParserError as e:
        logger.error("Failed to parse the csv file: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error occurred during file loading %s", e)
        raise
    
def apply_tfidf(train_data: pd.DataFrame, test_data: pd.DataFrame, max_features: int, text_column:str, target_column:str) -> tuple:
    """Apply tf-idf to the data"""
    try:
        vectorizer = TfidfVectorizer(max_features=max_features)
        
        X_train = train_data[text_column].values
        y_train = train_data[target_column].values
        X_test = test_data[text_column].values
        y_test = test_data[target_column].values
        
        X_train_vect = vectorizer.fit_transform(X_train)
        X_test_vect = vectorizer.transform(X_test)
        
        train_df = pd.DataFrame(X_train_vect.toarray())
        train_df["label"] = y_train
        
        test_df =pd.DataFrame(X_test_vect.toarray())
        test_df["label"] = y_test
        
        logger.debug("tf-idf vectorization performed on both train and test data")
        return train_df, test_df
    except Exception as e:
        logger.error("Error occurred during tf-idf vectorization of text feature: %s", e)
        raise
    
def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Save the processed dataframe as a csv file"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        logger.debug("Data saved to %s", file_path)
    except Exception as e:
        logger.error("Unexpected error ocurred while saving the data: %s", e)
        raise
        
    
def main():
    try:
        params = load_params(param_path="params.yaml")
        max_features = params["feature_engineering"]["max_features"]
        
        train_data = load_data("./data/interim/train_preprocessed.csv")
        test_data = load_data("./data/interim/test_preprocessed.csv")
        
        train_df, test_df = apply_tfidf(
            train_data=train_data,
            test_data=test_data,
            max_features=max_features,
            text_column="text",
            target_column="target"
        )
        
        save_data(df=train_df, file_path=os.path.join("./data", "processed", "train_tfidf.csv"))
        save_data(df=test_df, file_path=os.path.join("./data", "processed", "test_tfidf.csv"))
        
    except Exception as e:
        logger.error("Failed to complete the feature engineering process: %s", e)
        print(f"Error: {e}")
        
if __name__=='__main__':
    main()