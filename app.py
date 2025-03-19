import os
import io
import pandas as pd
import plotly.graph_objects as go
from flask import Flask, request, jsonify, send_from_directory
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.decomposition import PCA
import base64

app = Flask(__name__)

# Serve index.html
@app.route('/')
def serve_index():
    return send_from_directory("static", "index.html")

# Function to handle CSV parsing with error handling for encoding
def parse_csv(file):
    try:
        df = pd.read_csv(file, index_col=0, encoding='utf-8')
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file, index_col=0, encoding='latin1')
        except Exception as e:
            raise Exception(f'Failed to read CSV file: {str(e)}')
    return df

# Heatmap route
@app.route('/heatmap', methods=['POST'])
def generate_heatmap():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read file directly into memory
        df = parse_csv(file)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if df.empty:
        return jsonify({'error': 'Uploaded CSV is empty or invalid.'}), 400

    # Get width and height from form data
    width = int(request.form.get('width', 800))
    height = int(request.form.get('height', 600))

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=df.values.tolist(),  # Heatmap data
        x=df.columns.tolist(),  # Column names for x-axis ticks
        y=df.index.tolist(),    # Row names for y-axis ticks
        colorscale='Viridis',
        colorbar=dict(title='Expression')
    ))
    fig.update_layout(
        xaxis_title='Gene',
        yaxis_title='SampleID',
        width=width,
        height=height
    )

    # Return figure data and layout
    return jsonify({
        'data': fig.to_dict()['data'],
        'layout': fig.to_dict()['layout']
    })

# Volcano plot route
@app.route('/volcano', methods=['POST'])
def generate_volcano():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read file directly into memory
        df = parse_csv(file)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Ensure necessary columns exist
    if 'log2FoldChange' not in df.columns or '-log10(pvalue)' not in df.columns:
        return jsonify({'error': 'CSV must contain "log2FoldChange" and "-log10(pvalue)" columns.'}), 400

    # Get width and height from form data
    width = int(request.form.get('width', 800))
    height = int(request.form.get('height', 600))

    # Create volcano plot
    fig = go.Figure()

    # Significance threshold (e.g., p < 0.05)
    significant = df['pvalue'] < 0.05

    fig.add_trace(go.Scatter(
        x=df.loc[significant, 'log2FoldChange'].tolist(),
        y=df.loc[significant, '-log10(pvalue)'].tolist(),
        mode='markers',
        marker=dict(color='red', size=8),
        name='Significant (p < 0.05)',
        text=df.loc[significant].index.tolist(),  # Row names as hover text
        hoverinfo='text+x+y'  # Show row names, x, and y values on hover
    ))

    fig.add_trace(go.Scatter(
        x=df.loc[~significant, 'log2FoldChange'].tolist(),
        y=df.loc[~significant, '-log10(pvalue)'].tolist(),
        mode='markers',
        marker=dict(color='blue', size=8),
        name='Not Significant (p >= 0.05)',
        text=df.loc[~significant].index.tolist(),  # Row names as hover text
        hoverinfo='text+x+y'  # Show row names, x, and y values on hover
    ))

    fig.update_layout(
        xaxis_title="Log2 Fold Change",
        yaxis_title="-Log10 p-value",
        showlegend=True,
        width=width,
        height=height
    )

    # Return figure data and layout
    return jsonify({
        'data': fig.to_dict()['data'],
        'layout': fig.to_dict()['layout']
    })

if __name__ == '__main__':
    app.run(debug=True)
