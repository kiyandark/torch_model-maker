import os.path
import argparse
import imutils
import time
import cv2
import json
from flask import Flask,request,Response
import uuid
import numpy as np
import base64

# construct the argument parser and parse the arguments
    #ap = argparse.ArgumentParser()
    #ap.add_argument("-m", "--model", required=True,
    #	help="neural style transfer model")
    #ap.add_argument("-i", "--image", required=True,
    #    help="input image to apply neural style transfer to")
    #args = vars(ap.parse_args())

    # load the neural style transfer model from disk
    #print("[INFO] loading style transfer model...")
net = cv2.dnn.readNetFromTorch("models/trained/mosaic.t7")
with open("gambar/1.jpg", "rb") as imgfi:
    img = base64.b64encode(imgfi.read())

    # load the input image, resize it to have a width of 600 pixels, and
    # then grab the image dimensions
    #image = cv2.imread(img)
image = img.write(str.decode('base64'), "wb")
image = imutils.resize(img, width=600)
(h, w) = image.shape[:2]

    # construct a blob from the image, set the input, and then perform a
    # forward pass of the network
blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
    (103.939, 116.779, 123.680), swapRB=False, crop=False)
net.setInput(blob)
start = time.time()
output = net.forward()
end = time.time()

    # reshape the output tensor, add back in the mean subtraction, and
    # then swap the channel ordering
output = output.reshape((3, output.shape[2], output.shape[3]))
output[0] += 103.939
output[1] += 116.779
output[2] += 123.680
    #output /= 255.0
output = output.transpose(1, 2, 0)
output = np.clip(output, 0, 255)
    #output= output.astype("uint8")

    # show information on how long inference took
    #print("[INFO] neural style transfer took {:.4f} seconds".format(
    #    end - start))

    # save file
path_file = ("app/static/&s.jpg" %uuid.uuid4().hex)
cv2.imwrite(path_file, output)
    #cv2.imshow("Input", image)
    #cv2.imshow("Output", output)
    #cv2.waitKey(0)