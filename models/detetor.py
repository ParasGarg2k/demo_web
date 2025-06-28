# detector.py
from ultralytics import YOLO
import cv2
import numpy as np

class StoreObjectDetector:
    def __init__(self, model_path='yolov8n.pt', device='cpu'):
        """
        Initialize the YOLOv8 detector.
        Args:
            model_path (str): Path to the YOLOv8 model weights.
            device (str): 'cpu' or 'cuda' for GPU.
        """
        self.model = YOLO(model_path)
        self.device = device
        self.model.to(device)

    def detect_objects(self, image: np.ndarray, conf_threshold=0.3):
        """
        Detect objects in the input image.
        Args:
            image (np.ndarray): BGR image (from OpenCV)
            conf_threshold (float): confidence score threshold
        Returns:
            List of detected objects with bounding boxes and class names.
        """
        results = self.model(image)

        detections = []
        for result in results:
            for box in result.boxes:
                conf = box.conf.cpu().numpy()[0]
                if conf < conf_threshold:
                    continue

                cls_id = int(box.cls.cpu().numpy()[0])
                bbox = box.xyxy.cpu().numpy()[0]  # [x1, y1, x2, y2]
                detections.append({
                    "bbox": bbox,
                    "confidence": conf,
                    "class_id": cls_id,
                    "class_name": self.model.names[cls_id]
                })
        return detections

if __name__ == '__main__':
    # Quick test with webcam
    cap = cv2.VideoCapture(0)
    detector = StoreObjectDetector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detector.detect_objects(frame, conf_threshold=0.4)
        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(frame, f"{det['class_name']} {det['confidence']:.2f}", (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        cv2.imshow('Store Detector', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
