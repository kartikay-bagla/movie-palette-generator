import cv2
import numpy as np

# Load video file
video_path = "rots_downsized.mp4"
cap = cv2.VideoCapture(video_path)

dom_colors = []

# Loop through frames
while True:
    # Read frame
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame for faster processing (optional)
    frame = cv2.resize(frame, (frame.shape[1] // 4, frame.shape[0] // 4))

    # Flatten frame to 1D array
    pixels = frame.reshape(-1, 3)

    # # Calculate dominant color
    # colors, counts = np.unique(pixels, axis=0, return_counts=True)
    # dominant_color = colors[np.argmax(counts)]
    # print(dominant_color)

    k = 1  # number of clusters
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(np.float32(pixels), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert center color from float to integer
    dominant_color = np.round(centers[0]).astype(int)
    dom_colors.append(dominant_color)

    # Display dominant color
    # dominant_color_display = np.zeros((100, 100, 3), dtype=np.uint8)
    # dominant_color_display[:, :] = dominant_color
    # cv2.imshow("Dominant Color", dominant_color_display)
    # cv2.imshow("Frame", frame)

    # key = cv2.waitKey(1) & 0xFF
    # if key == ord('q'):  # Quit
    #     break
    # elif key == ord('n'):  # Next frame
    #     continue

out_array = np.zeros((500, len(dom_colors), 3), dtype=np.uint8)
for i, col in enumerate(dom_colors):
    out_array[:, i, :] = col

cv2.imshow("test", out_array)

resized = cv2.resize(out_array, (1920, 540))
cv2.imshow("resized", resized)

cv2.imwrite("rots_output.png", resized)

key = cv2.waitKey(0) & 0xFF
if key == ord('q'):  # Quit
    # break

    # Release video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()
