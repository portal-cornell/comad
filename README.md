
# Collaborative Manipulation Dataset (CoMaD)

 We release a high-quality dataset collected using a motion capture system, consisting of 488 human-human and 304 human-robot episodes of collaboration to perform daily household activities. 

 <table border="0">
 <tr align="center">
    <td><img src="docs/tasks.png" alt>
</tr>
</table>

### Human-Human Interactions

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
</table>

### Setup

Please download the remaining components for the dataset from this link: [CoMaD](https://cornell.box.com/s/jb0wau30dqotcjsak78ks64ea1o88yan). This includes the folders for the corresponding videos for the json files in the github repo.

Once downloaded, maintain the below file structure:
```
├── train
├── test
```
This allows for ML model training.

First create a new conda environment with python=3.9 and run the below command

``` 
pip install -r requirements.txt 
```

Then activate ipywidgets

``` 
jupyter nbextension enable --py widgetsnbextension 
```

### Visualization and Features

Play any data episode through Python notebook: scripts/comad_visualization.ipynb.

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
