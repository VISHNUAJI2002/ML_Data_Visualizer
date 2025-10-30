import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import os

def create_scatter_plot(data, x_column, y_column, save_path=None):
    """Create a scatter plot"""
    try:
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
        
        plt.scatter(x_clean, y_clean, alpha=0.7, color='blue')
        plt.title(f'Scatter Plot: {y_column} vs {x_column}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.grid(True, alpha=0.3)
        
        # Save to file if path provided
        if save_path:
            plt.savefig(save_path, format='png' if save_path.endswith('.png') else 'pdf', 
                       dpi=300, bbox_inches='tight')
        
        # Convert plot to base64 string for web display
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=150, bbox_inches='tight')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return plot_url
        
    except Exception as e:
        print(f"Error creating scatter plot: {e}")
        return None