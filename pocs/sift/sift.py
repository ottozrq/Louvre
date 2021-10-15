import cv2 
import matplotlib.pyplot as plt

# read images
img1 = cv2.imread('imgs/effel1.jpg')  
img2 = cv2.imread('imgs/effel2.jpg') 

img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img1 = cv2.resize(img1, (200, 300))
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
img2 = cv2.resize(img2, (200, 300))

sift = cv2.SIFT_create()

keypoints_1, descriptors_1 = sift.detectAndCompute(img1,None)
keypoints_2, descriptors_2 = sift.detectAndCompute(img2,None)

print(len(keypoints_1), len(keypoints_2))
print(len(descriptors_1), len(descriptors_2))
print(descriptors_1, descriptors_2)

bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

matches = bf.match(descriptors_1,descriptors_2)
matches = sorted(matches, key = lambda x:x.distance)
print(len(matches))
print(str(matches[1]))
