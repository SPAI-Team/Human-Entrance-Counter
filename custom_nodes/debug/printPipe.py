from typing import Any, Dict
from peekingduck.pipeline.nodes.node import AbstractNode


class Node(AbstractNode):
    """
    A helper class to help debugging by visualising the target data in pipeline.

    Args:
        targetData (:obj:`List`): 
            Keys of target data in pipeline to be printed.
            e.g. ['bboxes','bbox_labels']
        
        skipFrames (:obj:`int`):
            Number of frames to be skipped before printing the target data.
        
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        self.__name__ = ''
        self.curFrame = 0
        self.targetData = kwargs["targetData"]
        self.skipFrames = kwargs["skipFrames"]
        assert len(self.targetData) != 0, "Please enter at least one target data to be printed"

        if config is None:
            config = {
                "input": [*self.targetData],
                "output": ["none"]
            }
        super().__init__(config, node_path=__name__, **kwargs)
        

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:  # type: ignore
        """ This node does ___.
        Args:
            inputs (dict): Dict with keys "__", "__".
        Returns:
            outputs (dict): Dict with keys "__".
        """
        if self.curFrame % self.skipFrames == 0:
            print(*[inputs[target] for target in self.targetData], sep=',')
        
        self.curFrame += 1
        return {}
