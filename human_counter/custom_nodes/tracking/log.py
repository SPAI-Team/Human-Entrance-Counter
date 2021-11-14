#pratik:
#the commenting for the code
#the conversion of the datetime
#amir: 
#check if request is posted
#if posted, update the timings and footfall value
#if not then print error
#amir:
import requests
from datetime import datetime
from typing import Optional, Dict, Any
from peekingduck.pipeline.nodes.node import AbstractNode

class Node(AbstractNode):
    """<WHAT THIS NODE DOES>"""
    '''This node checks the current coordinate of centroid and the past box location.
        Args:
            inputs (dict): dict with key "trackers"
        Returns:
            outputs (dict): dict with keys "footfall", 'tracker'
      '''


    def __init__(self, postIntervalTiming:int="5", endpoint:str="", config: Dict[str, Any] = None, **kwargs: Any) -> Dict[str, Any]:
        self.__name__ = ''

        self.endpoint = endpoint
        self.postIntervalTiming = postIntervalTiming #>> NEED TO DO Type Casting FROM STRING TO DATETIME FOR COMPARISON PURPOSE
        self.pastPostTiming = datetime.now()

        if config is None:
            config = {
                "input": ["footfall"],
                "output": ["footfall"]
            }
        super().__init__(config, node_path=__name__, **kwargs)
         
    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
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
# End of class Node

# POST request to the endpoint        



# defining the api-endpoint 
API_ENDPOINT = "https://spai-human-counter.herokuapp.com/"
  
# your API key here
API_KEY = ""
  
# your source code here
source_code = '''
print("Hello, world!")
a = 1
b = 2
print(a + b)
'''
  
# data to be sent to api
data = {'api_dev_key':API_KEY,
        'api_option':'paste',
        'api_paste_code':source_code,
        'api_paste_format':'python'}

# sending post request and saving response as response object
postrequest = requests.post(url = API_ENDPOINT, data = data)

# extracting response text 
endpoint_url = postrequest.text
print("The endpoint_url URL is:%s"%endpoint_url) 

#error handling
#GET request to the endpoint
try:
  r = requests.get('https://spai-human-counter.herokuapp.com/')
  r.raise_for_status()
except requests.exceptions.HTTPError as err:
   raise SystemExit(err)
#try:
#  response = requests.post(_url, files = {
#    'file': some_file
#   })
#       response.raise_for_status()
#       except requests.exceptions.HTTPError as errh:
#          return "An Http Error occurred:" + repr(errh)
#        except requests.exceptions.ConnectionError as errc:
#          return "An Error Connecting to the API occurred:" + repr(errc)
#        except requests.exceptions.Timeout as errt:
#          return "A Timeout Error occurred:" + repr(errt)
#       except requests.exceptions.RequestException as err:
#          return "An Unknown Error occurred" + repr(err)
#POST request to the endpoint
try:
  r = requests.post('somerestapi.com/post-here', data = {
   'birthday': '9/9/3999'
})
  r.raise_for_status()
except requests.exceptions.HTTPError as e:
   print(e.response.text)
