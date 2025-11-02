# Exiftract

Exiftract is a simple, dark-theme GUI tool built with Python and Tkinter. It allows you to load an image (`.jpg`, `.jpeg`, `.tiff`) and instantly extract all its EXIF (Exchangeable Image File Format) metadata.



## Features

* **Clean Interface:** A modern, dark-theme GUI that's easy to use.
* **Full Data Extraction:** Pulls basic info (format, size) and all available EXIF data.
* **GPS Decoding:** Automatically finds, decodes, and displays GPS coordinates if they exist.
* **Organized View:** All metadata is shown in a clean, sortable table.
* **Save Reports:** You can save the full metadata report to a `.txt` file.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/exiftract.git](https://github.com/your-username/exiftract.git)
    cd exiftract
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    *(On Windows, use `.venv\Scripts\activate`)*

3.  **Install dependencies:**
    This project requires **Pillow**.
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  Run the script:
    ```bash
    python3 exiftract.py
    ```
2.  Click **"Browse..."** to select an image file.
3.  Click **"Scan Selected Image"** to extract and display the metadata.
4.  Click **"Save Report as .txt"** to save the results.
