# Human Entrance Counter with PeekingDuck
Human Entrance Counter is a jointly-collaborated project between [SPAI](https://www.instagram.com/spai.sp/) and [SP-RITE](https://www.instagram.com/sp.riteclub/) and its aim is to detect the amount of human traffic moving in and out of a bounded region at any given time.

## Project Overview

The project utilizes [PeekingDuck](https://github.com/aimakerspace/PeekingDuck) with custom nodes for human detection and tracking along with [Express.js](https://expressjs.com/) as backend controller.

![tech-stack.png](assets/tech-stack.png)


## To-Do
### PeekingDuck Model
- [x] Implement Centroid Tracking Custom Nodes
- [x] Count Objects Based on Centroid Movement Custom Nodes
- [x] Logging of Total Individual Custom Nodes
- [x] Implement Drawing Centroid with Id Custom Nodes
- [ ] Integration of Python Scripts / Peekingduck CLI with Web Application

### Front-End Web Application
- [x] Design Wireframe for Front-End
    - Display current footfall
    - Display past statistics
    - Display camera location
    - More Features...
- [ ] Development of HTML Pages with Integration of API Services

### Back-End Web Application
- [x] Read in footfall information
- [x] Design and Implement Routing
    - homepage
    - footfall api
    - More Features...


## Software Required:
- [Anaconda](https://www.anaconda.com/products/individual)
- [git](https://git-scm.com/downloads)
- [GitHub Desktop (For those that are unfamiliar with CLI)](https://desktop.github.com/)
- [VS Code](https://code.visualstudio.com/)

## Getting Started
1. Clone the Repository by 
    - Using Git CLI
        ```
        git clone https://github.com/SPAI-Team/Human-Entrance-Counter.git
        ```
    - Use GitHub Desktop App
        - Add repository
        - Clone repository
        - Input the URL `SPAI-Team/Human-Entrance-Counter`
2. Setting Up Conda Python Environment
    ```bash
    conda create --name human-entrance python=3.8
    conda activate human-entrance
    pip install peekingduck
    ```

## Formatting for backend

```
column      format              data type       example
time        YYYYMMDDhhmmss      string          20211114102300
footfall    int                 integer         1
location    locationname        string          fc3
```
## backend queries

get /history/:location/:startTime/:endTime
- input: locationname(string), startTime(string in YYYYMMDDhhmmss), endTime(string in YYYYMMDDhhmmss)
- output: json array of records
- each record: footfallid (int), time (string in YYYYMMDDhhmmss), cuurentfootfall (int), location (string), netfootfall (int)
* note: currentfootfall = total footfall(all added together), netfootfall = footfall recorded at time of record

example:
```get /history/fc1/20211111024000/20211114130000```

output:
```
[
    {
        "footfallid": 34,
        "time": "20211114101000",
        "currentfootfall": 20,
        "location": "fc1",
        "netfootfall": 20
    },
    {
        "footfallid": 35,
        "time": "20211114111000",
        "currentfootfall": 40,
        "location": "fc1",
        "netfootfall": 20
    }
]
```


get /latest/:location
- input: locationname (string)
- output: json object with 1 record
- record has: footfallid (int), time (string in YYYYMMDDhhmmss), cuurentfootfall (int), location (string)

example:
```get /latest/fc6```

output:
```
{
    "footfallid": 33,
    "time": "20211111024500",
    "currentfootfall": 0,
    "location": "fc6"
}
```

post /history
- input: locationname(string), startTime(string in YYYYMMDDhhmmss), netfootfall (int)
- output: empty array []

example:
```post /history```

_body_:
```
time:20211114121500
netfootfall:30
location:fc1
```

output: []
