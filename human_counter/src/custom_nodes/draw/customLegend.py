"""
Displays info from dabble nodes such as fps, object count and zone counts in a legend box
"""

from typing import Any, Dict, List
from peekingduck.pipeline.nodes.node import AbstractNode
from peekingduck.pipeline.nodes.draw.utils.legend import Legend
import cv2
from cv2 import FONT_HERSHEY_SIMPLEX, LINE_AA
from peekingduck.pipeline.nodes.draw.utils.constants import \
    THICK, WHITE, SMALL_FONTSCALE, BLACK, FILLED, \
    PRIMARY_PALETTE, PRIMARY_PALETTE_LENGTH


class Node(AbstractNode):
    """Draw node for drawing Legend box and info on image

    The draw legend node dynamically pulls the output results of previous nodes
    And uses it to draw the information into a legend box. Currently draws fps,
    object counts and object count in zones.

    all_legend_item: config is all possible items that can be drawn in legend box
    include: is used to select which information would be drawn
    This is so we can have the outputs but choose not to drawn on screen

    Inputs:

        all (:obj:`Any`): Receives inputs from all preceding outputs to use
        ass dynamic input for legend creation.

    Outputs:
        |none|

    Configs:
        position (:obj:`str`): **default = "bottom"**
            Position to draw legend box. "top" draws it at the top-left position
            while "bottom" draws it at bottom-left.

        include (:obj:`list`): **default = ["all_legend_items"]**
            List of information to draw. Current can draw "fps", "count" and/or
            "zone_count". The default value "all_legend_items" draws everything
            dynamically depending on inputs.
    """

    def __init__(self, config: Dict[str, Any] = None, **kwargs: Any) -> None:
        __name__ = ""
        if config is None:
            config = {
                'input': ["all"],
                'output': ["none"]
            }
        super().__init__(config, node_path=__name__, **kwargs)
        self.include = kwargs.get("include", ["all_legend_items"])
        self.position = kwargs.get("position", "bottom")
        self.all_legend_items = ['fps', 'count', 'zone_count']
        self.legend_items: List[str] = []

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Draws legend box with information from nodes

        Args:
            inputs (dict): Dict with all available keys

        Returns:
            outputs (dict): Dict with keys "none"
        """
        log_legend = Legend()

        if len(self.include) > 1:
            for legend in self.include:
                if legend not in self.all_legend_items and legend not in self.legend_items:
                    self.legend_items.append(legend)
                    def log_method(frame, y_pos, current_value): return cv2.putText(frame, "Footfall: {}".format(
                        current_value), (15 + 10, y_pos), FONT_HERSHEY_SIMPLEX, SMALL_FONTSCALE, WHITE, THICK, LINE_AA)
                    log_legend.add_register(name=legend, method=log_method)
        if self.include[0] == 'all_legend_items':  
            self.include = self.all_legend_items  
        self._include(inputs)
        if len(self.legend_items) != 0:
            log_legend.draw(inputs, self.legend_items,
                            self.position)  
            self.legend_items = []
        else:
            return {}
        # cv2 weighted does not update the referenced image. Need to return and replace.
        return {'img': inputs['img']}

    def _include(self, inputs: Dict[str, Any]) -> None:
        for item in self.all_legend_items:
            if item in inputs.keys() and item in self.include:
                self.legend_items.append(item)