'''
This file is for cropping images from a camera feed to the necessary size for the input to our neural network.
'''
import cv2
import numpy as np
import dlib
import os

landmark_path = os.path.join('assets', 'shape_predictor_68_face_landmarks.dat')

EYES_DETECTOR = dlib.get_frontal_face_detector()
LANDMARK_PREDICTOR = dlib.shape_predictor(landmark_path)
IMAGE_SIZE = (190, 80)

# takes the image, crops the eyes, puts it into the template, resizes to our network's image input size      
def network_image_crop(image):
    # grayscale image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # dlib face and landmarks
    faces = EYES_DETECTOR(gray)
    
    # if a face is detected
    if len(faces) > 0:
        landmarks = LANDMARK_PREDICTOR(gray, faces[0])
        pad = 5
        
        left_eye = (
            #left width, top height
            landmarks.part(36).x - pad, landmarks.part(37).y - pad,
            #right width, bottom height
            landmarks.part(39).x + pad, landmarks.part(41).y + pad
        )
        
        right_eye = (
            #left width, top height
            landmarks.part(42).x - pad, landmarks.part(43).y - pad,
            #right width, bottom height
            landmarks.part(45).x + pad, landmarks.part(47).y + pad
        )
        
        # get separate images for each eye
        # [start_y:end_y, start_x:end_x]
        left_eye_region = gray[left_eye[1]:left_eye[3], left_eye[0]:left_eye[2]]
        right_eye_region = gray[right_eye[1]:right_eye[3], right_eye[0]:right_eye[2]]
        
        # put eyes into template similar to our training data
        template = eye_template(left_eye_region, right_eye_region)
        
        # return resized image and true indicating it can be used for input in our network
        return (cv2.resize(template, IMAGE_SIZE), True)
    
    # if no faces are found return original image and false
    return (image, False)

# makes the template with the regions specified by cropping the eyes
def eye_template(left_eye, right_eye):
    # composite image height and width
    height = max(left_eye.shape[0], right_eye.shape[0])
    width = left_eye.shape[1] + right_eye.shape[1]

    # create a blank image to put data into
    composite_image = np.zeros((height, width), dtype=np.uint8)

    # put left and right eyes in the image side by side
    composite_image[:left_eye.shape[0], :left_eye.shape[1]] = left_eye
    composite_image[:right_eye.shape[0], left_eye.shape[1]:] = right_eye

    # return the composite image
    return composite_image