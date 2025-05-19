import cv2
from ultralytics import YOLO

def run_vehicle_monitor():
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(0)
    vehicle_classes = [2, 3, 5, 7]
    VEHICLE_THRESHOLD = 5

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        results = model(frame)[0]
        vehicle_count = 0
        for box in results.boxes:
            cls_id = int(box.cls)
            if cls_id in vehicle_classes:
                vehicle_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{model.names[cls_id]}"
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if vehicle_count >= VEHICLE_THRESHOLD:
            status = "ROAD FULL"
            color = (0, 0, 255)
        else:
            status = "SPACE AVAILABLE"
            color = (0, 255, 0)

        cv2.putText(frame, f"{status} ({vehicle_count} vehicles)",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        cv2.imshow("Road Vehicle Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
