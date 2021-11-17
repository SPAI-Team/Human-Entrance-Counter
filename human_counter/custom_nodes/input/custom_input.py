from peekingduck.pipeline.nodes.input.utils.read import VideoThread, VideoNoThread
from peekingduck.pipeline.nodes.input.utils.preprocess import resize_image
from peekingduck.pipeline.nodes.node import AbstractNode
from typing import Dict, Any
import cv2 as cv
import numpy as np
from urllib.request import urlopen
import os
import datetime
import time
import sys

# change to your ESP32-CAM ip
url = "http://192.168.137.86:81/stream"
CAMERA_BUFFRER_SIZE = 4096
stream = urlopen(url)
bts = b' '
i = 0

while True:
    try:
        bts += stream.read(CAMERA_BUFFRER_SIZE)
        jpghead = bts.find(b'\xff\xd8')
        jpgend = bts.find(b'\xff\xd9')
        if jpghead > -1 and jpgend > -1:
            jpg = bts[jpghead:jpgend+2]
            bts = bts[jpgend+2:]
            img = cv.imdecode(np.frombuffer(
                jpg, dtype=np.uint8), cv.IMREAD_UNCHANGED)
            # img=cv.flip(img,0) #>0:垂直翻轉, 0:水平翻轉, <0:垂直水平翻轉
            # h,w=img.shape[:2]
            #print('影像大小 高:' + str(h) + '寬：' + str(w))
            # img=cv.resize(img,(640,480))
            cv.imshow("a", img)
        k = cv.waitKey(1)
    except Exception as e:
        print("Error:" + str(e))
        bts = b''
        stream = urlopen(url)
        continue

    k = cv.waitKey(1)
    # 按a拍照存檔
    if k & 0xFF == ord('a'):
        cv.imwrite(str(i) + ".jpg", img)
        i = i+1
    # 按q離開
    if k & 0xFF == ord('q'):
        break
cv.destroyAllWindows()


"""
Reads a videofeed from a jpg chunk from esp-32 cam (e.g. webcam)
"""

class Node(AbstractNode):
    """Node to receive livestream as inputs.

    Inputs:
        None

    Outputs:
        |img|

        |filename|

        |pipeline_end|

        |saved_video_fps|

    Configs:
        fps_saved_output_video (:obj:`int`): **default = 10**

            FPS of the mp4 file after livestream is processed and exported.
            FPS dependent on running machine performance.

        filename (:obj:`str`):  **default = "webcamfeed.mp4"**

            Filename of the mp4 file if livestream is exported.

        resize (:obj:`Dict`): **default = { do_resizing: False, width: 1280, height: 720 }**

            Dimension of extracted image frame

        input_source (:obj:`int`): **default = 0 (for webcam)**

            Refer to `OpenCV doucmentation
            <https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#ga023786be1ee68a9105bf2e48c700294d/>`_
            for list of source stream codes

        mirror_image (:obj:`bool`): **default = False**

            Boolean to set extracted image frame as mirror image of input stream

        frames_log_freq (:obj:`int`): **default = 100**

            Logs frequency of frames passed in cli

        threading (:obj:`bool`): **default = False**

            Boolean to enable threading when reading frames from camera.
            The FPS can increase up to 30% if this is enabled for Windows and MacOS.
            This will also be supported in Linux in future PeekingDuck versions.

    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        self._allowed_extensions = ["mp4", "avi", "mov", "mkv"]
        if self.threading:
            self.videocap = VideoThread(                # type: ignore
                self.input_source, self.mirror_image)
        else:
            self.videocap = VideoNoThread(              # type: ignore
                self.input_source, self.mirror_image)

        width, height = self.videocap.resolution
        self.logger.info('Device resolution used: %s by %s', width, height)
        if self.resize['do_resizing']:
            self.logger.info('Resizing of input set to %s by %s',
                             self.resize['width'],
                             self.resize['height'])
        if self.filename.split('.')[-1] not in self._allowed_extensions:
            raise ValueError("filename extension must be one of: ",
                             self._allowed_extensions)

        self.frame_counter = 0

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.bts += self.stream.read(CAMERA_BUFFRER_SIZE)
            self.jpghead = self.bts.find(b'\xff\xd8')
            self.jpgend = self.bts.find(b'\xff\xd9')
            if self.jpghead > -1 and self.jpgend > -1:
                jpg = self.bts[jpghead:jpgend+2]
                bts = self.bts[jpgend+2:]
                img = cv.imdecode(
                    np.frombuffer(jpg, dtype=np.uint8), cv.IMREAD_UNCHANGED
                )
                if self.resize['do_resizing']:
                    img = resize_image(
                        img,
                        self.resize['width'],
                        self.resize['height']
                    )
                outputs = {
                    "img": img,
                    "pipeline_end": False,
                    "filename": self.filename,
                    "saved_video_fps": self.fps_saved_output_video
                }
                self.frame_counter += 1
                if self.frame_counter % self.frames_log_freq == 0:
                    self.logger.info('Frames Processed: %s ...',self.frame_counter)
            else:
                outputs = {"img": None,
                       "pipeline_end": True,
                       "filename": self.filename,
                       "saved_video_fps": self.fps_saved_output_video}
                self.logger.warning("No video frames available for processing.")
        except Exception as e:
            print("Error:" + str(e))
            sys.exit(1)
        return outputs
