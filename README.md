# path-finding

Finds smallest path between 2 points in a grid using A* Algorithm

<p align="center">
  <img alt="demo" height="500px" src="assets/demo.gif"/>
</p>

## Requirements

- python v3.5+
  - pygame v2.1.0+

## Usage

To launch the application without importing maze from image 
```bash
python3 main.py
```

To launch the application with image maze
```bash
python3 main.py path/to/image/file
```

## Controls

### Importing maze from image

- To make the image clear in the "image preview" window, change the size and threshold in the "image settings" window. After that, hit enter.

### Editing grid and finding path

- To designate the beginning of a path in the grid, click the "start point" button.
- Similarly, click "end point" to mark the path's end point, and "block" to mark the point as block.
- To find the path, click "find path" and then "reset" to clear the entire grid. Before selecting "find path", make sure you mark the starting and ending points.
- To make a mark in a box, use the left mouse button. To remove the block, right-click on the box.
