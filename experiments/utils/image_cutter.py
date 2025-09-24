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


def extract_sub_image(image_path, output_path, left, upper, right, lower):
    """Extracts a sub-image from the given image using the specified pixel coordinates.

    Args:
        image_path (str or Path): Path to the input image.
        output_path (str or Path): Path to save the extracted sub-image.
        left (int): The left pixel coordinate of the extraction rectangle.
        upper (int): The upper pixel coordinate of the extraction rectangle.
        right (int): The right pixel coordinate of the extraction rectangle.
        lower (int): The lower pixel coordinate of the extraction rectangle.
    """
    # Open the image
    image = Image.open(image_path)

    # Define the cropping box (left, upper, right, lower)
    crop_box = (left, upper, right, lower)

    # Crop the image
    sub_image = image.crop(crop_box)

    # Save the extracted sub-image
    sub_image.save(output_path)


current_dir = Path(__file__).parent.parent.parent.absolute()
sub_dir = Path("current_experiment")
dir = current_dir / sub_dir

path1 = dir / "lidars.png"
path2 = dir / "lidars_imu.png"
path3 = dir / "lidars_imu_gps.png"
path4 = dir / "error_cloud.png"

# Define the paths to your images
image_paths = [path1, path2, path3, path4]

# path1 = dir / "base.png"
# path2 = dir / "mom.png"

image_paths = [path1, path2, path3]

# Define the percentage of edges to crop for each side
crop_percentages = {
    "upper": 0,
    "lower": 0,
    "left": 8,
    "right": 20,
}

# Crop edges for each image
for image_path in image_paths:
    crop_edges(image_path, dir, crop_percentages)

# 150x170 pxs
# 1-st: 1820, 1000, 1970, 1170
# 2-nd: 1810, 1420, 1960, 1590

# extract_sub_image(path2, dir / "mom_sub_img_2.png", 1810, 1420, 1960, 1590)
