import pandas as pd

class DatasetHandler:
    def __init__(self):
        self.data = None
        self.feature_columns = None
        self.target_column = None

    def load_data(self, file_path):
        """Load CSV data and return the DataFrame"""
        try:
            self.data = pd.read_csv(file_path)
            return self.data  # This return statement was missing
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def set_feature_columns(self, columns):
        """Set the feature columns for analysis"""
        self.feature_columns = columns

    def set_target_column(self, column):
        """Set the target column for supervised learning"""
        self.target_column = column

    def get_data_info(self):
        """Get basic information about the dataset"""
        if self.data is not None:
            return {
                'shape': self.data.shape,
                'columns': self.data.columns.tolist(),
                'dtypes': self.data.dtypes.to_dict(),
                'missing_values': self.data.isnull().sum().to_dict()
            }
        return None

    def get_numeric_columns(self):
        """Get list of numeric columns"""
        if self.data is not None:
            return self.data.select_dtypes(include=['number']).columns.tolist()
        return []

    def get_categorical_columns(self):
        """Get list of categorical columns"""
        if self.data is not None:
            return self.data.select_dtypes(include=['object']).columns.tolist()
        return []