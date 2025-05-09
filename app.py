from flask import Flask, request, send_file, render_template_string
import os
from convert_docx_to_txt import process_docx_files

app = Flask(__name__)
UPLOAD_FOLDER = "legal_docs"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        if "file" not in request.files:
            error = "No file uploaded!"
        else:
            file = request.files["file"]
            if file.filename == "":
                error = "No file selected!"
            elif file and file.filename.endswith(".docx"):
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)
                output_file, process_error = process_docx_files()
                if process_error:
                    error = process_error
                else:
                    return send_file(output_file, as_attachment=True)
            else:
                error = "Please upload a .docx file!"
    return render_template_string("""
        <!DOCTYPE html>
        <html>
        <body>
            <h2>Upload .docx File</h2>
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".docx">
                <input type="submit" value="Upload and Process">
            </form>
            {% if error %}
                <p style="color:red;">{{ error }}</p>
            {% endif %}
        </body>
        </html>
    """, error=error)

if __name__ == "__main__":
    app.run(debug=True)