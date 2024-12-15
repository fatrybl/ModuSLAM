"""Model for depth estimation using Hugging Face's transformers library.

Authors: https://github.com/LiheYoung/Depth-Anything
TODO: make it faster...
"""

import numpy as np
import torch
from PIL.Image import Image
from transformers import (
    AutoImageProcessor,
    AutoModelForDepthEstimation,
    is_torch_available,
)

from phd.moduslam.custom_types.numpy import MatrixMxN


class DepthEstimator:
    def __init__(self):
        model: str = "depth-anything/Depth-Anything-V2-Base-hf"
        self._unnormilized_depth = "predicted_depth"
        self._image_processor = AutoImageProcessor.from_pretrained(model)
        self._model = AutoModelForDepthEstimation.from_pretrained(model)

    def estimate_depth(self, image: Image) -> MatrixMxN:
        """Estimates depth from the image.

        Args:
            image: image to estimate depth from.

        Returns:
            estimated depth.
        """
        image_3d = np.stack((np.array(image),) * 3, axis=-1)
        inputs = self._image_processor(images=image_3d, return_tensors="pt")
        with torch.no_grad():
            outputs = self._model(**inputs)
            predicted_depth = outputs.predicted_depth

        prediction = torch.nn.functional.interpolate(
            predicted_depth.unsqueeze(1), size=image.size[::-1], mode="bicubic", align_corners=False
        )
        output = prediction.squeeze().cpu().numpy()
        return output

    @staticmethod
    def _get_device() -> int:
        """Returns the device number."""
        if is_torch_available() and torch.cuda.is_available():
            return 0
        else:
            return -1
