from pathlib import Path

from PIL import Image


def crop_edges(image_path, output_dir, crop_percentages):
    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate the number of pixels to crop from each edge
    crop_pixels_left = int(width * crop_percentages["left"] / 100)
    crop_pixels_upper = int(height * crop_percentages["upper"] / 100)
    crop_pixels_right = int(width * crop_percentages["right"] / 100)
    crop_pixels_lower = int(height * crop_percentages["lower"] / 100)

    # Define the cropping box (left, upper, right, lower)
    crop_box = (
        crop_pixels_left,  # left
        crop_pixels_upper,  # upper
        width - crop_pixels_right,  # right
        height - crop_pixels_lower,  # lower
    )

    # Crop the image
    cropped_image = image.crop(crop_box)

    # Generate the new filename
    original_name = image_path.stem
    new_filename = f"{original_name}_cropped.png"
    output_path = output_dir / new_filename

    # Save the cropped image
    cropped_image.save(output_path)


current_dir = Path(__file__).parent.absolute()
sub_dir = Path("visualization/urban-26_no_gps/output")
dir = current_dir / sub_dir

path1 = dir / "base_cloud.png"
path2 = dir / "mom_cloud.png"
path3 = dir / "timeshift_cloud.png"
path4 = dir / "error_cloud.png"

# Define the paths to your images
image_paths = [path1, path2, path3, path4]

# Define the percentage of edges to crop for each side
crop_percentages = {
    "left": 30,  # Example: crop 10% from the left edge
    "upper": 30,  # Example: crop 5% from the upper edge
    "right": 30,  # Example: crop 10% from the right edge
    "lower": 20,  # Example: crop 5% from the lower edge
}

# Crop edges for each image
for image_path in image_paths:
    crop_edges(image_path, dir, crop_percentages)
