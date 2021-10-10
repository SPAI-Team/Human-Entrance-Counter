# import the necessary packages
from typing import Any, Dict
from .utils.centroidtracker import CentroidTracker
from peekingduck.pipeline.nodes.node import AbstractNode

class Node(AbstractNode):
    """
    ===.

    Args:
        targetData (:obj:`List`): 
            Keys of target data in pipeline to be printed.
            e.g. ['bboxes','bbox_labels']
        
        skipFrames (:obj:`int`):
            Number of frames to be skipped before printing the target data.
        
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        self.__name__ = ''
        if config is None:
            config = {
                "input": ["img","bboxes"],
                "output": ["trackers"]
            }
        super().__init__(config, node_path=__name__, **kwargs)

        #Initalise Centroid Tracker
        self.ct = CentroidTracker(
                            maxDistance=kwargs.get('maxDistance', 50),
                            maxDisappeared=kwargs.get('maxDisappeared', 40)
                        ) 
        

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  
        """ This node does ___.
        Args:
            inputs (dict): Dict with keys "__", "__".
        Returns:
            outputs (dict): Dict with keys "__".
        """        
        height, width, _ = inputs['img'].shape
        
        # Bounding Box Preprocessing
        # Make a copy of the bboxes and Rescale input range from 0-1 
        # to No. pixels
        bboxes = inputs['bboxes'].copy() 
        bboxes[:, [0,2]] *= width 
        bboxes[:, [1,3]] *= height 
        
        # Obtain output dictionary with Id as key, 
        # centroid coordinates as value
        trackers = self.ct.update(bboxes) 
        
        return {'trackers': trackers}
