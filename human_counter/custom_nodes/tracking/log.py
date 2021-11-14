import time
import requests
from datetime import datetime
from typing import Optional, Dict, Any
from peekingduck.pipeline.nodes.node import AbstractNode

class Node(AbstractNode):
    """<WHAT THIS NODE DOES>"""
    def __init__(self, postIntervalTiming:int="5", endpoint:str="", config: Dict[str, Any] = None, **kwargs: Any) -> Dict[str, Any]:
        self.__name__ = ''

        self.endpoint = endpoint
        self.postIntervalTiming = postIntervalTiming #>> NEED TO DO Type Casting FROM STRING TO DATETIME FOR COMPARISON PURPOSE
        self.pastPostTiming = datetime.now()

        if config is None:
            config = {
                "input": ["footfall"],
                "output": ["footfall"]7/ 
            }
        super().__init__(config, node_path=__name__, **kwargs)
         
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Method that draws the count on the top left corner of image
        
         Args:
             inputs (dict): Dict with keys "count".
         Returns:
             outputs (dict): None
         """
        current_footfall = inputs["footfall"]
        current_time = datetime.now().strftime("%H:%M:%S")
        
        if current_time >= (self.pastPostTiming + self.pastPostTiming):
            response = requests.post(
                self.endpoint, 
                data={
                    "footfall": inputs['footfall']
                }
            )
            ###### Check if the request has been posted successfully
            ###### if request posted, 
            ###### >> update the pastPostTiming
            ###### >> update the footfall value ( current_footfall = 0)

            ###### if not posted, print out error message
            
            pastPostTiming = self.postIntervalTiming + current_time

        return {"footfall": current_footfall}
