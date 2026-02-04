---
tags:
- ultralyticsplus
- yolov8
- ultralytics
- yolo
- vision
- object-detection
- pytorch
- awesome-yolov8-models
- plant classification
- plant detection
- leaf classification
- leaf detection
- crop detection
- disease detection
library_name: ultralytics
library_version: 8.0.43
inference: False
model-index:
- name: foduucom/plant-leaf-detection-and-classification
  results:
  - task:
      type: object-detection
    metrics:
    - type: precision
      value: 0.946
      name: mAP@0.5(box)
language:
- en
metrics:
- accuracy
---
Below is the Model Card for the YOLOv8s Leaf Detection and Classification model:

---
<p align="center">
<!-- Smaller size image -->
<img src="https://huggingface.co/foduucom/plant-leaf-detection-and-classification/resolve/main/thumbnail.jpg" alt="Image" style="width:500px; height:300px;">
</p>
# Model Card for YOLOv8s Leaf Detection and Classification

## Model Summary

The YOLOv8s Leaf Detection and Classification model is an object detection model based on the YOLO (You Only Look Once) framework. It is designed to detect and classify various types of leaves in images. The model has achieved a precision (mAP@0.5) of 0.946 on the object detection task.

## Model Details

### Model Description

The YOLOv8s Leaf Detection and Classification model is built on the YOLOv8 architecture, which is known for its real-time object detection capabilities. This specific model has been trained to recognize and classify different types of leaves from various plant species. It can detect multiple leaf instances in an image and assign them to their respective classes.

```
['ginger', 'banana', 'tobacco', 'ornamaental', 'rose', 'soyabean', 'papaya', 'garlic', 'raspberry', 'mango', 'cotton', 'corn', 'pomgernate', 'strawberry', 'Blueberry', 'brinjal', 'potato', 'wheat', 'olive', 'rice', 'lemon', 'cabbage', 'gauava', 'chilli', 'capcicum', 'sunflower', 'cherry', 'cassava', 'apple', 'tea', 'sugarcane', 'groundnut', 'weed', 'peach', 'coffee', 'cauliflower', 'tomato', 'onion', 'gram', 'chiku', 'jamun', 'castor', 'pea', 'cucumber', 'grape', 'cardamom']
```
- **Developed by:** FODUU AI
- **Model type:** Object Detection
- **Language(s) (NLP):** English
  
Furthermore, the YOLOv8s Leaf Detection and Classification model encourages user collaboration by allowing them to contribute their own plant leaf data. Users can submit images of new plant species, and suggest plant names for classification. Our team will diligently work to incorporate these new plant classes into the model, enhancing its ability to identify and classify an even wider variety of plant leaves.
Users are invited to actively participate in expanding the YOLOv8s Leaf Detection and Classification model's capabilities by sharing their plant names and corresponding dataset links through our community platform or by emailing the information to info@foduu.com. Your contributions will play a crucial role in enriching the model's knowledge and recognition of diverse plant species.

## Uses

### Direct Use

The YOLOv8s Leaf Detection and Classification model can be used directly for object detection tasks related to leaf detection and classification. It does not require fine-tuning or integration into a larger ecosystem or application.

### Downstream Use 

The model can also be fine-tuned for specific leaf detection and classification tasks or integrated into a larger application for plant-related research, agriculture, or environmental monitoring.

### Out-of-Scope Use

The model is not designed for unrelated tasks or object detection scenarios outside the scope of leaf detection and classification.

## Bias, Risks, and Limitations

The YOLOv8s Leaf Detection and Classification model may have some limitations and biases:

- The model's performance may vary depending on the quality and diversity of the training data.
- It may struggle with detecting leaves that are heavily occluded or overlapping with other objects.
- The model's accuracy may be affected by variations in lighting conditions, image quality, and resolution.
- It may not accurately detect very small or distant leaves in images.
- The model's classification accuracy may be lower for leaf species that resemble each other closely.
- The model's biases may stem from the biases present in the training data.

### Recommendations

Users (both direct and downstream) should be made aware of the risks, biases, and limitations of the model. Further research and experimentation are recommended to assess its performance in specific use cases and domains.

## How to Get Started with the Model

To get started with the YOLOv8s Leaf Detection and Classification model, follow these steps:

1. Install [ultralyticsplus](https://github.com/fcakyon/ultralyticsplus) and [ultralytics](https://github.com/ultralytics/ultralytics) libraries using pip:

```bash
pip install ultralyticsplus==0.0.28 ultralytics==8.0.43

```

2. Load the model and perform prediction using the provided code snippet.

```python
from ultralyticsplus import YOLO, render_result

# load model
model = YOLO('foduucom/plant-leaf-detection-and-classification')

# set model parameters
model.overrides['conf'] = 0.25  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # maximum number of detections per image


# set image
image = 'path/to/your/image'

# perform inference
results = model.predict(image)

# observe results
print(results[0].boxes)
render = render_result(model=model, image=image, result=results[0])
render.show()
```

## Training Details


### Training Data

The model is trained on hundreds of images of 46 different plants, including both disease-infected and healthy leaves.

### Training Procedure

The training process involves using high GPU capacity and is run for up to 50 epochs, where each epoch represents a complete pass through the entire training dataset, adjusting model weights to minimize the classification loss and optimize the performance.

#### Metrics

- mAP@0.5 (box): 
0.946

#### Summary

YOLOv8s is a powerful convolutional neural network tailored for leaf detection and classification of over 46 plant species. It leverages a modified CSPDarknet53 backbone, self-attention mechanism, and a feature pyramid network for accurate multi-scaled object detection, providing precise identification and classification of plant leaves.

### Model Architecture and Objective

YOLOv8 architecture utilizes a modified CSPDarknet53 as its backbone with 53 convolutional layers and cross-stage partial connections for improved information flow. The head consists of convolutional and fully connected layers for predicting bounding boxes, objectness scores, and class probabilities. It incorporates a self-attention mechanism and a feature pyramid network for multi-scaled object detection, enabling focus on relevant image features and detecting objects of different sizes.

### Compute Infrastructure

#### Hardware

NVIDIA A100 40GB GPU card

#### Software
Jupyter Notebook environment for model training.

## Model Card Contact

info@foduu.com
```bibtex
@ModelCard{
  author    = {Nehul Agrawal and
               Pranjal singh Thakur},
  title     = { YOLOv8s Leaf Detection and Classification},
  year      = {2023}
}
```
---