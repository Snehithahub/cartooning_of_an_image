import cv2
import numpy as np

def increase_saturation(image, saturation_scale=1.5):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = np.clip(s * saturation_scale, 0, 255).astype(np.uint8)
    hsv_enhanced = cv2.merge([h, s, v])
    bgr_enhanced = cv2.cvtColor(hsv_enhanced, cv2.COLOR_HSV2BGR)
    return bgr_enhanced

def cartoonize_frame(frame):
    # Increase saturation
    frame = increase_saturation(frame, saturation_scale=1.5)
    
    # Resize frame
    frame = cv2.resize(frame, (900, 700))
    
    # Convert to gray and resize
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resize = cv2.resize(grey, (900, 700))
    
    # Apply median blur and adaptive threshold
    smoothGrayScale = cv2.medianBlur(resize, 3)
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 9)
    
    # Apply bilateral filter
    colorImage = cv2.bilateralFilter(frame, 9, 300, 300)
    
    # Combine edges with the color image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    
    return cartoonImage

# Open the video file
video_path = r'C:\Users\Chandra\Downloads\d.mp4'
c = cv2.VideoCapture(video_path)

while True:
    isTrue, frame = c.read()
    if not isTrue:
        break
    
    # Process each frame
    cartoon_frame = cartoonize_frame(frame)
    
    # Display the processed frame
    cv2.imshow('Cartoonized Video', cartoon_frame)
    
    # Break the loop if 'd' key is pressed
    if cv2.waitKey(20) & 0xFF == ord('d'):
        break

# Release the video capture and destroy all OpenCV windows
c.release()
cv2.destroyAllWindows()
