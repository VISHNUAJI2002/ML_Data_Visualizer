import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import io
import base64

def create_regression_plot(data, x_column, y_column, save_path=None):
    """Create a regression plot with line of best fit"""
    try:
        # Create figure
        plt.figure(figsize=(10, 6))
        
        # Convert columns to numeric, coercing errors to NaN
        x_data = pd.to_numeric(data[x_column], errors='coerce')
        y_data = pd.to_numeric(data[y_column], errors='coerce')
        
        # Remove rows where either x or y is NaN
        mask = ~(x_data.isna() | y_data.isna())
        x_clean = x_data[mask]
        y_clean = y_data[mask]
        
        if len(x_clean) == 0:
            raise ValueError(f"No valid numeric data found in columns {x_column} and {y_column}")
        
        # Create scatter plot
        plt.scatter(x_clean, y_clean, alpha=0.6, color='blue', label='Data points')
        
        if len(x_clean) > 1:  # Need at least 2 points for regression
            # Fit linear regression
            X = x_clean.values.reshape(-1, 1)
            y = y_clean.values
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Create regression line
            x_range = np.linspace(x_clean.min(), x_clean.max(), 100)
            y_pred = model.predict(x_range.reshape(-1, 1))
            
            r_squared = model.score(X, y)
            plt.plot(x_range, y_pred, color='red', linewidth=2, 
                    label=f'Regression line (R² = {r_squared:.3f})')
        
        plt.title(f'Regression Plot: {y_column} vs {x_column}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save to file if path provided
        if save_path:
            plt.savefig(save_path, format='png' if save_path.endswith('.png') else 'pdf', 
                       dpi=300, bbox_inches='tight')
        
        # Convert plot to base64 string
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=150, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return plot_url
        
    except Exception as e:
        print(f"Error creating regression plot: {e}")
        return None