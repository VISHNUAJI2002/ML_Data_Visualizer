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
    selected_columns = request.form.getlist('columns') # These are the features
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
        numeric_cols = data.select_dtypes(include=['number']).columns
        
        if chart_type == 'scatter':
            selected_numeric = [col for col in selected_columns if col in numeric_cols]
            
            if len(selected_numeric) >= 2:
                plot = create_scatter_plot(data, selected_numeric[0], selected_numeric[1])
            else:
                return "Scatter plot requires selecting at least 2 numeric columns", 400
                
        elif chart_type == 'regression':
            selected_numeric = [col for col in selected_columns if col in numeric_cols]
            
            if len(selected_numeric) >= 2:
                plot = create_regression_plot(data, selected_numeric[0], selected_numeric[1])
            else:
                return "Regression plot requires selecting at least 2 numeric columns", 400
                
        elif chart_type == 'heatmap':
            selected_numeric = [col for col in selected_columns if col in numeric_cols]

            if len(selected_numeric) < 2:
                return "Heatmap requires selecting at least 2 numeric columns", 400

            data_for_heatmap = data[selected_numeric]
            plot = create_heatmap(data_for_heatmap) 
                
        elif chart_type == 'decision_tree' and target_column:
            if not selected_columns:
                return "Decision tree requires at least one feature column to be selected", 400

            # **THIS IS THE FIX:**
            # 1. Create a list of all columns needed (features + target)
            columns_for_tree = selected_columns.copy()
            if target_column not in columns_for_tree:
                columns_for_tree.append(target_column)
            
            # 2. Create a new DataFrame with *only* these columns
            data_for_tree = data[columns_for_tree]
            
            # 3. Pass the new, filtered DataFrame to the function.
            #    Now it only has the columns you selected, and we can
            #    use the original 2-argument call.
            plot = create_decision_tree(data_for_tree, target_column)

        elif chart_type == 'decision_tree' and not target_column:
             return "Decision tree requires a target column to be selected", 400
             
        else:
            return "Invalid chart type or insufficient/incorrect columns selected", 400
        
        if plot:
            return render_template('visualization.html', plot=plot)
        else:
            return "Error generating visualization. Check column selections.", 500
            
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

    # Get params from session
    selected_columns = params.get('selected_columns', [])
    target_column = params.get('target_column')
    chart_type = params.get('chart_type')
    
    # Generate unique filename
    unique_id = str(uuid.uuid4())[:8]
    filename = f"{chart_type}_{unique_id}.{format}"
    file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], filename)
    
    try:
        numeric_cols = data.select_dtypes(include=['number']).columns

        if chart_type == 'scatter':
            selected_numeric = [col for col in selected_columns if col in numeric_cols]
            if len(selected_numeric) < 2:
                return "Scatter plot requires selecting at least 2 numeric columns", 400
            create_scatter_plot(data, selected_numeric[0], selected_numeric[1], save_path=file_path)
            
        elif chart_type == 'regression':
            selected_numeric = [col for col in selected_columns if col in numeric_cols]
            if len(selected_numeric) < 2:
                return "Regression plot requires selecting at least 2 numeric columns", 400
            create_regression_plot(data, selected_numeric[0], selected_numeric[1], save_path=file_path)
            
        elif chart_type == 'heatmap':
            selected_numeric = [col for col in selected_columns if col in numeric_cols]
            if len(selected_numeric) < 2:
                return "Heatmap requires selecting at least 2 numeric columns", 400
            
            data_for_heatmap = data[selected_numeric]
            create_heatmap(data_for_heatmap, save_path=file_path) 
            
        elif chart_type == 'decision_tree':
            if not target_column or not selected_columns:
                return "Decision tree requires features and a target", 400
            
            # **THIS IS THE SAME FIX, MIRRORED FOR DOWNLOADS:**
            # 1. Create a list of all columns needed (features + target)
            columns_for_tree = selected_columns.copy()
            if target_column not in columns_for_tree:
                columns_for_tree.append(target_column)
                
            # 2. Create a new DataFrame with *only* these columns
            data_for_tree = data[columns_for_tree]
            
            # 3. Pass the filtered data to the function.
            #    We must assume the 'save_path' argument is the 3rd one.
            create_decision_tree(data_for_tree, target_column, save_path=file_path)
        
        else:
            return "Unknown chart type", 400

        return send_file(file_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return f"Error generating download: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)