from PIL import Image


def crop_image_to_top(image_path, output_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Get the dimensions of the image
        width, height = img.size

        # Get two thirds width
        two_thirds_width = 3 * width // 4

        # Calculate the dimensions of the top-left quarter
        new_height = height // 15

        # Start with a height offset of 5% of the original height
        new_height_offset = 3*(height // 40)
        bottom_point = new_height + (height // 21)


        # Define the box to crop (left, upper, right, lower)
        box = (0, new_height_offset, two_thirds_width, bottom_point )

        # Crop the image
        cropped_img = img.crop(box)

        # Save the cropped image
        cropped_img.save(output_path)


def crop_image_to_second_third_row(image_path, output_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Get the dimensions of the image
        width, height = img.size

        # Get two thirds width
        left_crop = 18 * (width // 19)

        # Calculate the height of each section
        sections = height // 3

        # Topside offset
        topside_offset = sections // 10
        bottomside_offset = sections // 9

        top_point = sections + 2 * topside_offset
        bottom_point = 2 * sections - bottomside_offset

        # Define the box to crop (left, upper, right, lower)
        # The cropping box starts at the top of the second third and ends at the bottom of the image
        box = (0, top_point, left_crop, bottom_point)

        # Crop the image
        cropped_img = img.crop(box)

        # Save the cropped image in the output path
        cropped_img.save(output_path)

    print(f"Cropped image saved to {output_path}")


def crop_image_to_second_fifth_row(image_path, output_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Get the dimensions of the image
        width, height = img.size

        # Calculate the height of each section
        sections = height // 5
        width_max = 9 * width // 10

        # Topside offset
        topside_offset = 2 * sections
        bottomside_offset = 2.2 * sections

        box = (0, topside_offset, width_max, bottomside_offset)

        # Crop the image
        cropped_img = img.crop(box)

        # Save the cropped image in the output path
        cropped_img.save(output_path)

        # Remove the image file
        #os.remove(image_path)

    print(f"Cropped image saved to {output_path}")
