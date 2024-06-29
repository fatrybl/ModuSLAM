"""Model for depth estimation using Hugging Face's transformers library.

Authors: https://github.com/LiheYoung/Depth-Anything
TODO: make it faster...
"""

import torch
from PIL.Image import Image
from transformers import is_torch_available, pipeline

from moduslam.utils.numpy_types import MatrixMxN


class DepthEstimator:
    def __init__(self):
        model: str = "LiheYoung/depth-anything-small-hf"
        task: str = "depth-estimation"
        self._unnormilized_depth = "predicted_depth"
        device = self._get_device()
        self._pipe = pipeline(task=task, model=model, device=device)

    def estimate_depth(self, image: Image) -> MatrixMxN:
        """Estimates depth from the image.

        Args:
            image: image to estimate depth from.

        Returns:
            estimated depth.
        """
        depth = self._pipe(image)[self._unnormilized_depth].cpu().numpy().squeeze()
        return depth

    @staticmethod
    def _get_device() -> int:
        """Returns the device number."""
        if is_torch_available() and torch.cuda.is_available():
            return 0
        else:
            return -1
