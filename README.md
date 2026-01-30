# ☢️ Exif Nuke (Privacy Tool)

**Exif Nuke** is a forensic privacy tool designed to strip hidden metadata (EXIF data) from images. 

Modern smartphones and cameras embed sensitive data into photos—including GPS coordinates, device models, and timestamps—which can compromise user privacy when uploaded online. This tool automatically scans, extracts this hidden intelligence for review, and produces a clean, safe version of the image.

## 🚀 Features
* **Automated Scanning:** Detects images in a target directory automatically.
* **Metadata Extraction:** Rips out hidden EXIF data and saves it to a text log for forensic review.
* **Privacy Scrubbing:** Generates a 1:1 copy of the image with zero metadata.
* **Bulk Processing:** Can handle multiple images in a single batch.

## 📦 Built With
* **Python 3:** The core automation logic.
* **Pillow (PIL):** The Python Imaging Library used to access internal file headers. It allows the script to read raw EXIF tags and reconstruct the image pixels without the attached data payload.

## 🛠️ Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Rafiq-root/ExifNuke.git](https://github.com/Rafiq-root/ExifNuke.git)
    cd ExifNuke
    ```

2.  **Set up the environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## 💻 Usage

1.  Place your target images (JPEG/JPG) into the `Images_Input` folder.
2.  Run the tool:
    ```bash
    python main.py
    ```
3.  **View Results:**
    * **Clean Images:** Located in the `Images_Clean` folder.
    * **Data Logs:** Metadata reports are found in `Metadata_Logs`.

## 🛡️ Disclaimer
This tool is intended for privacy protection and educational purposes. Always ensure you have ownership of the files you are processing.