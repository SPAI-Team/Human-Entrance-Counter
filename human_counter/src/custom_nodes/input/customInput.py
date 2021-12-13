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
        url (:obj:`str`): **default = null**

            url to fetch http stream buffer. Raise warning if it is None.

        resize (:obj:`Dict`): **default = { do_resizing: False, width: 1280, height: 720 }**

            Dimension of extracted image frame

        frames_log_freq (:obj:`int`): **default = 100**

            Logs frequency of frames passed in cli
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        assert self.url is not None, "Source url cannot be None. Please specify a url to fetch stream buffer."
        self.bts = b''
        self.img=None
        self.CAMERA_BUFFRER_SIZE = 4096
        self.stream = urlopen(self.url, timeout=5)

        if self.resize['do_resizing']:
            self.logger.info('Resizing of input set to %s by %s',
                             self.resize['width'],
                             self.resize['height'])

        self.frame_counter = 0

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        while True:
            try:
                self.bts += self.stream.read(self.CAMERA_BUFFRER_SIZE)
                self.jpghead = self.bts.find(b'\xff\xd8')
                self.jpgend = self.bts.find(b'\xff\xd9')
                if self.jpghead > -1 and self.jpgend > -1:
                    jpg = self.bts[self.jpghead:self.jpgend+2]
                    self.bts = self.bts[self.jpgend+2:]
                    self.img = cv.imdecode(
                        np.frombuffer(jpg, dtype=np.uint8), cv.IMREAD_UNCHANGED
                    )
                    if self.resize['do_resizing']:
                        self.img = resize_image(
                            self.img,
                            self.resize['width'],
                            self.resize['height']
                        )
                    outputs = {
                        "img": self.img,
                        "pipeline_end": False
                    }
                    self.frame_counter += 1
                    if self.frame_counter % self.frames_log_freq == 0:
                        self.logger.info(
                            'Frames Processed: %s ...', self.frame_counter)
                    return outputs
            except Exception as e:
                # self.bts=b""
                # self.stream=urlopen(self.url)
                self.logger.warning("Error:" + str(e))
                outputs = {"img": None,
                           "pipeline_end": True
                }
                self.logger.warning("No video frames available for processing.")
                return outputs
