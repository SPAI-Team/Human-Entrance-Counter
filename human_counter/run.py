import click
import peekingduck
from peekingduck.runner import Runner
from peekingduck.pipeline.nodes.input import live
from peekingduck.pipeline.nodes.model import yolo
from peekingduck.pipeline.nodes.draw import bbox, blur_bbox
from peekingduck.pipeline.nodes.dabble import fps
from peekingduck.pipeline.nodes.output import media_writer, screen
from custom_nodes.input import custom_input
from custom_nodes.dabble import tracker, counter, printPipe
from custom_nodes.draw import customLegend, rotate, line, drawCentroid
assert peekingduck.__version__ == 'v1.1.1' , "Peekingduck is not Updated to the latest version. Run `pip install -U peekingduck` to update your peekingduck version."

@click.command()
@click.option(
    "--source",
    "-s",
    default=None
)
@click.option(
    "--rotation",
    "-r",
    type=click.Choice(["0", "90", "180", "270"]),
    default="0"
)
@click.option(
    "--blur",
    "-b",
    is_flag=True,
    default=False
)
def main(source:str, rotation:int, blur:bool) -> None:
    click.echo(source)

    # Input Nodes
    input_node = live.Node(
        input_source = source if source else 0,
        # resize = dict(do_resizing=True, width=480, height=480),
        threading= True
    )
    # input_node = custom_input.Node(url = source)

    # Model Nodes
    yolo_node = yolo.Node(
        detect_ids =[0], # detect human for 0
        )
    
    # Dabble Nodes
    fps_node = fps.Node(fps_log_display=True)
    tracker_node = tracker.Node(maxDisappeared = 60)
    counter_node = counter.Node(
        endpoint = "https://spai-human-counter-backend-api.herokuapp.com/history/"
    )
    
    # Draw Nodes
    output_node = screen.Node()
    draw_bbox_node = bbox.Node()
    blur_bbox_node = blur_bbox.Node()
    rotate_node = rotate.Node(rotation=int(rotation))
    legend_node = customLegend.Node(position="top",include=["fps", "footfall"])
    roi_node = line.Node()
    draw_centroid_node = drawCentroid.Node()

    print("Peekingduck is Running")
    nodes = [
        input_node,
        rotate_node, 
        yolo_node, 
        tracker_node,
        counter_node,
        fps_node,
        draw_bbox_node,
        legend_node,
        blur_bbox_node,
        roi_node,
        draw_centroid_node,
        output_node
    ]
    if not blur: # remove blur node if not specified
        nodes.pop(-4)
    Runner(nodes=nodes).run()

if __name__ == "__main__":
    main()