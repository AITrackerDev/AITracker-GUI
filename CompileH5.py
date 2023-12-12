import h5py
import numpy as np
from sklearn.model_selection import train_test_split

def split_data(input_h5_file, output_train_h5_file, output_test_h5_file, test_size=0.2, random_state=42):
    # Open the input H5 file
    with h5py.File('image_collection2023-12-07_00-59-52.h5', 'r') as h5_file:
        # Get the images and labels
        images = h5_file['images'][:]
        labels = h5_file['labels'][:]

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=test_size, random_state=random_state)

    # Create new H5 files for training and testing data
    with h5py.File(output_train_h5_file, 'w') as train_h5_file:
        train_h5_file.create_dataset('images', data=X_train)
        train_h5_file.create_dataset('labels', data=y_train)

    with h5py.File(output_test_h5_file, 'w') as test_h5_file:
        test_h5_file.create_dataset('images', data=X_test)
        test_h5_file.create_dataset('labels', data=y_test)

if __name__ == "__main__":
    # Specify the paths for input and output H5 files
    input_h5_file_path = 'image_collection2023-12-07_00-59-52.h5'
    output_train_h5_file_path = 'train_data.h5'
    output_test_h5_file_path = 'test_data.h5'

    # Split the data and create new H5 files
    split_data(input_h5_file_path, output_train_h5_file_path, output_test_h5_file_path)

    print("Data split and saved successfully.")