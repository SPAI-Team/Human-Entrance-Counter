import sys
import cv2 as cv
import numpy as np
from typing import Dict, Any
from urllib.request import urlopen
from peekingduck.pipeline.nodes.input.utils.preprocess import resize_image
from peekingduck.pipeline.nodes.node import AbstractNode


class Node(AbstractNode):
    """Reads a videofeed from a jpg chunk from esp-32 cam (e.g. webcam).

    Inputs:
        None

    Outputs:
        |img|

        |pipeline_end|

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

    def __init__(
            self, url: str, 
            resize: Dict[str, Any] = {"do_resizing": False, "width": 1280, "height": 720}, 
            config: Dict[str, Any] = None, 
            **kwargs: Any
        ) -> None:
        self.__name__ = ''
        if config is None:
            config = {
                "input": [],
                "output": ["img", "pipeline_end"]
            }
        super().__init__(config, node_path=__name__, **kwargs)
        self.url = url
        self.bts = b' '
        self.resize = resize
        self.stream = urlopen(url)
        self.CAMERA_BUFFRER_SIZE = 4096
        self.frames_log_freq = 100

        if self.resize['do_resizing']:
            self.logger.info('Resizing of input set to %s by %s',
                             self.resize['width'],
                             self.resize['height'])

        self.frame_counter = 0

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        try:
            self.bts += self.stream.read(CAMERA_BUFFRER_SIZE)
            self.jpghead = self.bts.find(b'\xff\xd8')
            self.jpgend = self.bts.find(b'\xff\xd9')
            if self.jpghead > -1 and self.jpgend > -1:
                jpg = self.bts[jpghead:jpgend+2]
                self.bts = self.bts[jpgend+2:]
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
                    self.logger.info(
                        'Frames Processed: %s ...', self.frame_counter)
            else:
                outputs = {"img": None,
                           "pipeline_end": True,
                           "filename": self.filename,
                           "saved_video_fps": self.fps_saved_output_video}
                self.logger.warning(
                    "No video frames available for processing.")
        except Exception as e:
            print("Error:" + str(e))
            sys.exit(1)

        return outputs
