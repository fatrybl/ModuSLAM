from pathlib import Path

from kiss_icp.datasets import dataset_factory
from kiss_icp.datasets.mulran import MulranDataset
from kiss_icp.pipeline import OdometryPipeline

data_dir = Path("/home/mark/Downloads/mulran/DCC01")
data_loader = MulranDataset(data_dir=data_dir)


pipeline = OdometryPipeline(
    dataset=dataset_factory(
        dataloader="mulran",
        data_dir=data_dir,
    ),
    deskew=True,
    max_range=120,
    visualize=True,
)
pipeline.visualizer.global_view = True
pipeline._run_pipeline()
