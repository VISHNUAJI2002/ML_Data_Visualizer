from flask import Flask, request, render_template, flash, redirect, url_for, session, send_file
import pandas as pd
import os
import uuid
from data_processing.dataset_handler import DatasetHandler
from visualizations.scatter_plot import create_scatter_plot
from visualizations.regression_plot import create_regression_plot
from visualizations.heatmap import create_heatmap
from visualizations.decision_tree import create_decision_tree

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'
app.secret_key = 'your-secret-key-here'  # Add secret key for flash messages
dataset_handler = DatasetHandler()

# Create directories if they don't exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('downloads', exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file selected", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    
    if file and file.filename.endswith('.csv'):
        try:
            # Save the uploaded file
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Load data to get columns
            data = dataset_handler.load_data(filepath)
            
            if data is None:
                return "Error loading CSV file. Please check the file format.", 400
            
            return render_template('select_columns.html', 
                                 columns=data.columns.tolist(), 
                                 filepath=filepath)
        except Exception as e:
            return f"Error processing file: {str(e)}", 500
    
    return "Please upload a valid CSV file", 400

@app.route('/visualize', methods=['POST'])
def visualize():
    selected_columns = request.form.getlist('columns')
    target_column = request.form.get('target')
    chart_type = request.form['chart_type']
    filepath = request.form.get('filepath')
    
    if not filepath:
        return "File path missing", 400
    
    # Load data from the saved file
    data = dataset_handler.load_data(filepath)
    
    if data is None:
        return "Error loading data file", 400
    
    # Store visualization parameters in session for downloads
    session['viz_params'] = {
        'selected_columns': selected_columns,
        'target_column': target_column,
        'chart_type': chart_type,
        'filepath': filepath
    }
    
    try:
        plot = None
        
        if chart_type == 'scatter' and len(selected_columns) >= 2:
            numeric_cols = data.select_dtypes(include=['number']).columns
            selected_numeric = [col for col in selected_columns[:2] if col in numeric_cols]
            
            if len(selected_numeric) >= 2:
                plot = create_scatter_plot(data, selected_numeric[0], selected_numeric[1])
            else:
                return "Scatter plot requires 2 numeric columns", 400
                
        elif chart_type == 'regression' and len(selected_columns) >= 2:
            numeric_cols = data.select_dtypes(include=['number']).columns
            selected_numeric = [col for col in selected_columns[:2] if col in numeric_cols]
            
            if len(selected_numeric) >= 2:
                plot = create_regression_plot(data, selected_numeric[0], selected_numeric[1])
            else:
                return "Regression plot requires 2 numeric columns", 400
                
        elif chart_type == 'heatmap':
            plot = create_heatmap(data)
            
        elif chart_type == 'decision_tree' and target_column:
            plot = create_decision_tree(data, target_column)
        else:
            return "Invalid chart type or insufficient/incorrect columns selected", 400
        
        if plot:
            return render_template('visualization.html', plot=plot)
        else:
            return "Error generating visualization", 500
            
    except Exception as e:
        return f"Error generating visualization: {str(e)}", 500

@app.route('/download/<format>')
def download_plot(format):
    """Download the current visualization as PNG or PDF"""
    if 'viz_params' not in session:
        return "No visualization to download", 400
    
    params = session['viz_params']
    data = dataset_handler.load_data(params['filepath'])
    
    if data is None:
        return "Error loading data", 400
    
    # Generate unique filename
    unique_id = str(uuid.uuid4())[:8]
    filename = f"{params['chart_type']}_{unique_id}.{format}"
    file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    
    try:
        # Generate plot and save to file
        if params['chart_type'] == 'scatter':
            numeric_cols = data.select_dtypes(include=['number']).columns
            selected_numeric = [col for col in params['selected_columns'][:2] if col in numeric_cols]
            create_scatter_plot(data, selected_numeric[0], selected_numeric[1], save_path=file_path)
            
        elif params['chart_type'] == 'regression':
            numeric_cols = data.select_dtypes(include=['number']).columns
            selected_numeric = [col for col in params['selected_columns'][:2] if col in numeric_cols]
            create_regression_plot(data, selected_numeric[0], selected_numeric[1], save_path=file_path)
            
        elif params['chart_type'] == 'heatmap':
            create_heatmap(data, save_path=file_path)
            
        elif params['chart_type'] == 'decision_tree':
            create_decision_tree(data, params['target_column'], save_path=file_path)
        
        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return f"Error generating download: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)