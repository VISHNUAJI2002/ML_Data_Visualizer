import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

def create_heatmap(data, save_path=None):
    """Create a correlation heatmap"""
    try:
        # Select only numeric columns
        numeric_data = data.select_dtypes(include=['number'])
        
        if numeric_data.empty:
            raise ValueError("No numeric columns found for correlation heatmap")
        
        # Calculate correlation matrix
        correlation_matrix = numeric_data.corr()
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, 
                   annot=True, 
                   cmap='coolwarm', 
                   center=0,
                   square=True,
                   fmt='.2f')
        plt.title('Correlation Heatmap')
        plt.tight_layout()
        
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
        print(f"Error creating heatmap: {e}")
        return None