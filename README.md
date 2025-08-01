# seq-visualizer
Components for building an interactive webpage to visualize transcriptomic sequencing data

## Interactive website to generate publication-ready figures

- Goal: Create a user-friendly website that scientists can use to visualize sequencing data

*See "sequencingVisualization_stepByStep.ipynb" file for the step-by-step breakdown*

### Requirements:
1. Set up environment
- Language: Python
- Libraries: flask, pandas, matplotlib, seaborn, plotly, scikit-learn
2. Frontend: A user-friendly interface for data upload, parameter selection, and figure customization.
- Framework: React (with libraries like shadcn/ui for UI components)
- File upload handling
- Interactive figure customization
3. Backend: Data processing and visualization generation.
- Language: Python (Flask or FastAPI)
- Libraries: Seaborn, Matplotlib, Plotly
- Handling CSV/TXT data uploads
4. Figure Generation:
- Heatmaps: Seaborn/Matplotlib
- Volcano & MA Plots: Matplotlib
- PCA: Scikit-learn for computation, Plotly for interactive visuals
5. Deployment:
- Docker container for reproducibility
- Local server

### Step 1: Set up the environment
### Step 2: Create the frontend (HTML)
### Step 3A: Create the backend (Flask Server)
### Step 3B: Test the backend
### Step 4: Generate figures
### Step 5: Deployment

### How to allow others to use the same environment
- User must have Docker installed: https://www.docker.com/get-started/
- Include the following files in the appropriate directory structure:
```
C:\repos\seq-visualizer
│
├── static
│   ├── index.html
├── .dockerignore
├── app.py
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```
- After setting up directory, run the following code in terminal to build docker image
```
# python -m venv venv # only need to create this once
# on windows: venv\Scripts\activate 
OR
# on linux: source venv/bin/activate

wsl # open linux box on windows
docker-compose up
# if image isn't already created, it will be built before running in container
# if need to modify the script and rebuild the image, run the following line
# docker-compose up --build
```
- Open web browser and navigate to: http://127.0.0.1:5000/