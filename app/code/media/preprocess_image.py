import os

import cv2

from ..utils.utils import create_temp_copy


def preprocess_image_adding_rectangles(image_path):
    temp_path = create_temp_copy(image_path)

    # Read the image in grayscale from the new path
    image = cv2.imread(temp_path, cv2.IMREAD_GRAYSCALE)

    # Check if the image was loaded properly
    if image is None:
        raise FileNotFoundError(
            f"Could not read image from {temp_path}. Please ensure the file exists and is accessible.")

    # Define rectangle properties
    rects = [
        ((0, 0), (image.shape[1] // 2, image.shape[0] // 3)),
        ((0, 0), (image.shape[1] // 5, image.shape[0])),
        ((0, image.shape[0] // 3), (image.shape[1], image.shape[0] // 3 + image.shape[0] // 3)),
    ]

    # Draw rectangles on the image
    for (top_left, bottom_right) in rects:
        cv2.rectangle(image, top_left, bottom_right, 255, thickness=cv2.FILLED)

    # Invert colors if needed
    inverted_image = cv2.bitwise_not(image)

    # Resize for better OCR accuracy
    scaled_image = cv2.resize(inverted_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Optionally remove the temporary file if you no longer need it
    os.remove(temp_path)


    return scaled_image


def preprocess_image(image_path):
    # Read the image in grayscale from the new path
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Check if the image was loaded properly
    if image is None:
        raise FileNotFoundError(
            f"Could not read image from {image_path}. Please ensure the file exists and is accessible.")
    # Invert colors if needed
    inverted_image = cv2.bitwise_not(image)
    # Resize for better OCR accuracy
    scaled_image = cv2.resize(inverted_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    return scaled_image
