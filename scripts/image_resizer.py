from PIL import Image
import os

# ======== CONFIGURE THESE ========
input_folder = "survival_arena/icons/entities"          # Folder containing PNGs
output_folder = "survival_arena/resized_legends" # Folder to save resized images
target_size = (16, 16)         # (width, height)
# =================================

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all PNG files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".png"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Open and resize image
        with Image.open(input_path) as img:
            resized_img = img.resize(target_size, Image.Resampling.LANCZOS)
            resized_img.save(output_path, "PNG")
        
        print(f"✅ Resized and saved: {output_path}")

print("\n🎉 All PNG images have been resized successfully!")
