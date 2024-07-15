import cv2
import time
import math

# Placeholder function to load a pre-trained detection model
def load_drone_detection_model():
    # This is a placeholder. Replace with actual model loading code.
    print("Loading drone detection model...")

# Placeholder function to detect a drone in the frame
def detect_drone(frame):
    # This is a placeholder. Replace with actual detection logic.
    # For testing, let's assume we detect a drone at the center of the frame.
    height, width = frame.shape[:2]
    bbox = (width // 2 - 50, height // 2 - 50, 100, 100)
    return bbox

# Function to list available cameras
def list_cameras():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

def calculate_distance(speed_kmph, time_seconds):
    # Assuming speed is constant and converting km/h to m/s
    speed_mps = speed_kmph * 1000 / 3600
    return speed_mps * time_seconds

def main():
    available_cameras = list_cameras()
    if len(available_cameras) < 1:
        print("No cameras found.")
        return

    print("Available camera indices:", available_cameras)

    cam_index = available_cameras[0]  # Use the first available camera index
    cam = cv2.VideoCapture(cam_index)

    model = load_drone_detection_model()

    start_time = time.time()
    drone_speed_kmph = 60  # Placeholder for drone speed in km/h

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        bbox = detect_drone(frame)
        if bbox:
            x, y, w, h = bbox

            # Calculate the time elapsed since the drone started flying
            time_elapsed = time.time() - start_time

            # Calculate the distance the drone has traveled
            distance_traveled = calculate_distance(drone_speed_kmph, time_elapsed)

            # Display the bounding box and information
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Distance: {distance_traveled:.2f}m", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.putText(frame, f"Speed: {drone_speed_kmph}km/h", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
