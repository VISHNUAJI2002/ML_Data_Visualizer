def get_feature_columns(data):
    return data.columns.tolist()

def get_target_column(data):
    return data.columns.tolist()

def validate_columns(data, feature_columns, target_column):
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' is not in the dataset.")
    for column in feature_columns:
        if column not in data.columns:
            raise ValueError(f"Feature column '{column}' is not in the dataset.")

def plot_selection_chart(plot_type, *args, **kwargs):
    plot_functions = {
        'scatter': 'scatter_plot.create_scatter_plot',
        'regression': 'regression_plot.create_regression_plot',
        'heatmap': 'heatmap.create_heatmap',
        'decision_tree': 'decision_tree.create_decision_tree'
    }
    
    if plot_type not in plot_functions:
        raise ValueError(f"Plot type '{plot_type}' is not supported.")
    
    module_name, function_name = plot_functions[plot_type].split('.')
    module = __import__(f"visualizations.{module_name}", fromlist=[function_name])
    plot_function = getattr(module, function_name)
    
    return plot_function(*args, **kwargs)