from typing import Any, Dict
from peekingduck.pipeline.nodes.node import AbstractNode
import cv2


class Node(AbstractNode):
    '''
    Add a line to the image that separates an image into two sections

    Inputs:
        |img|

    Outputs:
        |img|

    Args:
        rotate (:obj:`int`): **default=0
            rotate the image frames clockwise in degree. Currently
            only accept 0, 90, 180 and 270 as valid arguments.
    '''

    def __init__(self, rotation: int = 0, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        __name__ = ""
        if config is None:
            config = {
                'input': ["img"],
                'output': ["img"]
            }
        super().__init__(config, node_path=__name__, **kwargs)
        if rotation not in (0, 90, 180, 270):
            raise ValueError(
                "Rotate node only accept 0, 90, 180 and 270 as valid arguments")
        self.rotation = rotation
        self.rotation_policy = {
            0: None,
            90: cv2.ROTATE_90_CLOCKWISE,
            180: cv2.ROTATE_180,
            270: cv2.ROTATE_90_COUNTERCLOCKWISE
        }

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        '''
        This node draws a line based on size of image, roi value and axis
        Args:
            inputs (dict): dict with key "img".
        Returns:
            outputs (dict): dict with key "img".
        '''
        if self.rotation != 0:
            return {'img': cv2.rotate(inputs["img"], self.rotation_policy[self.rotation])}
        else:
            return {'img': inputs["img"]}
