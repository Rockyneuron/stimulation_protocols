import cv2


# Open the video file
cap = cv2.VideoCapture("data/000/world.mp4")

# Initialize the pause status and the delay between frames (in ms)
paused = False
delay = 25
frame_n=0
# Loop through the video frames
while True:
    # Check if the video is paused
    if not paused:
        # Read a frame from the video
        ret, frame = cap.read()

        # Check if the frame was successfully read
        if not ret:
            break

        # Display the frame
        cv2.imshow("Frame", frame)
        frame_n+=1
        print('current frame= {}'.format(frame_n))
        # print('delay= {}'.format(delay))
    # Wait for a key press
    key = cv2.waitKey(delay) & 0xFF

    # Check if the space bar was pressed (to pause/resume the video)
    if key == ord(' '):
        paused = not paused

    # Check if the 'q' key was pressed (to quit)
    elif key == ord('q'):
        break

# Release the video file and close the window
cap.release()
cv2.destroyAllWindows()