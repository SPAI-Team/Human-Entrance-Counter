from typing import Any, Dict
from peekingduck.pipeline.nodes.node import AbstractNode
import cv2

class Node(AbstractNode):
    '''
    Draw the centroid and id for every object tracked to the image

    Inputs:
        |img|

        |trackers|

    Outputs:
        |img|
    '''

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path = __name__, **kwargs)  
    
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        '''
        This node draws the centroid and id for every tracker assigned
        Args:
            inputs (dict): dict with key "img" and "trackers".
        Returns:
            outputs (dict): dict with key "img".
        '''
        for (objectID, centroid) in inputs["trackers"].items():
            text = "ID {}".format(objectID)
            cv2.putText(inputs['img'], text, (centroid[0] - 10, centroid[1] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2
            )
            cv2.circle(inputs['img'], (centroid[0], centroid[1]), 4, (255, 255, 255), -1)
        
        return {'img': inputs['img']}
