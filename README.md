# Human Entrance Counter with PeekingDuck
Human Entrance Counter project is aimed to detect the amount of human traffic moving in and out of a bounded region at any given time.
The project utilizes [PeekingDuck](https://github.com/aimakerspace/PeekingDuck) with custom nodes for human detection and tracking.

### To-Do
- [x] Writing Custom Node for PeekingDuck
- [x] Centroid Tracking
- [ ] Integration with Peekingduck CLI and ensure customNode works
- [ ] count objects based on Centroid Movement and Output Total Individual in Area (Display using Legend)
- [ ] Drawing Centroid with Id using opencv
- [ ] Logging of Total Individual
- [ ] Simple GUI to display (opencv windows, bar chart of human entrace in different hour)


### Software Required:
- [Anaconda](https://www.anaconda.com/products/individual)
- [git](https://git-scm.com/downloads)

### Requirements
```bash
conda create --name human-entrance python=3.8
conda activate human-entrance
git clone https://github.com/SPAI-Team/Human-Entrance-Counter.git
pip install peekingduck
```