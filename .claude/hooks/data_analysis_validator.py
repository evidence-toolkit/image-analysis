#!/usr/bin/env python3
"""
Data Analysis Validation Hook for Claude Code
Automatically validates data science code for best practices and common issues.
"""
import json
import sys
import re
import os

def check_pandas_best_practices(code):
    """Check for pandas best practices."""
    issues = []

    # Check for chained operations without assignment
    if re.search(r'\.(?:loc|iloc|query)\[.*\]\.(?:loc|iloc|query)', code):
        issues.append("Consider using .copy() for chained pandas operations to avoid SettingWithCopyWarning")

    # Check for iterrows usage
    if 'iterrows()' in code:
        issues.append("Consider using .apply(), .map(), or vectorized operations instead of iterrows() for better performance")

    # Check for proper memory management
    if re.search(r'pd\.read_csv\(.*\)', code) and 'dtype=' not in code and 'chunksize=' not in code:
        issues.append("Consider specifying dtypes or using chunksize for large CSV files")

    return issues

def check_visualization_standards(code):
    """Check for visualization best practices."""
    issues = []

    # Check for figure size specification
    if 'plt.figure(' in code and 'figsize=' not in code:
        issues.append("Consider specifying figsize for consistent plot dimensions")

    # Check for proper labels
    if any(plot in code for plot in ['plt.plot(', 'plt.scatter(', 'plt.bar(']):
        if not any(label in code for label in ['xlabel(', 'ylabel(', 'title(']):
            issues.append("Consider adding axis labels and title for better plot clarity")

    # Check for seaborn context
    if 'sns.' in code and 'sns.set_style(' not in code and 'sns.set_context(' not in code:
        issues.append("Consider setting seaborn style and context for consistent aesthetics")

    return issues

def check_statistical_practices(code):
    """Check for statistical analysis best practices."""
    issues = []

    # Check for random seed setting
    if any(method in code for method in ['train_test_split', 'RandomForest', 'random_state']):
        if 'random_state=' not in code and 'np.random.seed(' not in code:
            issues.append("Consider setting random_state for reproducible results")

    # Check for proper validation
    if any(model in code for model in ['fit(', 'predict(']):
        if 'train_test_split' not in code and 'cross_val_score' not in code:
            issues.append("Consider using proper train/test split or cross-validation")

    return issues

def check_notebook_structure(file_path):
    """Check Jupyter notebook structure and organization."""
    issues = []

    if not file_path.endswith('.ipynb'):
        return issues

    try:
        with open(file_path, 'r') as f:
            notebook = json.load(f)

        cells = notebook.get('cells', [])
        markdown_cells = [c for c in cells if c['cell_type'] == 'markdown']
        code_cells = [c for c in cells if c['cell_type'] == 'code']

        # Check for documentation
        if len(markdown_cells) < len(code_cells) * 0.2:
            issues.append("Consider adding more markdown documentation cells to explain analysis steps")

        # Check for imports organization
        first_code_cell = next((c for c in cells if c['cell_type'] == 'code'), None)
        if first_code_cell:
            source = ''.join(first_code_cell.get('source', []))
            if not any(imp in source for imp in ['import pandas', 'import numpy']):
                issues.append("Consider organizing imports in the first code cell")

    except Exception as e:
        issues.append(f"Could not analyze notebook structure: {e}")

    return issues

def main():
    """Main validation function."""
    try:
        # Read input from Claude Code
        input_data = json.load(sys.stdin)
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', '')

        # Only analyze relevant files
        if not any(file_path.endswith(ext) for ext in ['.py', '.ipynb']):
            sys.exit(0)

        issues = []

        # Read file content
        if os.path.exists(file_path):
            if file_path.endswith('.ipynb'):
                # Notebook-specific checks
                issues.extend(check_notebook_structure(file_path))

                # Extract code from notebook
                with open(file_path, 'r') as f:
                    notebook = json.load(f)
                code_content = ''
                for cell in notebook.get('cells', []):
                    if cell['cell_type'] == 'code':
                        code_content += ''.join(cell.get('source', []))
            else:
                # Python file
                with open(file_path, 'r') as f:
                    code_content = f.read()

            # Run code analysis
            issues.extend(check_pandas_best_practices(code_content))
            issues.extend(check_visualization_standards(code_content))
            issues.extend(check_statistical_practices(code_content))

            # Output suggestions
            if issues:
                print("📊 Data Science Code Review Suggestions:")
                for i, issue in enumerate(issues, 1):
                    print(f"  {i}. {issue}")
                print(f"\n✓ Analyzed {os.path.basename(file_path)} for data science best practices")
            else:
                print(f"✓ {os.path.basename(file_path)} follows data science best practices")

    except Exception as e:
        print(f"Error in data analysis validation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()