import os
import cv2
import shutil
import staintools


def preprocess_pipeline(input_path, output_path) :
    if not os.path.exists(output_path):
        os.makedirs(output_path)  

    for root, _, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith('.png'):
                input_image_path = os.path.join(root, file)
                output_image_path = os.path.join(output_path, os.path.splitext(file)[0] + '.png')

                img = cv2.imread(input_image_path)
                if img is None:
                    print(f"Could not read image: {input_image_path}")
                    continue


                proprocessed_img = stain_normalizatioon(img)
                proprocessed_img = resize_image(img, 1024, 1024)
                preprocessed_img = crop_image(img, json_file_path)
                proprocessed_img = resize_image(img, 224, 224)
                preprocessed_img = normalize_image(img)
                preprocessed_img = standaradize_image(img)


                



    cv2.imwrite(output_image_path, processed_img)
    print(f"Saved processed image to {output_image_path}")


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