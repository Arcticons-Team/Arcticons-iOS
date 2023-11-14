import os
import cairosvg
from PIL import Image
import xml.etree.ElementTree as ET

def add_or_modify_stroke_width(element, stroke_width):
    """Add or modify stroke-width in the style attribute."""
    style = element.get('style', '')
    if 'stroke-width' not in style:
        new_style = f'stroke-width:{stroke_width};{style}' if style else f'stroke-width:{stroke_width}'
        element.set('style', new_style)

def set_attributes_recursively(element, stroke_width):
    """Set stroke-width attribute recursively on all subelements."""
    for subelement in element.iter():
        add_or_modify_stroke_width(subelement, stroke_width)

def modify_svg(svg_file, stroke_width=".8px"):
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Modify stroke-width
    set_attributes_recursively(root, stroke_width)

    tree.write(svg_file)  # Overwrite the original SVG or write to a new file

def svg_to_png(svg_file, output_png, png_width=180):
    """Convert an SVG file to a PNG file with a specified width."""
    cairosvg.svg2png(url=svg_file, write_to=output_png, output_width=png_width)

def combine_center_align(png_file1, png_file2, output_file):
    """Combine two PNG files and center align them."""
    # Open the images
    img1 = Image.open(png_file1)
    img2 = Image.open(png_file2)

    # Calculate dimensions for the output image
    output_width = max(img1.width, img2.width)
    output_height = max(img1.height, img2.height)

    # Create a new image with the calculated dimensions
    combined_img = Image.new('RGBA', (output_width, output_height), (255, 255, 255, 0))

    # Calculate positions for center alignment
    img1_x = (output_width - img1.width) // 2
    img1_y = (output_height - img1.height) // 2
    img2_x = (output_width - img2.width) // 2
    img2_y = (output_height - img2.height) // 2

    # Paste the images onto the combined image
    combined_img.paste(img2, (img2_x, img2_y), img2 if img2.mode == 'RGBA' else None)
    combined_img.paste(img1, (img1_x, img1_y), img1 if img1.mode == 'RGBA' else None)

    # Save the combined image
    combined_img.save(output_file)

# Define file paths
svg_directory = 'source/'
export_directory = 'export/'
existing_png = 'back.png'

# Ensure export directory exists
if not os.path.exists(export_directory):
    os.makedirs(export_directory)

# Process each SVG in the directory
for filename in os.listdir(svg_directory):
    if filename.endswith(".svg"):
        svg_file = os.path.join(svg_directory, filename)
        base_name = os.path.splitext(filename)[0]
        exported_png = os.path.join(export_directory, f"{base_name}.png")
        output_png = os.path.join(export_directory, f"{base_name}.png")

        # Modify stroke-width and convert to PNG
        modify_svg(svg_file, "1.5px")  # Adjust stroke-width as needed
        svg_to_png(svg_file, exported_png)

        # Combine the exported PNG with an existing PNG
        combine_center_align(exported_png, existing_png, output_png)

        print(f"Processed and combined {filename}")
