from flask import Flask, render_template, request, redirect, url_for
import os
import random

app = Flask(__name__)

# Define the directories to save uploaded files
UPLOAD_FOLDER = 'uploads'
SHIRT_UPLOAD_FOLDER = 'static/shirt_uploads'
PANT_UPLOAD_FOLDER = 'static/pant_uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SHIRT_UPLOAD_FOLDER'] = SHIRT_UPLOAD_FOLDER
app.config['PANT_UPLOAD_FOLDER'] = PANT_UPLOAD_FOLDER

# Ensure the upload directories exist
for folder in [UPLOAD_FOLDER, SHIRT_UPLOAD_FOLDER, PANT_UPLOAD_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

@app.route("/")
def home():
    # Get random shirt and pant images
    shirt_image = get_random_image("static/shirt_uploads")
    pant_image = get_random_image("static/pant_uploads")

    # Pass images to the template
    return render_template("index.html", random_shirt_image=shirt_image, random_pant_image=pant_image)

@app.route("/AddS")
def adds():
    return render_template("add.html", upload_type='shirt')

@app.route("/AddP")
def addp():
    return render_template("add_pants.html", upload_type='pant')

@app.route("/Shuffle")
def shuffle():
    pass

@app.route("/upload", methods=["POST"])
def upload():
    # Determine the upload type from the form
    upload_type = request.form.get('upload_type')

    # Get the appropriate upload folder based on the upload type
    if upload_type == 'shirt':
        upload_folder = app.config['SHIRT_UPLOAD_FOLDER']
    elif upload_type == 'pant':
        upload_folder = app.config['PANT_UPLOAD_FOLDER']
    else:
        return "Invalid upload type"

    # Save each file to the corresponding upload directory
    files = request.files.getlist("files[]")
    for file in files:
        file.save(os.path.join(upload_folder, file.filename))

    # Render the upload.html template with a link to go back to the home page
    return redirect('..')

@app.route("/upload_pants", methods=["POST"])
def upload_pants():
    # Determine the upload type from the form
    upload_type = request.form.get('upload_type')

    # Get the appropriate upload folder based on the upload type
    if upload_type == 'pant':
        upload_folder = app.config['PANT_UPLOAD_FOLDER']
    else:
        return "Invalid upload type"

    # Save each file to the corresponding upload directory
    files = request.files.getlist("files[]")
    for file in files:
        file.save(os.path.join(upload_folder, file.filename))

   # Redirect to the home page
    return redirect('..')

if __name__ == "__main__":
    app.run(debug=True)

# Assuming you have functions to get random images from directories
def get_random_image(directory):
    image_files = os.listdir(directory)
    return random.choice(image_files)

