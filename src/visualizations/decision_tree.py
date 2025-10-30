import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import io
import base64

def create_decision_tree(data, target_column):
    """Create a decision tree visualization"""
    try:
        # Prepare the data
        feature_columns = [col for col in data.columns if col != target_column]
        X = data[feature_columns].select_dtypes(include=['number'])
        y = data[target_column]
        
        if X.empty:
            raise ValueError("No numeric features found for decision tree")
        
        # Handle categorical target variable
        if y.dtype == 'object':
            le = LabelEncoder()
            y_encoded = le.fit_transform(y)
            class_names = le.classes_
        else:
            y_encoded = y
            class_names = None
        
        # Create and fit decision tree
        clf = DecisionTreeClassifier(max_depth=3, random_state=42)
        clf.fit(X, y_encoded)
        
        # Create visualization
        plt.figure(figsize=(15, 10))
        plot_tree(clf, 
                 feature_names=X.columns, 
                 class_names=class_names,
                 filled=True, 
                 rounded=True,
                 fontsize=10)
        plt.title(f'Decision Tree for {target_column}')
        
        # Convert plot to base64 string
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=150, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return plot_url
        
    except Exception as e:
        print(f"Error creating decision tree: {e}")
        return None