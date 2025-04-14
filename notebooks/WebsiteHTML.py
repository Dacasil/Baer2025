def getHTML():
    return """
< !DOCTYPE
html >
< html
lang = "de" >
< head >
< meta
charset = "UTF-8" >
< meta
name = "viewport"
content = "width=device-width, initial-scale=1.0" >
< title > Dateiverarbeitung < / title >
< style >
:root
{
    --jb - dark - blue:  # 00205B;
        --jb - light - blue:  # 0070C0;
--jb - gold:  # B39757;
--jb - white:  # FFFFFF;
--jb - light - gray:  # F5F5F5;
}

body
{
    font - family: 'Helvetica Neue', Arial, sans - serif;
background - color: var(--jb - light - gray);
margin: 0;
padding: 0;
display: flex;
justify - content: center;
align - items: center;
min - height: 100
vh;
color:  # 333;
}

.container
{
    background - color: var(--jb - white);
border - radius: 8
px;
box - shadow: 0
4
px
12
px
rgba(0, 32, 91, 0.1);
padding: 40
px;
width: 100 %;
max - width: 600
px;
text - align: center;
}

h1
{
    color: var(--jb - dark - blue);
margin - bottom: 24
px;
font - weight: 300;
}

.logo
{
    margin - bottom: 32px;
color: var(--jb - dark - blue);
font - size: 24
px;
font - weight: 600;
}

.upload - area
{
    border: 2px dashed var(--jb - light - blue);
border - radius: 6
px;
padding: 30
px;
margin - bottom: 24
px;
transition: all
0.3
s
ease;
cursor: pointer;
}

.upload - area: hover
{
    background - color: rgba(0, 112, 192, 0.05);
}

.upload - icon
{
    font - size: 48px;
color: var(--jb - light - blue);
margin - bottom: 16
px;
}

.file - input
{
    display: none;
}

.btn
{
    background - color: var(--jb - dark - blue);
color: white;
border: none;
padding: 12
px
24
px;
border - radius: 4
px;
cursor: pointer;
font - size: 16
px;
transition: background - color
0.3
s;
}

.btn: hover
{
    background - color: var(--jb - light - blue);
}

.result
{
    margin - top: 24px;
padding: 16
px;
background - color: var(--jb - light - gray);
border - radius: 4
px;
display: none;
}

.file - info
{
    margin - top: 16px;
font - size: 14
px;
color: var(--jb - light - blue);
}
< / style >
< / head >
< body >
< div


class ="container" >

< div


class ="logo" > DATEIVERARBEITUNG < / div >

< h1 > Bitte
laden
Sie
Ihre
4
Dateien
hoch < / h1 >

< form
method = "post"
enctype = "multipart/form-data"
id = "uploadForm" >
< input
type = "file"
name = "files"
multiple


class ="file-input" id="fileInput" required >

< label
for ="fileInput" >
< div


class ="upload-area" id="uploadArea" >

< div


class ="upload-icon" > ↑ < / div >

< p > Klicken
Sie
hier
oder
ziehen
Sie
die
Dateien
per
Drag & Drop < / p >
< p > < small > Bitte
genau
4
Dateien
auswählen < / small > < / p >
< / div >
< / label >

< div


class ="file-info" id="fileInfo" > < / div >

< button
type = "submit"


class ="btn" > Dateien verarbeiten < / button >

< / form >

< div


class ="result" id="result" > < / div >

< / div >

< script >
const
fileInput = document.getElementById('fileInput');
const
uploadArea = document.getElementById('uploadArea');
const
fileInfo = document.getElementById('fileInfo');
const
resultDiv = document.getElementById('result');
const
form = document.getElementById('uploadForm');

// Drag and drop
Funktionen
uploadArea.addEventListener('dragover', (e) = > {
    e.preventDefault();
uploadArea.style.backgroundColor = 'rgba(0, 112, 192, 0.1)';
});

uploadArea.addEventListener('dragleave', () = > {
    uploadArea.style.backgroundColor = '';
});

uploadArea.addEventListener('drop', (e) = > {
    e.preventDefault();
uploadArea.style.backgroundColor = '';
fileInput.files = e.dataTransfer.files;
updateFileInfo();
});

fileInput.addEventListener('change', updateFileInfo);

function
updateFileInfo()
{
if (fileInput.files.length > 0)
{
    const
names = Array.
from

(fileInput.files).map(f= > f.name).join(', ');
fileInfo.textContent = `Ausgewählte
Dateien: ${names}(${fileInput.files.length} / 4)`;
} else {
    fileInfo.textContent = '';
}
}

form.addEventListener('submit', async (e) = > {
    e.preventDefault();

if (fileInput.files.length !== 4)
{
    showResult('Bitte genau 4 Dateien auswählen', 'error');
return;
}

const
formData = new
FormData(form);

try {
const response = await fetch('/', {
method: 'POST',
body: formData
});

const
result = await response.text();
showResult(result, 'success');
} catch(error)
{
    showResult('Fehler bei der Verarbeitung: ' + error.message, 'error');
}
});

function
showResult(message, type)
{
    resultDiv.textContent = message;
resultDiv.style.display = 'block';
resultDiv.style.color = type == = 'error' ? '#d32f2f': '#00205B';
}
< / script >
    < / body >
        < / html >
"""