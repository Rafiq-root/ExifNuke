#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from PIL import Image, ExifTags

# Configuration: Where folders are located
INPUT_FOLDER = "./Images_Input"
CLEAN_FOLDER = "./Images_Clean"
LOG_FOLDER = "./Metadata_Logs"

def setup_folders():
    """
    Checks if the output directories exist.
    If they do not exist, this function creates them to prevent file errors.
    """
    if not os.path.exists(CLEAN_FOLDER):
        os.makedirs(CLEAN_FOLDER)
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

def extract_metadata(image, filename):
    """
    Extracts EXIF metadata from an image object.
    
    Args:
        image (PIL.Image): The opened image object.
        filename (str): The name of the file being processed.
        
    Returns:
        bool: True if metadata was found and saved, False otherwise.
    """
    exif_data = image.getexif()
    
    log_filename = f"{os.path.splitext(filename)[0]}_report.txt"
    log_path = os.path.join(LOG_FOLDER, log_filename)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"--- METADATA REPORT: {filename} ---\n\n")
        
        if not exif_data:
            f.write("No EXIF metadata found in this image.\n")
            return False

        found_data = False
        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            f.write(f"{tag_name}: {value}\n")
            found_data = True
            
    return found_data

def clean_image(image, filename):
    """
    Creates a deep copy of the image pixel data without the metadata tags.
    
    Args:
        image (PIL.Image): The source image.
        filename (str): The output filename.
    """
    clean_path = os.path.join(CLEAN_FOLDER, filename)
    
    # Extract raw pixel data to strip attached metadata
    data = list(image.getdata())
    
    # Create new image object with same mode and size
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    
    image_without_exif.save(clean_path)
    print(f"   [+] Clean image saved to: {clean_path}")

def process_images():
    """
    Main orchestration function.
    Iterates through the input folder, handles errors, and calls processing functions.
    """
    print(f"[*] Scanning folder: {INPUT_FOLDER} ...")
    
    for filename in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, filename)
        
        if not os.path.isfile(file_path):
            continue
            
        try:
            with Image.open(file_path) as img:
                print(f"\nProcessing: {filename}")
                
                # Step 1: Extract & Log Data
                has_data = extract_metadata(img, filename)
                if has_data:
                    print(f"   [!] Metadata found! Saved to {LOG_FOLDER}")
                else:
                    print("   [i] No metadata found.")
                
                # Step 2: Create Clean Copy
                clean_image(img, filename)
                
        except Exception as e:
            print(f"   [x] Could not process {filename}: {e}")

if __name__ == "__main__":
    setup_folders()
    process_images()
    print("\n[Done] All images processed.")