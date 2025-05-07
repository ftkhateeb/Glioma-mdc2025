import os
import cv2
import shutil
#from histomicstk.preprocessing import color_normalization
import staintools
import numpy as np


def normalize_stain_vahadane(img: np.ndarray, target_img: str) -> np.ndarray:
    """
    Normalize the staining of an image using Vahadane method with a target image as reference.

    Parameters:
        img (np.ndarray): Source image (Hematoxylin & Eosin stained).
        target_img (np.ndarray): Target/reference image for stain normalization.

    Returns:
        np.ndarray: Stain-normalized image.
    """
    target_img = cv2.imread(target_img)
    # Convert from BGR (OpenCV) to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    target_rgb = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)

    # Initialize the StainNormalizer for the Vahadane method
    normalizer = staintools.StainNormalizer(method='vahadane')

    # Fit the normalizer with the target image
    normalizer.fit(target_rgb)

    # Transform the source image to the normalized version
    normalized_img = normalizer.transform(img_rgb)
    normalized_img_bgr = cv2.cvtColor(normalized_img, cv2.COLOR_RGB2BGR)

    return normalized_img_bgr

def apply_reinhard_normalization(img: np.ndarray, target_img_path: str) -> np.ndarray:
    """
    Applies Reinhard stain normalization using the staintools package.

    Args:
        img: The input H&E stained image (BGR).
        target_img_path: Path to the reference image.

    Returns:
        The stain-normalized image (BGR).
    """
    target_img = cv2.imread(target_img_path)
    if target_img is None:
        raise ValueError(f"Could not read target image: {target_img_path}")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    target_rgb = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)

    normalizer = staintools.ReinhardColorNormalizer()  # Use ReinhardColorNormalizer directly
    normalizer.fit(target_rgb)
    normalized_img_rgb = normalizer.transform(img_rgb)

    normalized_img_bgr = cv2.cvtColor(normalized_img_rgb, cv2.COLOR_RGB2BGR)
    return normalized_img_bgr


def apply_mackenko_normalization(img: np.ndarray, target_img: str) -> np.ndarray:
    """
    Preprocesses the image by applying Mackenko stain normalization using the staintools package.

    Parameters:
    - image_path (str): Path to the input H&E stained image.
    - target_size (tuple): The target size to resize the image (default: (224, 224)).

    Returns:
    - normalized_image (ndarray): The stain-normalized image.
    """
    target_img = cv2.imread(target_img)
    # Convert from BGR (OpenCV) to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    target_rgb = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)

    # Initialize the StainNormalizer for the Vahadane method
    normalizer = staintools.StainNormalizer(method='macenko')

    # Fit the normalizer with the target image
    normalizer.fit(target_rgb)

    # Transform the source image to the normalized version
    normalized_img = normalizer.transform(img_rgb)
    normalized_img_bgr = cv2.cvtColor(normalized_img, cv2.COLOR_RGB2BGR)
    return normalized_img_bgr


def loop_data_perform_action(perform_func, input_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for root, _, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.png')):
                input_image_path = os.path.join(root, file)
                output_image_path = os.path.join(output_path, os.path.splitext(file)[0] + '.png')


                img = cv2.imread(input_image_path)
                if img is None:
                    print(f"Could not read image: {input_image_path}")
                    continue

      
                processed_img = perform_func(img)

    
                cv2.imwrite(output_image_path, processed_img)
                print(f"Saved processed image to {output_image_path}")

def copy_json_files(input_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for root, _, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith('.json'):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_path, file)
                
                shutil.copy2(input_file_path, output_file_path)
                print(f"Copied {input_file_path} to {output_file_path}")
   

def find_most_representative_image(input_dir_path):
    intensities = []
    
    # Walk through the directory and read the files
    for root, _, files in os.walk(input_dir_path):
        for file in files:
            if file.lower().endswith((".png", ".jpg")):
                file_path = os.path.join(root, file)
                
                # Try reading the image in grayscale
                img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    intensities.append((file, img.mean()))
                else:
                    print(f"Warning: Could not read image {file_path}")
        
    # Check if intensities is empty
    if not intensities:
        raise ValueError("No valid images found in the directory.")
    
    # Calculate the mean intensity
    mean_intensity = np.mean([i[1] for i in intensities])
    
    # Find the image with the closest intensity to the mean
    closest = min(intensities, key=lambda x: abs(x[1] - mean_intensity))
    
    return closest[0]

def find_most_representative_image_color(input_dir_path):
    intensities = []
    
    for root, _, files in os.walk(input_dir_path):
        for file in files:
            if file.lower().endswith((".png", ".jpg")):
                file_path = os.path.join(root, file)
                img = cv2.imread(file_path)  # Read as color image
                if img is not None:
                    mean_color = img.mean(axis=(0, 1))  # Mean of each color channel
                    intensities.append((file, mean_color))
                else:
                    print(f"Warning: Could not read image {file_path}")
        
    if not intensities:
        raise ValueError("No valid images found in the directory.")
    
    mean_intensity = np.mean([i[1] for i in intensities], axis=0)  # Mean of color means
    
    def color_distance(x):
        return np.linalg.norm(x[1] - mean_intensity)  # Euclidean distance

    closest = min(intensities, key=color_distance)
    
    return closest[0]

def stain_normalize_with_reference(reference_image):
    """
    Returns a function that applies Macenko stain normalization using the reference image.
    """
    normalizer = Normalizer()
    normalizer.fit(reference_image)

    def apply_stain_normalization(img):
        return normalizer.transform(img)

    return apply_stain_normalization


def convert_jpg_to_png(img):
    return img


def save_json():
    return img