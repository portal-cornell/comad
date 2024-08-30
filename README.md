
# Collaborative Manipulation Dataset (CoMaD)

The CoMaD dataset is a collection of collaborative kitchen activities. We release 5 different long-horizon activities (Reactive Stirring, Cart Place, Table Setting, Cabinet Arrange, and, Object Handovers).

The dataset contains multiple episodes of human-human and human-robot teams performing each activity. There are over 15 unique users across our dataset collaborating with a Franka Emika Research 3 robot arm.

We release a high-quality dataset collected using a motion capture system, consisting of:
- 488 human-human episodes (~6 hours of motion)
- 304 human-robot episodes (~1 hour of motion)

Each episode contains the following data:
- Motion Capture of 24 upper body joints of the human
- Robot Arm Joint Positions (for Human-Robot teams)
- Third-person RGB camera view

Motion capture and joint positions are collected at a frequency of 120Hz, while the camera records images at 30Hz.

 <table border="0">
 <tr align="center">
    <td><img src="docs/tasks.png" alt>
</tr>
</table>

<!-- ### Human-Human Interactions

<table border="0">
 <tr align="center">
    <td><img src="docs/handover_hh.gif" alt>
    <em>Object Handover</em></td>
</tr>
    <tr align="center">
    <td><img src="docs/react_hh.gif" alt>
    <em>Reactive Stirring</em></td>
</tr>
    <tr align="center">
    <td><img src="docs/tabletop_hh.gif" alt>
    <em>Collaborative Table Setting</em></td>
</tr>
</tr>
    <tr align="center">
    <td><img src="docs/cabinet_hh.gif" alt>
    <em>Cabinet Arrange</em></td>
</tr>
</tr>
    <tr align="center">
    <td><img src="docs/cart_hh.gif" alt>
    <em>Cart Pick</em></td>
</tr>
</table>

### Human-Robot Interactions

<table border="0">
 <tr align="center">
    <td><img src="docs/handover_hr.gif" alt>
    <em>Object Handover</em></td>
</tr>
    <tr align="center">
    <td><img src="docs/react_hr.gif" alt>
    <em>Reactive Stirring</em></td>
</tr>
    <tr align="center">
    <td><img src="docs/tabletop_hr.gif" alt>
    <em>Collaborative Table Setting</em></td>
</tr>
</tr>
    <tr align="center">
    <td><img src="docs/cabinet_hr.gif" alt>
    <em>Cabinet Arrange</em></td>
</tr>
</tr>
    <tr align="center">
    <td><img src="docs/cart_hr.gif" alt>
    <em>Cart Pick</em></td>
</tr>
</table> -->

### Setup

Please download the remaining components for the dataset from this link: [CoMaD](https://cornell.box.com/s/jb0wau30dqotcjsak78ks64ea1o88yan). This includes the folders for the corresponding videos for the json files in the github repo.

After downloading, maintain the following file structure to facilitate splitting model training into training and validation sets.
```
├── train
├── test
```
First create a new conda environment with python=3.9 and run the below command
``` 
pip install -r requirements.txt 
```

Then activate ipywidgets

``` 
jupyter nbextension enable --py widgetsnbextension 
```

### Visualization and Features

Play any data episode through Python notebook: ```scripts/comad_visualization.ipynb```.

In the notebook, the user can load a matplotlib viz of every episode that can either be paired with the corresponding RGB video or a slideshow of images from the RGB video that are aligned by timestep.

<table border="0">
 <tr align="center">
    <td><img src="docs/cabinet_hr_vid.gif" alt>
    <em>RGB Video</em></td>
</tr>
    <tr align="center">
    <td><img src="docs/cabinet_hr_img_slide.gif" alt>
    <em>Image Slideshow</em></td>
</tr>
</table>

### BibTeX
If you find the dataset or paper useful for your research, please cite our paper:

   ```bash
   @article{kedia2023interact,
    title={InteRACT: Transformer Models for Human Intent Prediction Conditioned on Robot Actions},
    author={Kedia, Kushal and Bhardwaj, Atiksh and Dan, Prithwish and Choudhury, Sanjiban},
    journal={arXiv preprint arXiv:2311.12943},
    year={2023}
  }
   ``` 
