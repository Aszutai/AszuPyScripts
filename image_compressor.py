import os
import zipfile
import shutil
from PIL import Image

def convert_zip_file(zip_file_path):
    print("Starting image compression")
    dir_path, file_name = os.path.split(zip_file_path)
    temp = os.path.join(dir_path, 'temp')
    # Extract the zip file to a temporary directory
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp)
    
    # Convert all images in the temporary directory to JPEG format
    for root, dirs, files in os.walk(temp):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                # Open the image and save it in JPEG format with quality 80%
                image_path = os.path.join(root, file)
                with Image.open(image_path) as image:
                    # If the image width is greater than 1980, resize it to a maximum width of 1980
                    if image.width > 1980:
                      new_height = int((1980 / float(image.width)) * image.height)
                      image = image.resize((1980, new_height), Image.LANCZOS)
                    if image.mode == 'RGBA':
                      background = Image.new('RGB', image.size, (255, 255, 255))
                      background.paste(image, mask=image.split()[3])
                      image = background
                      image.convert('RGB').save(image_path, 'JPEG', quality=80)
                    else:
                      image.save(image_path, 'JPEG', quality=80)
    print("Image compressed")
    
    # Create a new zip file with the converted images
    with zipfile.ZipFile(zip_file_path, 'w') as zip_ref:
        for root, dirs, files in os.walk(temp):
            for file in files:
                zip_ref.write(os.path.join(root, file), file)
    
    # Remove the temporary directory
    shutil.rmtree(temp)
    print("Done")

##
def main():
    convert_zip_file(r".zip")



##
if __name__ == '__main__':
    main()
    