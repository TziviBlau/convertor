#!/usr/bin/env python3
import os
import sys
from PIL import Image
import glob
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def convert_images_to_pdf(image_paths, output_pdf=None):
    """
    Convert one or more images to a PDF file
    
    Args:
        image_paths: List of image paths or single image path
        output_pdf: Name of the output PDF file (default is "output.pdf")
    """
    # Use environment variable for PDF name if available
    if output_pdf is None:
        output_pdf = os.environ.get("PDF_NAME", "output.pdf")
    
    # Make sure output directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Ensure output PDF has .pdf extension
    if not output_pdf.endswith('.pdf'):
        output_pdf += '.pdf'
    
    output_path = os.path.join(output_dir, output_pdf)
    
    # If single string is passed (not a list)
    if isinstance(image_paths, str):
        # If it's a directory, get all images
        if os.path.isdir(image_paths):
            image_paths = glob.glob(os.path.join(image_paths, '*.jpg')) + \
                         glob.glob(os.path.join(image_paths, '*.jpeg')) + \
                         glob.glob(os.path.join(image_paths, '*.png'))
        else:
            # It's a single image
            image_paths = [image_paths]
    
    # Sort images to ensure consistent ordering
    image_paths.sort()
    
    if not image_paths:
        print("No images found to convert.")
        return
    
    # Create PDF
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            img_width, img_height = img.size
            
            # Scale image to fit page while maintaining aspect ratio
            aspect = img_width / float(img_height)
            if aspect > 1:
                # Width is greater than height
                img_width = width - 50
                img_height = img_width / aspect
            else:
                # Height is greater than width
                img_height = height - 50
                img_width = img_height * aspect
            
            # Center image on page
            x_centered = (width - img_width) / 2
            y_centered = (height - img_height) / 2
            
            # Draw image on the page
            c.drawImage(img_path, x_centered, y_centered, width=img_width, height=img_height)
            c.showPage()
            
            print(f"Added image: {img_path}")
        except Exception as e:
            print(f"Error processing image {img_path}: {e}")
    
    # Save the PDF
    c.save()
    print(f"PDF created successfully: {output_path}")
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_image_to_pdf.py <image_path or directory>")
        sys.exit(1)
    
    path = sys.argv[1]
    convert_images_to_pdf(path)
