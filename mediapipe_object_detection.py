
# STEP 1: Import the necessary modules.
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
MARGIN = 10  # pixels
ROW_SIZE = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
TEXT_COLOR = (255, 0, 0)  # red


def visualize(
    image,
    detection_result
) -> np.ndarray:
    """Draws bounding boxes on the input image and return it.
    Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.
    Returns:
    Image with bounding boxes.
    """
    for detection in detection_result.detections:
        # Draw bounding_box
        bbox = detection.bounding_box
        start_point = bbox.origin_x, bbox.origin_y
        end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)

        # Draw label and score
        category = detection.categories[0]
        category_name = category.category_name
        probability = round(category.score, 2)
        result_text = category_name + ' (' + str(probability) + ')'
        text_location = (MARGIN + bbox.origin_x,
                            MARGIN + ROW_SIZE + bbox.origin_y)
        cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                    FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)
    return image


def initialize_detector(model_path='efficientdet.tflite', threshold=0.5):
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.ObjectDetectorOptions(
        base_options=base_options,
        score_threshold=threshold
    )
    detector = vision.ObjectDetector.create_from_options(options)
    return detector

def detector_wrapper(object_detector, numpy_img_data):
    mp_image_obj = mp.Image(image_format=mp.ImageFormat.SRGB, data=numpy_img_data) # 不知道有無更好的轉換方法? Pillow Image -> Mediapipe Image
    detection_result = object_detector.detect(mp_image_obj)
    return detection_result


class MPObjectDetectorWrapper():
    def __init__(self, model_path='efficientdet.tflite', threshold=0.5):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.ObjectDetectorOptions(
            base_options=base_options,
            score_threshold=threshold
        )
        self.detector = vision.ObjectDetector.create_from_options(options)


    def object_detect(self, numpy_img_data):
        mp_image_obj = mp.Image(image_format=mp.ImageFormat.SRGB, data=numpy_img_data) # 不知道有無更好的轉換方法? Pillow Image -> Mediapipe Image
        detection_result = self.detector.detect(mp_image_obj)
        return detection_result        

    def visualize(self, image, detection_result) -> np.ndarray:
        """Draws bounding boxes on the input image and return it.
        Args:
        image: The input RGB image.
        detection_result: The list of all "Detection" entities to be visualize.
        Returns:
        Image with bounding boxes.
        """
        for detection in detection_result.detections:
            # Draw bounding_box
            bbox = detection.bounding_box
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            cv2.rectangle(image, start_point, end_point, TEXT_COLOR, 3)
            # Draw label and score
            category = detection.categories[0]
            category_name = category.category_name
            probability = round(category.score, 2)
            result_text = category_name + ' (' + str(probability) + ')'
            text_location = (MARGIN + bbox.origin_x,
                                MARGIN + ROW_SIZE + bbox.origin_y)
            cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                        FONT_SIZE, TEXT_COLOR, FONT_THICKNESS)
        return image



if __name__ == "__main__":
    # STEP 2: Create an ObjectDetector object.
    detector = MPObjectDetectorWrapper()

    # # STEP 3: Capture frame from camera.
    # # STEP 4: Detect objects in the upcoming frame.
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame")
            # break
    
        # # STEP 5: Process the detection result. In this case, visualize it.
        detection_result = detector.object_detect(frame)
        image_copy = np.copy(frame)
        annotated_image = detector.visualize(image=image_copy, detection_result=detection_result)
        cv2.imshow('object_detecion', annotated_image)
        if cv2.waitKey(5) == ord('q'):
            break    # 按下 q 鍵停止
    cap.release()
