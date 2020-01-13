import numpy as np
from PIL import Image
import os
import json

import torch
from torchvision import models, transforms


mean, std = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]

trnsfrm = transforms.Compose([transforms.Resize(255),
							 transforms.CenterCrop(224),
							 transforms.ToTensor(),
							 transforms.Normalize(mean, std)])

imagenet_class_index_path = open('../data/imagenet_class_index.json')
imagenet_class_index = json.load(imagenet_class_index_path)

model = models.resnet34(pretrained=True)
model.eval()


def preprocess(image):
    return trnsfrm(image).unsqueeze(0)

def predict_label(image):
	image = preprocess(image)
	output = model.forward(image)
	_, y_hat = output.max(1)
	pred_idx = str(y_hat.item())

	return imagenet_class_index[pred_idx][1]
