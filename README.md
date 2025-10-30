# ML Data Visualizer

## Overview
The ML Data Visualizer is a Python application designed to facilitate the visualization of machine learning datasets. Users can upload their datasets, select target and feature columns, and choose from various visualization types, including scatter plots, regression plots, heatmaps, and decision trees.

## Features
- Load datasets in various formats (CSV, Excel, etc.)
- Select target and feature columns for analysis
- Generate different types of visualizations:
  - Scatter Plot
  - Regression Plot
  - Heatmap
  - Decision Tree

## Project Structure
```
ml-data-visualizer
├── src
│   ├── app.py                # Main entry point of the application
│   ├── models
│   │   └── __init__.py       # Initializes the models package
│   ├── visualizations
│   │   ├── __init__.py       # Initializes the visualizations package
│   │   ├── scatter_plot.py    # Function to create scatter plots
│   │   ├── regression_plot.py  # Function to create regression plots
│   │   ├── heatmap.py         # Function to create heatmaps
│   │   └── decision_tree.py    # Function to visualize decision trees
│   ├── data_processing
│   │   ├── __init__.py       # Initializes the data processing package
│   │   └── dataset_handler.py  # Class to handle dataset loading and processing
│   └── utils
│       ├── __init__.py       # Initializes the utils package
│       └── helpers.py         # Helper functions for data processing and visualization
├── requirements.txt           # Project dependencies
├── config.py                  # Configuration settings
└── README.md                  # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ml-data-visualizer.git
   ```
2. Navigate to the project directory:
   ```
   cd ml-data-visualizer
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```
   python src/app.py
   ```
2. Follow the prompts to upload your dataset and select the desired features and target columns.
3. Choose the type of visualization you wish to generate.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.