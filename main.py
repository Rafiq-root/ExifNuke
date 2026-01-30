import os
from PIL import Image, ExifTags

# Configuration: Where folders are located
INPUT_FOLDER = "./Images_Input"
CLEAN_FOLDER = "./Images_Clean"
LOG_FOLDER = "./Metadata_Logs"

def setup_folders():
    """Create the necessary folders if they don't exist."""
    if not os.path.exists(CLEAN_FOLDER):
        os.makedirs(CLEAN_FOLDER)
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)

def extract_metadata(image, filename):
    """
    Extracts hidden data (EXIF) from the image and saves it to a text file.
    """
    # Get the raw EXIF data dictionary
    exif_data = image.getexif()
    
    # Create a text file name (e.g., photo.jpg -> photo_report.txt)
    log_filename = f"{os.path.splitext(filename)[0]}_report.txt"
    log_path = os.path.join(LOG_FOLDER, log_filename)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"--- METADATA REPORT: {filename} ---\n\n")
        
        if not exif_data:
            f.write("No EXIF metadata found in this image.\n")
            return False

        # Loop through all the hidden tags
        found_data = False
        for tag_id, value in exif_data.items():
            # Translate the number ID (e.g., 306) to a human name (e.g., "DateTime")
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            
            # Write it to the text file
            f.write(f"{tag_name}: {value}\n")
            found_data = True
            
    return found_data

def clean_image(image, filename):
    """
    Saves a new copy of the image without the metadata.
    """
    clean_path = os.path.join(CLEAN_FOLDER, filename)
    
    # We create a new empty image list to strip data
    data = list(image.getdata())
    
    # Creating a fresh image object ensures no old metadata carries over
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    
    image_without_exif.save(clean_path)
    print(f"   [+] Clean image saved to: {clean_path}")

def process_images():
    print(f"[*] Scanning folder: {INPUT_FOLDER} ...")
    
    # Loop through every file in the input folder
    for filename in os.listdir(INPUT_FOLDER):
        file_path = os.path.join(INPUT_FOLDER, filename)
        
        # Skip if it's a folder or not an image
        if not os.path.isfile(file_path):
            continue
            
        try:
            # Open the image
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