from typing import Any, Dict, List
from peekingduck.pipeline.nodes.node import AbstractNode


class Node(AbstractNode):
    '''
    Track coordinate of centroid and update the net-footfall of a particular interval.

    Inputs:
        |img|

        |trackers|

    Outputs:
        |footfall|

    Args:
        roi (:obj:`int`): **default=0.5
            position of virtual barrier to register individuals moving in or out
            of frame

        axis_y (:obj:`bool`): **default=True
            use a verticle line to act as the virtual barrier
    '''

    def __init__(self, roi=0.5, axis_y=True, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        self.__name__ = ''

        self.roi = roi  # Percentage of frame
        self.axis_y = axis_y  # Orient of virtual line
        self.footfall = 0  # Current Net Footfall
        self.pos_hist = dict() # Dict to record position status (IN:True, OUT:False)

        if config is None:
            config = {
                "input": ["img", "trackers"],
                "output": ["footfall"]
            }
        super().__init__(config, node_path=__name__, **kwargs)

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        '''
        This node checks the current coordinate of centroid and the past box location.
        Args:
            inputs (dict): dict with key "trackers"
        Returns:
            outputs (dict): dict with keys "footfall", 'tracker' 
        '''
        width, height, _ = inputs['img'].shape

        for centroidId, coordinates in inputs["trackers"].items():
            pastIsIn = self.pos_hist.get(centroidId, None) # Get past position history if exist
            currentIsIn = self.checkIsIn( # Obtain current position status
                coordinates,
                self.roi,
                self.axis_y,
                width,
                height
            )

            # Add status if past status does not exist
            if pastIsIn is None: 
                self.pos_hist[centroidId] = currentIsIn
                continue # Skip to next centroid
            
            # Update footfall when object leave the premises
            if pastIsIn > currentIsIn: 
                self.footfall -= 1
            # Update footfall when object enter the premises
            elif pastIsIn < currentIsIn: 
                self.footfall += 1

            # Update current position status
            self.pos_hist[centroidId] = currentIsIn 
        
        # Remove status for missing tracker
        for centroidId in self.pos_hist.copy(): # use .copy() to avoid RuntimeError
            if centroidId not in inputs["trackers"].keys():
                self.pos_hist.pop(centroidId)

        return {"footfall": self.footfall}

    def checkIsIn(self, coordinate: List[float], roi: int, axis_y: bool, width: int, height: int):
        '''
        This method checks the isIn status of a coordinate based on roi position and axis choosen.
        Args:
            coordinates (list): list with coordinate of object
            roi (int): position of virtual barrier to register individuals moving in or out of frame
            axis_y (bool): to user virticle virtual barrier or horizontal virtual barrier
            width (int): width of input frame
            height (int): height of input frame
        Returns:
            isIn (bool): boolean status on whether is the object in premises
        '''
        x_coord, y_coord = coordinate
        if axis_y:
            # Return boolean status on is x_coord beyond virtual boundary
            return True if x_coord >= roi * width else False 
        else:
            # Return boolean status on is y_coord beyond virtual boundary
            return True if y_coord >= roi * height else False
