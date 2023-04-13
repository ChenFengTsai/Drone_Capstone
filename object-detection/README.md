# Running the Tello YOLOv5 Script

This repository contains a script that allows you to use a DJI Tello drone to run object detection using the YOLOv5 model. Follow these steps to get started:

## Prerequisites

Before you can run the script, you need to make sure you have the following:

- Python 3.x
- Clone [YOLOv5 repo version 5.0](https://github.com/ultralytics/yolov5) and install dependencies by running `pip install -r requirements.txt` from within the yolov5 directory.

To install YOLOv5 version 5.0
```bash
git clone --branch v5.0 https://github.com/ultralytics/yolov5.git
```

## Running the Script

1. Clone this repository and navigate to the `tello_yolov5` directory.
2. Copy the `tello_yolov5.py` script from this repository into the yolov5 directory that you cloned earlier.
3. Connect your Tello drone to your computer using Wi-Fi.
4. Open a terminal and navigate to the `yolov5` directory.
5. Run the script by running the command `python tello_yolov5.py`.

## Troubleshooting

If you encounter errors when running the script, it may be due to version compatibility issues with PyTorch. To resolve this, try the following steps:

1. Make sure you have the latest version of PyTorch installed.
2. Try running the script with a different version of PyTorch, if available.
3. Check the YOLOv5 repository for any known issues related to PyTorch version compatibility.

If you are still unable to resolve the issue, you can try installing a specific version of PyTorch that is known to be compatible with YOLOv5. To do this, run the following command:

```bash
pip install torch==1.8.1 torchvision==0.9.1 -f https://download.pytorch.org/whl/cu111/torch_stable.html
```

This will install PyTorch version 1.8.1 and torchvision version 0.9.1, which are known to be compatible with the YOLOv5 repository. Once you have installed this version, try running the script again.

If you are still having issues, feel free to open an issue in this repository and we will try to assist you as best we can.

Happy flying!

