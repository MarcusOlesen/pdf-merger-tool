# PDF Merger Tool

A simple desktop GUI application to **merge multiple PDF files** with drag-and-drop ordering and a clean interface.

I built this tool because I often need to combine multiple PDFs and wanted something lightweight and offline — without having to upload files to online tools every time.

---

## 🚀 Features

- Select one or more PDF files from your computer  
- Reorder them by drag-and-drop  
- Merge and save with a custom name  
- Simple progress dialog while merging  
- Automatically closes when finished  
- Works fully offline  

---

## 🧰 Requirements

You’ll need **Python 3.8+** and the following Python packages:

```
PyQt6
PyPDF2
````

Install them with:

```bash
pip install PyQt6 PyPDF2
````

---

## 💻 How to Run

Clone or download this repository, then from the project folder run:

```bash
python pdf_merger.py
```

The app will launch with a simple window:

1. Click **Select PDFs** to choose your files
2. Reorder them as needed by dragging
3. Click **Merge PDFs** and choose a file name to save

---

##  Build a Standalone `.exe`

If you want to use it without opening a terminal each time, you can package it as a single executable using **PyInstaller**:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico pdf_merger.py
```

* `--onefile` → bundles everything into one file
* `--windowed` → hides the terminal window
* `--icon=icon.ico` → adds a custom icon (optional)

The generated `.exe` will appear in the `dist/` folder.
```
