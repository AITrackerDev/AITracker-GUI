import os
import h5py
import numpy as np
from sklearn.model_selection import train_test_split

def print_image_sizes(h5_file):
    images = h5_file['images'][:]
    for i, image in enumerate(images):
        print(f"Size of image {i + 1}: {image.shape}")

def compile_data(input_h5_files, output_train_h5_file, output_test_h5_file, test_size=0.2, random_state=42):
    # Initialize empty lists to store data from multiple files
    all_images = []
    all_labels = []

    # Loop through the list of input H5 files
    for input_h5_file in input_h5_files:
        # Open each input H5 file
        with h5py.File(input_h5_file, 'r') as h5_file:
            # Print the size of each image before compilation
            print(f"Printing sizes of images in {input_h5_file}:")
            print_image_sizes(h5_file)

            # Get the images and labels
            images = h5_file['images'][:]
            labels = h5_file['labels'][:]

            # Append data from the current file to the lists
            all_images.append(images)
            all_labels.append(labels)

    # Concatenate data from all files
    images = np.concatenate(all_images, axis=0)
    labels = np.concatenate(all_labels, axis=0)

    # Split the combined data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=test_size, random_state=random_state)

    # Create a single H5 file for training data
    with h5py.File(output_train_h5_file, 'w') as train_h5_file:
        train_h5_file.create_dataset('images', data=X_train)
        train_h5_file.create_dataset('labels', data=y_train)

    # Create a single H5 file for testing data
    with h5py.File(output_test_h5_file, 'w') as test_h5_file:
        test_h5_file.create_dataset('images', data=X_test)
        test_h5_file.create_dataset('labels', data=y_test)

def process_all_h5_files(input_dir, output_train_file, output_test_file):
    # Get a list of all H5 files in the input directory
    input_h5_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.h5')]

    # Process all H5 files and compile into single training and testing H5 files
    compile_data(input_h5_files, output_train_file, output_test_file)

if __name__ == "__main__":
    # Specify the input directory containing H5 files
    input_directory = 'H5Demo'

    # Specify the output file paths for training and testing H5 files
    output_train_file_path = 'H5Demo/output_train.h5'
    output_test_file_path = 'H5Demo/output_test.h5'

    # Process all H5 files in the input directory
    process_all_h5_files(input_directory, output_train_file_path, output_test_file_path)

    print("Data split and saved successfully.")


# import h5py
# import numpy as np
# from sklearn.model_selection import train_test_split
#
# def split_data(input_h5_file, output_train_h5_file, output_test_h5_file, test_size=0.2, random_state=42):
#     # Open the input H5 file
#     with h5py.File('image_collection2023-12-07_00-59-52.h5', 'r') as h5_file:
#         # Get the images and labels
#         images = h5_file['images'][:]
#         labels = h5_file['labels'][:]
#
#         # Split the data into training and testing sets
#         X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=test_size, random_state=random_state)
#
#     # Create new H5 files for training and testing data
#     with h5py.File(output_train_h5_file, 'w') as train_h5_file:
#         train_h5_file.create_dataset('images', data=X_train)
#         train_h5_file.create_dataset('labels', data=y_train)
#
#     with h5py.File(output_test_h5_file, 'w') as test_h5_file:
#         test_h5_file.create_dataset('images', data=X_test)
#         test_h5_file.create_dataset('labels', data=y_test)
#
# if __name__ == "__main__":
#     # Specify the paths for input and output H5 files
#     input_h5_file_path = 'image_collection2023-12-07_00-59-52.h5'
#     output_train_h5_file_path = 'train_data.h5'
#     output_test_h5_file_path = 'test_data.h5'
#
#     # Split the data and create new H5 files
#     split_data(input_h5_file_path, output_train_h5_file_path, output_test_h5_file_path)
#
#     print("Data split and saved successfully.")