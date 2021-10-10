# import the necessary packages
from typing import Any, Dict
from .utils.centroidtracker import CentroidTracker
from peekingduck.pipeline.nodes.node import AbstractNode

class Node(AbstractNode):
    """
    Assign unique ID and centroids coordinate based on input bboxes using
    Euclidean distance as update mechanism.

    Inputs:
        |img|

        |bboxes|

    Outputs:
        |trackers|

    Args:
        maxDistance (:obj:`int`): **default = 50
            max distance between centroids to assign a new centroid Id
        
        maxDisappeared (:obj:`int`): **default = 40
            max number of frame for an object to be disappeared before 
            assigning new centroid Id.
        
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
        """ This node does centroid tracking based on input bboxes.
        Args:
            inputs (dict): Dict with keys "img", "bboxes".
        Returns:
            outputs (dict): Dict with keys "trackers".
        """        
        height, width, _ = inputs['img'].shape
        
        # Make a copy of the bboxes and 
        # Rescale bboxes range from 0-1 to number of pixels
        bboxes = inputs['bboxes'].copy() 
        bboxes[:, [0,2]] *= width 
        bboxes[:, [1,3]] *= height 
        
        # Update the trackers dictionaries 
        # with Centroid Id as key and 
        # Centroid coordinates as value
        #   e.g. OrderedDict([(0, array([205, 291]))])
        trackers = self.ct.update(bboxes) 
        
        return {'trackers': trackers}
