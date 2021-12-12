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
        roi (:obj:`int`): **default=0.5
            position of barrier to draw the divider line

        axis_y (:obj:`bool`): **default=True
            use a vertical line to act as barrier
    
    '''

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path = __name__, **kwargs)  

    
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        '''
        This node draws a line based on size of image, roi value and axis
        Args:
            inputs (dict): dict with key "img".
        Returns:
            outputs (dict): dict with key "img".
        '''
        height, width, _ = inputs['img'].shape
        if self.axis_y:
            image = cv2.line(inputs['img'], (int(self.roi*width), 0), (int(self.roi*width), height), (0xFF, 0, 0), 5)
        else:
            image = cv2.line(inputs['img'], (0, int(self.roi * height)), (width, int(self.roi * height)), (0xFF, 0, 0), 5)
        
        return {'img': image}