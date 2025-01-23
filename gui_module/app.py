import os
from flask import Flask, render_template, request, session, redirect, url_for, flash
from markupsafe import Markup
from flask_session import Session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()

"""
For production create secret key via passlib or bcrypt
This is used in session and cookies (it generates tokens)
In cookies it protects agains Cross-Site Request Forgery (CSRF)
app.secret_key = "your_secret_key"  # Replace with a secure key
"""

app.config["SESSION_TYPE"] = "filesystem"  # or could use db here
Session(app)

real_controller = None
UPLOAD_FOLDER = os.getenv("INPUT_FILES")
print(f"GUI UPLOAD FOLDER: {UPLOAD_FOLDER}")
 

# Custom filter to convert newlines to <br> tags
@app.template_filter("nl2br")
def nl2br(value):
    return Markup(value.replace("\n", "<br>"))

# make the controller a Singleton
def get_real_controller():
    from controllers.real_controller import RealController
    global real_controller
    if real_controller is None:
        real_controller = RealController()
    return real_controller


@app.route("/", methods=["GET", "POST"])
def index():
    controller = get_real_controller()
    # Initialize chat history if it doesn't exist
    if "history" not in session:
        session["history"] = []

    if request.method == "POST":
        user_input = request.form["user_input"].strip()
        print(f"User Input: {user_input}")  # Debugging statement

        # just truncation user_input for the summary for now
        user_input_summary = user_input[:25]
        if len(user_input) > 25:
            user_input_summary += "..."

        # Process the input and generate a response
        # response = f"Response to: {user_input}"
        response = controller.retrieve_response(user_input)
        #print(f"In app, response is: {response}")

        # Add the new entry to history
        session["history"].insert(0,{"user": user_input, "response": response, "user_summary": user_input_summary})
        session.modified = True  # Mark the session as modified to save changes

        # Redirect to the same page to prevent resubmission
        return redirect(url_for("index"))

    return render_template("index.html", history=session["history"])


@app.route("/clear_history", methods=["POST"])
def clear_history():
    session.pop("history", None)  # Remove history from session
    return redirect(url_for("index"))  # Redirect to the main page

# Allowed file extensions (adjust as needed)
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif", "docx","xlsx", "pptx"}

# Helper function to check allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for file upload
# This will call the factory and trigger the loader (based on file extension)
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No file part")
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        print(f"\n***APP.py file_path {file_path}")
        file.save(file_path)
        get_real_controller().load_the_file(file_path)
        flash("File successfully uploaded")
        return redirect(url_for("index"))
    else:
        flash("File type not allowed")
        return redirect(url_for("index"))




# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Other routes and app code here
if __name__ == "__main__":
    app.run(debug=True, port=8081)
