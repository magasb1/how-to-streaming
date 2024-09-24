import cv2
import numpy as np
from collections import defaultdict
from ultralytics import YOLO


def start_stream(input_stream):

    model = YOLO("yolov10n.onnx", task="detect")
    print(model.names)

    cap = cv2.VideoCapture(input_stream)
    track_history = defaultdict(lambda: [])

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            results = model.track(frame, persist=True, conf=0.3, classes=[2,3,5,7])
            annotated_frame = results[0].plot()
            """ # Get the boxes and track IDs
            boxes = results[0].boxes.xywh.cpu()
            if results[0].boxes:
                if results[0].boxes.id is None:
                    track_ids = []
                track_ids = results[0].boxes.id.int().cpu().tolist()
                if len(track_ids) > 0:
                    # Plot the tracks
                    for box, track_id in zip(boxes, track_ids):
                        x, y, w, h = box
                        track = track_history[track_id]
                        track.append((float(x), float(y)))  # x, y center point
                        if len(track) > 30:  # retain 90 tracks for 90 frames
                            track.pop(0)

                        # Draw the tracking lines
                        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                        cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 255), thickness=2) """
            cv2.imshow("YOLOv8 Tracking", annotated_frame)
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            break
    cap.release()


# Veikamera
start_stream("https://polarislive-lh.akamaized.net/hls/live/2039440/fvn/hzDaPl9KkIbkcZFUvWFfg/master.m3u8")
#start_stream("https://play.example.com/demo_1024x576_6fps_300k/")

# Kristiansand torg
#start_stream("https://polarislive-lh.akamaized.net/hls/live/2039440/fvn/jcp1YQkJV7Zb4khPH2q8O/master.m3u8")