from flask import Flask, request, render_template_string, redirect, url_for
from markupsafe import Markup
import os
import time
from datetime import datetime
import webbrowser
from time import sleep
from queue import Queue


app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File processing | Julius Bär</title>
    <style>
        :root {
            --jb-dark-blue: #00205B;
            --jb-blue: #0056B3;
            --jb-light-blue: #E6F0FA;
            --jb-white: #FFFFFF;
            --jb-gray: #F8F8F8;
            --jb-dark-gray: #333333;
            --jb-border: #E0E0E0;
        }

        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--jb-gray);
            color: var(--jb-dark-gray);
            line-height: 1.6;
        }

        .header {
            background-color: var(--jb-white);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            padding: 20px 0;
            border-bottom: 1px solid var(--jb-border);
        }

        .header-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            align-items: center;
        }

        .logo {
            height: 40px;
        }

        .main-container {
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
        }

        .card {
            background-color: var(--jb-white);
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            padding: 40px;
            margin-bottom: 30px;
        }

        h1 {
            color: var(--jb-dark-blue);
            font-weight: 500;
            font-size: 28px;
            margin-top: 0;
            margin-bottom: 30px;
        }

        .upload-container {
            border: 2px dashed var(--jb-blue);
            border-radius: 4px;
            padding: 40px;
            text-align: center;
            margin-bottom: 25px;
            background-color: var(--jb-light-blue);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .upload-container:hover {
            background-color: rgba(0, 86, 179, 0.1);
        }

        .upload-icon {
            font-size: 48px;
            color: var(--jb-blue);
            margin-bottom: 15px;
        }

        .file-input {
            display: none;
        }

        .btn {
            background-color: var(--jb-blue);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: background-color 0.3s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .btn:hover {
            background-color: var(--jb-dark-blue);
        }

        .file-info {
            margin: 20px 0;
            font-size: 14px;
            color: var(--jb-blue);
        }

        .result-box {
            margin-top: 30px;
            padding: 20px;
            background-color: var(--jb-light-blue);
            border-left: 4px solid var(--jb-blue);
            display: {% if result %}block{% else %}none{% endif %};
        }

        .footer {
            text-align: center;
            padding: 30px 0;
            color: #666;
            font-size: 14px;
            border-top: 1px solid var(--jb-border);
        }

        .requirements {
            font-size: 14px;
            color: #666;
            margin-top: 30px;
        }
        .header-container {
            display: flex;
            justify-content: center; /* Horizontally center */
            align-items: center;    /* Vertically center */
            height: 100%;           /* Ensure full height alignment */
        }
    
        .header-title {
            font-size: 28px;        /* Slightly larger font */
            font-weight: bold;      /* Bold text */
            color: var(--jb-blue);  /* Correct blue color */
            margin: 0;              /* Remove default margin */
            text-align: center;     /* Center text alignment */
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-container">
            <h1 class="header-title">FiveNeu(t)rons</h1>
        </div>
    </header>

    <main class="main-container">
        <div class="card">
            <h1>File processing</h1>

            <form method="post" enctype="multipart/form-data" id="uploadForm">
                <input type="file" name="files" multiple class="file-input" id="fileInput" required>

                <label for="fileInput">
                    <div class="upload-container" id="uploadArea">
                        <div class="upload-icon">↑</div>
                        <p>Select files to upload</p>
                        <p><small>Please select exactly 4 files (PDF, Excel, Word)</small></p>
                    </div>
                </label>

                <div class="file-info" id="fileInfo">
                    {% if filenames %}Selected files: {{ filenames }}{% endif %}
                </div>

                <button type="submit" class="btn">Process files</button>

                <div class="requirements">
                    <p>Requirements:</p>
                    <ul>
                        <li>Maximum 10 MB per file</li>
                        <li>Permitted formats: .pdf, .xlsx, .docx</li>
                        <li>Total size must not exceed 25 MB</li>
                    </ul>
                </div>
            </form>

            <div class="result-box" id="result">
                {% if result %}{{ result }}{% endif %}
            </div>
        </div>
    </main>

    <footer class="footer">
        <p>© 2025 FiveNeu(t)rons | All rights reserved</p>
    </footer>

    <script>
        const fileInput = document.getElementById('fileInput');
        const uploadArea = document.getElementById('uploadArea');
        const fileInfo = document.getElementById('fileInfo');
        const form = document.getElementById('uploadForm');

        // Drag and drop Funktionen
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.style.backgroundColor = 'rgba(0, 86, 179, 0.2)';
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.style.backgroundColor = '';
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.style.backgroundColor = '';
            fileInput.files = e.dataTransfer.files;
            updateFileInfo();
        });

        fileInput.addEventListener('change', updateFileInfo);

        function updateFileInfo() {
            if (fileInput.files.length > 0) {
                const names = Array.from(fileInput.files).map(f => f.name).join(', ');
                fileInfo.innerHTML = `<strong>Selected files:</strong> ${names} <br>(${fileInput.files.length} from 4 files)`;
            } else {
                fileInfo.textContent = '';
            }
        }

        form.addEventListener('submit', function(e) {
            if (fileInput.files.length !== 4) {
                e.preventDefault();
                fileInfo.innerHTML = '<span style="color:#d32f2f;">Please select exactly 4 files</span>';
            }
        });
    </script>
</body>
</html>
"""
RESULT_HTML = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Result | Julius Bär</title>
    <style>
        :root {
            --jb-dark-blue: #00205B;
            --jb-blue: #0056B3;
            --jb-white: #FFFFFF;
            --jb-gray: #F8F8F8;
            --jb-dark-gray: #333333;
        }

        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--jb-gray);
            color: var(--jb-dark-gray);
            line-height: 1.6;
        }

        .header {
            background-color: var(--jb-white);
            padding: 20px 0;
            border-bottom: 1px solid #E0E0E0;
        }

        .header-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            align-items: center;
        }

        .logo {
            height: 40px;
        }

        .main-container {
            max-width: 800px;
            margin: 40px auto;
            padding: 0 20px;
        }

        .card {
            background-color: var(--jb-white);
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            padding: 40px;
            text-align: center;
        }

        h1 {
            color: var(--jb-dark-blue);
            font-weight: 500;
            font-size: 28px;
            margin-top: 0;
            margin-bottom: 30px;
        }

        .result-box {
            background-color: #F5F5F5;
            border-left: 4px solid var(--jb-blue);
            padding: 20px;
            margin: 30px 0;
            text-align: left;
            font-family: monospace;
            white-space: pre-wrap;
        }

        .btn {
            background-color: var(--jb-blue);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: background-color 0.3s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            text-decoration: none;
            display: inline-block;
            margin-top: 20px;
        }

        .btn:hover {
            background-color: var(--jb-dark-blue);
        }
        .header-container {
        display: flex;
        justify-content: center; /* Horizontally center */
        align-items: center;    /* Vertically center */
        height: 100%;           /* Ensure full height alignment */
        }

        .header-title {
            font-size: 28px;        /* Slightly larger font */
            font-weight: bold;      /* Bold text */
            color: var(--jb-blue);  /* Correct blue color */
            margin: 0;              /* Remove default margin */
            text-align: center;     /* Center text alignment */
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-container">
            <h1 class="header-title">FiveNeu(t)rons</h1>
        </div>
    </header>

    <main class="main-container">
        <div class="card">
            <h1>What we found</h1>

            <div class="result-box">
                {{ result_text }}
            </div>

            <a href="/" class="btn">Upload more</a>
        </div>
    </main>

    <footer class="footer">
        <p>© 2023 FiveNeu(t)rons | All rights reserved</p>
    </footer>
</body>
<style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px 0;
        background-color: var(--jb-white);
        border-top: 1px solid #E0E0E0;
        font-size: 14px;
        color: #666;
    }
</style>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    result = None
    filenames = None

    save_path = "data/website"
    os.makedirs(save_path, exist_ok=True)


    if request.method == 'POST':
        files = request.files.getlist('files')
        if len(files) != 4:
            result = "Fehler: Bitte genau 4 Dateien hochladen"
        else:
            # Hier kommt deine Dateiverarbeitung
            filenames = [file.filename for file in files]
            result = Markup(f"Erfolgreich verarbeitet!<br><br>Dateien:<ul>" + "".join(
                f"<li>{filename}</li>" for filename in filenames) + "</ul>")

            # Generate the timestamped directory name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Format: YYYYMMDD_HHMMSS
            directory_path = os.path.join(save_path, timestamp)
            os.makedirs(directory_path, exist_ok=True)  # Create the directory

            # Save each file in the directory
            for file in files:
                file.save(os.path.join(directory_path, file.filename))
            processing_result = " \nExample Output:\nPassport surname 'V' drastically contradicts the full surname 'Livi' provided in the profile and narrative data. This is beyond a typo and suggests a potential issue with the passport information or a mismatch of identities. While the passport first name initial 'G' aligns with Giulia, the missing surname raises a significant flag"

            return redirect(url_for('show_result', result=processing_result))

    return render_template_string(HTML_TEMPLATE,
                                  result=result,
                                  filenames=", ".join(filenames) if filenames else None)


def start_website():
    #webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=True)

@app.route('/result')
def show_result():
    return render_template_string(RESULT_HTML, result_text=request.args.get('result', 'Kein Ergebnis vorhanden'))


# def start_website():
#     print("Starting Website...")
#     app.run(debug=True)


if __name__ == '__main__':
    start_website()
#start_website()