import requests
from typing import Any, Dict, List
from datetime import datetime, timedelta
from peekingduck.pipeline.nodes.node import AbstractNode


class Node(AbstractNode):
    '''
    Track coordinate of centroid and update the net-footfall of a particular interval.
    *Additionally, the node can also creates a Post request of the accumulated net-footfall 
    to an API Server after every defined interval.

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

        endpoint (:obj:`str`): **default=None
            Url link to send Post request of net-footfall

        postIntervalTiming (:obj:`int`): **default=5
            Interval to send a Post request counted in minutes (i.e. default parameter will send a post request every 5 minutes)

        location (:obj:`str`): **default=fc6
            Unique location name which the API Server receives
    '''

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        if self.endpoint is not None:  # If an endpoint is provided
            # Initialize pastPostTiming and postInterval
            self.pastPostTiming = datetime.now()
            self.currentTiming = datetime.now()
            self.postInterval = timedelta(minutes=self.postIntervalTiming)
        self.footfall = 0  # Current Net Footfall
        self.pos_hist = dict()  # Dict to record position status (IN:True, OUT:False)

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        '''
        This node checks the current coordinate of centroid and the past box location.
        Args:
            inputs (dict): dict with key "trackers"
        Returns:
            outputs (dict): dict with keys "footfall", 'tracker' 
        '''
        height, width, _ = inputs['img'].shape

        for centroidId, coordinates in inputs["trackers"].items():
            # Get past position history if exist
            pastIsIn = self.pos_hist.get(centroidId, None)
            currentIsIn = self.checkIsIn(  # Obtain current position status
                coordinates,
                self.roi,
                self.axis_y,
                width,
                height
            )

            # Add status if past status does not exist
            if pastIsIn is None:
                self.pos_hist[centroidId] = currentIsIn
                continue  # Skip to next centroid

            # Update footfall when object leave the premises
            if pastIsIn > currentIsIn:
                self.footfall -= 1
            # Update footfall when object enter the premises
            elif pastIsIn < currentIsIn:
                self.footfall += 1

            # Update current position status
            self.pos_hist[centroidId] = currentIsIn

        # Remove status for missing tracker
        for centroidId in self.pos_hist.copy():  # use .copy() to avoid RuntimeError
            if centroidId not in inputs["trackers"].keys():
                self.pos_hist.pop(centroidId)

        # Check on whether to send post request if required
        if self.endpoint is not None:
            self.currentTiming = datetime.now()
            if self.currentTiming >= (self.pastPostTiming + self.postInterval):
                self.sendPostRequest(
                    endpoint=self.endpoint,
                    strftime=self.currentTiming.strftime("%Y%m%d%H%M%S"),
                    location=self.location
                )

        return {"footfall": self.footfall}

    def checkIsIn(self, coordinate: List[float], roi: int, axis_y: bool, width: int, height: int) -> bool:
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

    def sendPostRequest(self, endpoint: str, strftime: str, location: str) -> None:
        '''
        This method send a post request to the endpoint provided along with different footfall informations 
        for the API.

        Args:
            endpoint (str): Url to the API Server receiving post request
            strftime (str): String of time formatted as YYYYMMDDHHMMSS
            location (str): Unique location name which the API Server receives
        '''

        # Send post request
        response = requests.post(
            endpoint,
            json={
                "time": strftime,
                "netfootfall": self.footfall,
                "location": location
            }
        )

        # Reset the footfall value if the post request succeeded
        if response.status_code == 200:
            self.logger.info(
                f"> Post request Sent Successfully at {self.currentTiming.strftime('%Y/%m/%d | %H:%M:%S')}")
            self.footfall = 0
            self.pastPostTiming = datetime.now()
        # Else print out the error
        else:
            self.logger.warning("An Error occurred during the Post request. Please contact the administrator for more information.")
