All three things 
1. haarcascade_frontalface_default.xml
2. model.h5
3. standalone_.py
Should be in same directory 

To run a video feed instead of Camera input replace 
cap = cv2.VideoCapture(0)
with
cap = cv2.VideoCapture('Address of Video') 
in standalone_.py

Press 'q' to exit. 

requirements 
numpy==1.17.4
opencv-python==4.1.2.30
tensorflow==2.1.2
