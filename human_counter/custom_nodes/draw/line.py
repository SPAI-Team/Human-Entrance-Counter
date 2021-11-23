from typing import Any, Dict
from peekingduck.pipeline.nodes.node import AbstractNode
from centroidtracker import CentroidTracker
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
            use a verticle line to act as barrier
    
    '''

    def __init__(self, roi = 0.5, axis_y = True, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        self.__name__ = ''
        self.roi = roi # percentage of frame
        self.axis_y = axis_y # orient of virtual line

        if config is None:
            config = {
                'input': ["img"],
                'output': ["img"]
            } 

        super().__init__(config, node_path = __name__, **kwargs)  
    
    def run(self, inputs: Dict[str, Any],trackableObjects,to,centroid) -> Dict[str, Any]:
        '''
        This node draws a line based on size of image, roi value and axis
        Args:
            inputs (dict): dict with key "img".
        Returns:
            outputs (dict): dict with key "img".
        '''
        self.__to__ = to
        self.__trackableObjects__ = trackableObjects
        self.__centroid__ = centroid


        ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
        objects = ct.update(self.__trackableObjects__)
        #trackers = []
        #trackableObjects = {}
        for (objectID, centroid) in objects.items():
            to = trackableObjects.get(objectID, None)     
        trackableObjects[objectID] = to

        text = "ID {}".format(objectID)
        cv2.putText(inputs['img'], text, (centroid[0] - 10, centroid[1] - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.circle(inputs['img'], (centroid[0], centroid[1]), 4, (255, 255, 255), -1)
        
        height, width, _ = inputs['img'].shape
        if self.axis_y:
            image = cv2.line(inputs['img'], (int(self.roi*width), 0), (int(self.roi*width), height), (0xFF, 0, 0), 5)
        else:
            image = cv2.line(inputs['img'], (0, int(self.roi * height)), (width, int(self.roi * height)), (0xFF, 0, 0), 5)
        
        return {'img': image}

    # trackableObjects[objectID] = to

    #         text = "ID {}".format(objectID)
    #         cv2.putText(image_np, text, (centroid[0] - 10, centroid[1] - 10),
    #                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    #         cv2.circle(
    #             image_np, (centroid[0], centroid[1]), 4, (255, 255, 255), -1)
        

#         # Draw ROI line
#         if x_axis:
#             cv2.line(image_np, (int(roi_position*width), 0),
#                      (int(roi_position*width), height), (0xFF, 0, 0), 5)
#         else:
#             cv2.line(image_np, (0, int(roi_position*height)),
#                      (width, int(roi_position*height)), (0xFF, 0, 0), 5)