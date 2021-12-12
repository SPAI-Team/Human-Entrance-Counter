from typing import Any, Dict
from peekingduck.pipeline.nodes.node import AbstractNode


class Node(AbstractNode):
    """
    A helper class to help debugging by printing the target data in pipeline.

    Inputs:
        |dataInPipe|

    Outputs:
        |none|

    Args:
        dataInPipe (:obj:`List`): 
            Keys of target data in pipeline to be printed.
            e.g. ['bboxes','bbox_labels']
        
        skipFrames (:obj:`int`): **default = 100**
            Number of frames to be skipped before printing the target data.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        super().__init__(config, node_path=__name__, **kwargs)
        assert len(self.dataInPipe) != 0, "Please enter at least one target data to be printed"
        self.curFrame = 0

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """ This node does print target data for every skipFrames.
        Args:
            inputs (dict): Dict with all keys in  "`dataInPipe`".
        Returns:
            outputs (dict): None
        """
        if self.curFrame % self.skipFrames == 0:
            print(*[inputs[data] for data in self.dataInPipe], sep=',')
        
        self.curFrame += 1
        return {}
