#!/usr/bin/env python3
"""
Jupyter Notebook Organization Hook for Claude Code
Automatically organizes and validates notebook structure for data science workflows.
"""
import json
import sys
import os
from datetime import datetime

def organize_notebook_metadata(notebook):
    """Add metadata and structure to notebook."""
    # Ensure proper metadata
    if 'metadata' not in notebook:
        notebook['metadata'] = {}

    # Add data science specific metadata
    notebook['metadata'].update({
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'name': 'python',
            'version': '3.8+'
        },
        'data_science_template': {
            'created': datetime.now().isoformat(),
            'template_version': '1.0',
            'analysis_type': 'exploratory'
        }
    })

    return notebook

def add_header_cell(notebook):
    """Add a header cell if missing."""
    cells = notebook.get('cells', [])

    # Check if first cell is already a markdown header
    if cells and cells[0]['cell_type'] == 'markdown':
        first_cell_source = ''.join(cells[0].get('source', []))
        if first_cell_source.startswith('#'):
            return notebook  # Header already exists

    # Create header cell
    header_cell = {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [
            '# Data Analysis Notebook\n',
            '\n',
            '**Author:** [Your Name]\n',
            f'**Date:** {datetime.now().strftime("%Y-%m-%d")}\n',
            '**Objective:** [Describe the analysis objective]\n',
            '\n',
            '## Summary\n',
            '\n',
            '[Brief summary of findings and key insights]\n',
            '\n',
            '---\n'
        ]
    }

    # Insert at beginning
    cells.insert(0, header_cell)
    notebook['cells'] = cells
    return notebook

def add_imports_cell(notebook):
    """Add standard imports cell if missing."""
    cells = notebook.get('cells', [])

    # Look for existing imports
    has_imports = False
    for cell in cells[:3]:  # Check first 3 cells
        if cell['cell_type'] == 'code':
            source = ''.join(cell.get('source', []))
            if 'import pandas' in source or 'import numpy' in source:
                has_imports = True
                break

    if has_imports:
        return notebook

    # Find position to insert imports (after header)
    insert_pos = 1 if cells and cells[0]['cell_type'] == 'markdown' else 0

    imports_cell = {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [
            '# Standard library imports\n',
            'import pandas as pd\n',
            'import numpy as np\n',
            'import matplotlib.pyplot as plt\n',
            'import seaborn as sns\n',
            '\n',
            '# Configure visualization defaults\n',
            'plt.style.use(\'seaborn-v0_8\')\n',
            'sns.set_palette("husl")\n',
            'plt.rcParams[\'figure.figsize\'] = (12, 8)\n',
            '\n',
            '# Display options\n',
            'pd.set_option(\'display.max_columns\', None)\n',
            'pd.set_option(\'display.max_rows\', 100)\n',
            '\n',
            '# Suppress warnings\n',
            'import warnings\n',
            'warnings.filterwarnings(\'ignore\')\n'
        ]
    }

    cells.insert(insert_pos, imports_cell)
    notebook['cells'] = cells
    return notebook

def add_section_templates(notebook):
    """Add section template cells if notebook is minimal."""
    cells = notebook.get('cells', [])

    # Only add templates if notebook has fewer than 5 cells
    if len(cells) >= 5:
        return notebook

    section_cells = [
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 1. Data Loading and Overview\n',
                '\n',
                'Load and examine the dataset structure, shape, and basic information.\n'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'metadata': {},
            'outputs': [],
            'source': [
                '# Load data\n',
                '# df = pd.read_csv(\'data.csv\')\n',
                '\n',
                '# Basic information\n',
                '# print(f"Dataset shape: {df.shape}")\n',
                '# print(f"Memory usage: {df.memory_usage().sum() / 1024**2:.2f} MB")\n',
                '# df.info()\n'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 2. Exploratory Data Analysis\n',
                '\n',
                'Examine data distributions, missing values, and initial patterns.\n'
            ]
        },
        {
            'cell_type': 'code',
            'execution_count': None,
            'metadata': {},
            'outputs': [],
            'source': [
                '# Check for missing values\n',
                '# missing_data = df.isnull().sum()\n',
                '# print("Missing values:")\n',
                '# print(missing_data[missing_data > 0])\n',
                '\n',
                '# Basic statistics\n',
                '# df.describe()\n'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 3. Data Visualization\n',
                '\n',
                'Create visualizations to understand patterns and relationships.\n'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 4. Analysis and Insights\n',
                '\n',
                'Detailed analysis and key findings.\n'
            ]
        },
        {
            'cell_type': 'markdown',
            'metadata': {},
            'source': [
                '## 5. Conclusions and Next Steps\n',
                '\n',
                'Summary of findings and recommendations for further analysis.\n'
            ]
        }
    ]

    # Add section templates at the end
    cells.extend(section_cells)
    notebook['cells'] = cells
    return notebook

def main():
    """Main notebook organization function."""
    try:
        # Read input from Claude Code
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', '')

        # Only process Jupyter notebooks
        if not file_path.endswith('.ipynb'):
            sys.exit(0)

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                notebook = json.load(f)

            # Organize notebook
            original_cells = len(notebook.get('cells', []))

            notebook = organize_notebook_metadata(notebook)
            notebook = add_header_cell(notebook)
            notebook = add_imports_cell(notebook)
            notebook = add_section_templates(notebook)

            # Write back if changes were made
            new_cells = len(notebook.get('cells', []))
            if new_cells > original_cells:
                with open(file_path, 'w') as f:
                    json.dump(notebook, f, indent=2)

                print(f"📊 Organized notebook structure: {os.path.basename(file_path)}")
                print(f"   • Added {new_cells - original_cells} template cells")
                print(f"   • Enhanced metadata and imports")
            else:
                print(f"✓ Notebook {os.path.basename(file_path)} already well-organized")

    except Exception as e:
        print(f"Error organizing notebook: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()