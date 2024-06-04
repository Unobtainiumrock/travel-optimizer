# About
Recently, I've been planning a trip to Europe and one of the stops is Barcelona. An issue that I always face when planning for travel is that whenever I have a list of places to go, I have no concept of where each are located in relation to one another. Tools like Google maps can only get you so far, and I find the interface for my specific needs to be clunky.

I decided to start the trip plans by conversing with ChatGPT and while it was able to come up with fun itineraties for my given timeframe, I didn't know if I'd have any wasted or unnecessary back-and-forth commutes. My time there is limited, so I wanted to have the most optimal ordering of locations to visit. 


## Modeling the Problem
This can be modeled by the traveling salesman problem (TSP). More specifically, I want to:

1. Start at my hotel
2. End at my hotel
3. Visit each location exactly once

## What the Tool Does
The small tool I whipped up will query the Google Maps API using a given set of GPS coordinates and get a distance matrix in return. This distance matrix is then used in conjunction with a TSP solver to minimize the total distance traveled, while adhering to my constraints.

## Next Stages
1. However convenient this may be, there's still a lot to the process that needs to be automated. Initially, I looked up addresses of places and grabbed their respective GPS coordinates. This isn't ideal for obvious reasons, so I'll need to determine if addresses can directly replace the GPS coordinates in the API query, or if I'll need to create a mapping between the two.

2. There was manual work involved in adding locations to the Google My Maps tool and drawing connecting lines between locations. I want to either find a way to integrate my code into programmatically interacting with the Google My Maps tool, or create my own UI for reasons seen in 3.

3. The current UI for this will create a polygon once you've connectd all of the destination vertices together. It's nice, but I want to add more visual information to either the vertices, edges, or both --something that visually indicates to users the order of places to hit.

4. Investigate whether or not there's a way to export these graph tours to map apps with multiple stops.

These are just a few of my immediate changes I'll make, but I'm certain more ideas will arise.

### TO DO
1. Work on next stages changes
2. Add a section to this README.md that shows screenshots of the Google My Maps tool rendering my results
3. Add screenshots of giphy's of using the app
4. Create an installation guide and HOW TO USE section (make minimal assumptions about end users)
5. Add links to: traveling salesman problem, Overleaf, Google My Maps
6. More formally state the problem in an Overleaf doc
7. Consider making a Jupyter Notebook to play with this
8. Consider writing a Medium post about it or a YouTube video
9. Code cleanup, tests, type hints
10. Make it clear that users need their own API key and to closely guard that API key.
