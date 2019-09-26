from imageai.Detection import ObjectDetection
import os

def get_all_objects(image):
    execution_path = os.getcwd()

    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , image), output_image_path=os.path.join(execution_path , "imagenew.jpg"))

    return detections

detections = get_all_objects(image='downloads\AgADBAADjLIxG6X5OVDr3qJ94eQN0J1LqBsABAEAAwIAA3kAA3VpAgABFgQ.jpg')

for eachObject in detections:
    print(eachObject["name"] , " : " , eachObject["percentage_probability"])
