import cv2

# Use 0 for the first camera, 1 for the second one, etc.
video_src = "test1.mp4"

# Capture video from the webcam
cap = cv2.VideoCapture(video_src)

# Create background subtractor
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=5, varThreshold=200,detectShadows=False)

ret, prev_frame = cap.read()

if not ret:
    print("Cannot read the video source")
    exit()

# Apply background subtraction to initialize prev_frame
prev_frame = bg_subtractor.apply(prev_frame)
prev_x, prev_y, prev_w, prev_h = 0, 0, 0, 0
while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Apply background subtraction
    fg_mask = bg_subtractor.apply(frame)

    # Calculate absolute difference of current frame and
    # the previous frame
    diff = cv2.absdiff(prev_frame, fg_mask)

    # Threshold the diff image so that we get the foreground
    threshold = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)[1]

    # Find contours of the threshold image
    contours, _ = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:  # Check if any contour is detected
        # Choose the contour with maximum area
        max_contour = max(contours, key=cv2.contourArea)

        # Ignore small contours based on area threshold
        if cv2.contourArea(max_contour) > 500:
            (x, y, w, h) = cv2.boundingRect(max_contour)

            # Measure the Euclidean distance between the center of the current
            # bounding box and the center of the previous bounding box
            distance = ((prev_x + prev_w / 2 - x - w / 2) ** 2 +
                        (prev_y + prev_h / 2 - y - h / 2) ** 2) ** 0.5

            # Only draw the bounding box if the distance is above a threshold
            if distance > 2:  # You might need to adjust this threshold
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Update previous bounding box
                prev_x, prev_y, prev_w, prev_h = x, y, w, h

        # Show the frame
    cv2.imshow("Video Stream", frame)

    # Set current frame as previous frame for next iteration
    prev_frame = fg_mask.copy()

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()