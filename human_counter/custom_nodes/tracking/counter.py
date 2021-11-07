from typing import Any, Dict
from .tracker import Node as imNode
from peekingduck.pipeline.nodes.node import AbstractNode

class Node(AbstractNode):
    '''
    Track coordinate of centroid and update the net-footfall of a particular interval.

    Inputs:
        |ROI position|
        
        |video axis|
        
        |trackers|
    
    Outputs:
        |footfall|
        
        |tracker|
    '''
    def __init__(self, roi, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        self.__name__ = ''
        self.roi = roi
        if config is None:
            config = {
                "input": ['img', 'trackers'],
                "output": ["footfall", "box_location"]
            }
        super().__init__(config, node_path = __name__, **kwargs)
        

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        '''
        This node checks the current coordinate of centroid and the past box location.
        Args:
            inputs (dict): dict with key 'img', 'trackers'
        Returns:
            outputs (dict): dict with keys 'footfall', 'tracker' 
        '''
        x_axis, y_axis, _ = inputs['img'].shape
        poi = {'x_axis': x_axis * self.roi, 'y_axis' : y_axis}

        counter = 0
        
        for i in inputs['trackers'].keys():
            if 'is_in' in inputs['trackers'][i].keys():
                if (inputs['trackers'][i]['coordinate'][0] > poi['x_axis'] and inputs['trackers'][i]['is_in'] == False):
                    counter += 1
                    inputs['trackers'][i]['is_in'] = True
                elif (inputs['trackers'][i]['coordinate'][0] < poi['x_axis'] and inputs['trackers'][i]['is_in'] == True):
                    counter -= 1
                    inputs['trackers'][i]['is_in'] = False
            
            else:
                if (inputs['trackers'][i]['coordinate'][0] > poi['x_axis']):
                    counter += 1
                    inputs['trackers'][i]['is_in'] = True
                elif (inputs['trackers'][i]['coordinate'][0] < poi['x_axis']):
                    inputs['trackers'][i]['is_in'] = False

        return {'footfall': counter, 'tracker': inputs['trackers']}