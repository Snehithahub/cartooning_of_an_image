import cv2
import numpy as np

# Function to apply pure cartoon effect
def pure_cartoonize(image_path):
    # Load the image
    image = cv2.imread(image_path)
    image = cv2.resize(image, (800, 600))  # Resize image for easier processing

    # Step 1: Edge Preserving Filter (Bilateral Filter)
    # This helps in noise reduction while preserving strong edges
    filtered = cv2.bilateralFilter(image, 9, 250, 250)

    # Step 2: Convert to Grayscale
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

    # Step 3: Detect Edges
    # Use adaptive thresholding to get strong edges
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Step 4: Color Quantization
    def color_quantization(img, k):
        data = np.float32(img).reshape((-1, 3))
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
        ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        result = center[label.flatten()]
        result = result.reshape(img.shape)
        return result

    quantized = color_quantization(filtered, 9)

    # Step 5: Combine Edges and Quantized Image
    cartoon = cv2.bitwise_and(quantized, quantized, mask=edges)

    return cartoon

# Example usage
if __name__ == '__main__':
    image_path = r'C:\Users\Chandra\Desktop\coding\tj.jpg'  # Replace with your image path
    cartoon_image = pure_cartoonize(image_path)

    # Display the images
    cv2.imshow('Original Image', cv2.imread(image_path))
    cv2.imshow('Pure Cartoon Image', cartoon_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
