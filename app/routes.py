from flask import Flask, request, render_template, redirect, url_for
import os
from werkzeug.utils import secure_filename
from utils import load_data, clean_data, generate_eda_report

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'data/uploads'
OUTPUT_FOLDER = 'data/output'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    """
    Route for uploading a dataset file.
    """
    if request.method == "POST":
        # Check if a file is uploaded
        if "file" not in request.files:
            return "No file part in the request"

        file = request.files["file"]

        # If no file is selected, or the file has no name
        if file.filename == "":
            return "No selected file"

        # Secure the filename and save it
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            return redirect(url_for("process_file", file_path=file_path))

    return render_template("index.html")

@app.route("/process")
def process_file():
    """
    Route to process the uploaded dataset file.
    """
    # Get the file path from the request args
    file_path = request.args.get("file_path")
    
    # Load the data
    data = load_data(file_path)
    if data is None:
        return "Failed to load data."

    # Clean the data
    cleaned_data = clean_data(data)

    # Generate EDA report and basic plots
    plot_files = generate_eda_report(cleaned_data, output_path=app.config['OUTPUT_FOLDER'])

    # Convert plot files to relative paths for displaying in templates
    relative_paths = [os.path.relpath(f, start="static") for f in plot_files]

    # Redirect to the results page with plot paths
    return redirect(url_for("show_results", plot_files=relative_paths))

@app.route("/results")
def show_results():
    """
    Route to display results from data processing and EDA.
    """
    # Get the list of plot files from the request args
    plot_files = request.args.getlist("plot_files")

    return render_template("results.html", plot_files=plot_files)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
