import json
import numpy as np
from matplotlib import pyplot as plt
import numpy as np
from IPython.display import Video, display
from ipywidgets import (
    interactive,
    interact,
    IntSlider,
    VBox,
    Layout,
    HBox,
    Output,
    Label,
    Play,
    jslink,
)
import os
import cv2


def extract_frames(video_path, save_every=1):
    vidcap = cv2.VideoCapture(video_path)
    success = True
    video = []
    print("Loading video frames .....")
    count = 0
    while success:
        success, image = vidcap.read()
        if not success:
            break
        image = cv2.resize(image, (480, 270))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if count % save_every == 0:
            video.append(image)
        count += 1
    print("Loaded")
    return video


def get_relevant_joints(
    all_joints,
    mapping,
    relevant_joints=[
        "BackTop",
        "LShoulderBack",
        "RShoulderBack",
        "LElbowOut",
        "RElbowOut",
        "LWristOut",
        "RWristOut",
        "WaistLBack",
        "WaistRBack",
        "LHandOut",
        "RHandOut",
    ],
):
    relevant_joint_pos = []
    for joint in relevant_joints:
        pos = all_joints[mapping[joint]]
        relevant_joint_pos.append(pos)
    return relevant_joint_pos


def get_history(all_joints, current_idx, mapping, history_length=10, skip_rate=5):
    history_joints = []
    for i in range(
        current_idx - (history_length - 1) * skip_rate, current_idx + 1, skip_rate
    ):
        idx = max(0, i)
        history_joints.append(get_relevant_joints(all_joints[idx], mapping))
    return history_joints


def get_future(all_joints, current_idx, mapping, future_length=25, skip_rate=5):
    future_joints = []
    for i in range(
        current_idx + skip_rate, current_idx + future_length * skip_rate + 1, skip_rate
    ):
        idx = min(i, all_joints.shape[0] - 1)
        future_joints.append(get_relevant_joints(all_joints[idx], mapping))
    return future_joints


def get_joints(joint_data, timestep, mapping):
    current_joints = get_relevant_joints(joint_data[timestep], mapping)
    history_joints = get_history(joint_data, timestep, mapping)
    future_joints = get_future(joint_data, timestep, mapping)

    return current_joints, future_joints


def point_array(
    current_joints,
    future_joints,
    figures,
    ax,
    swap_y_z=False,
    invert=False,
    color="black",
):
    edges = [(0, 1), (0, 2), (1, 3), (3, 5), (2, 4), (4, 6), (5, 9), (6, 10)]
    extra_edges = [(1, 7), (7, 8), (8, 2)]
    if current_joints is not None:
        for idx, edge in enumerate(edges + extra_edges):
            pos1, pos2 = current_joints[edge[0]], current_joints[edge[1]]
            x1, y1, z1 = pos1.tolist()
            x2, y2, z2 = pos2.tolist()
            if invert:
                x = np.array([-x1, -x2])
            else:
                x = np.array([x1, x2])
            if swap_y_z:
                y = np.array([z1, z2])
                z = np.array([y1, y2])
            else:
                y = np.array([y1, y2])
                z = np.array([z1, z2])
            figures[0][0].append(ax.plot(x, y, z, zdir="z", c=color, alpha=1))
            figures[0][1].append(ax.scatter(x, y, z, s=10, c=color, alpha=1))
    if future_joints is not None:
        for i, time in enumerate([24]):
            for idx, edge in enumerate(edges + extra_edges):
                joints = future_joints[time]
                pos1, pos2 = joints[edge[0]], joints[edge[1]]
                x1, y1, z1 = pos1.tolist()
                x2, y2, z2 = pos2.tolist()
                x = np.array([-x1, -x2])
                if swap_y_z:
                    y = np.array([z1, z2])
                    z = np.array([y1, y2])
                else:
                    y = np.array([y1, y2])
                    z = np.array([z1, z2])
                figures[2][0].append(
                    ax.plot(
                        x,
                        y,
                        z,
                        zdir="z",
                        c="green",
                        alpha=0.9 - 0.1 * ((time + 1) / 25),
                    )
                )
                figures[2][1].append(
                    ax.scatter(
                        x,
                        y,
                        z,
                        s=10,
                        c="green",
                        alpha=0.9 - 0.1 * ((time + 1) / 25),
                    )
                )


def robot_array(joints, figures, ax, timestep):
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 11)]
    robo_joints = joints[timestep]
    for idx, edge in enumerate(edges):
        if edge[1] == 8 or edge[1] == 9:
            line_width = 1
            point_rad = 2
        else:
            line_width = 4
            point_rad = 5
        pos1, pos2 = robo_joints[edge[0]], robo_joints[edge[1]]
        x1, y1, z1 = pos1.tolist()
        x2, y2, z2 = pos2.tolist()
        x = np.array([x1, x2])
        y = np.array([y1, y2])
        z = np.array([z1, z2])
        figures[0][0].append(
            ax.plot(x, y, z, zdir="z", c="black", alpha=1, linewidth=line_width)
        )
        figures[0][1].append(
            ax.scatter(x, y, z, s=5, c="black", alpha=1, linewidth=point_rad)
        )


def get_title(task, episode, dataset):
    if task == "cabinet" or task == "cart" or task == "handover":
        data = task.capitalize()
    elif task == "tabletop":
        data = "Tabletop Motion"
    elif task == "react":
        data = "Reactive Stirring"
    return f"{data} {dataset} Episode {episode}"


# Create a function to update the plots
def update_plots(
    frame_no,
    dataset,
    task,
    episode,
    person_data,
    mapping,
    video,
    img_slide,
):
    joint_data_A = person_data["Person_1"]
    if dataset == "HH":
        joint_data_B = person_data["Person_2"]
    else:
        joint_data_B = []
    if dataset == "HR":
        joint_data_R = person_data["Robot"]
    else:
        joint_data_R = None
    if img_slide:
        fig, (ax_json, ax_vid) = plt.subplots(1, 2, figsize=(12, 5))
    else:
        fig = plt.figure(figsize=(12, 5))
        ax_json = fig.add_subplot(projection="3d")
        ax_vid = None
    if img_slide:
        ax_json.axis("off")
        ax_vid.axis("off")
        ax_json = fig.add_subplot(1, 2, 1, projection="3d")
    ax_json.grid(False)
    ax_json.set_xticks([])
    ax_json.set_yticks([])
    ax_json.set_zticks([])
    figures_A = [[[], []], [[], []], [[], []]]
    figures_B = [[[], []], [[], []], [[], []]]
    figures_R = [[[], []]]
    if img_slide:
        ax_vid = fig.add_subplot(1, 2, 2)
        ax_vid.axis("off")
        if (frame_no // 4) < len(video):
            ax_vid.imshow(video[frame_no // 4])
        else:
            ax_vid.imshow(video[len(video) - 1])

    if dataset == "HR":
        ax_json.set_xlim3d([-0.5, 1])
        ax_json.set_ylim3d([0, 1.5])
        ax_json.set_zlim3d([1.2, 2.2])
    else:
        ax_json.set_xlim3d([-0.5, 1])
        ax_json.set_ylim3d([-0.5, 1])
        ax_json.set_zlim3d([1.2, 2.2])

    if dataset == "HH":
        current_joints_A, future_joints_A = get_joints(joint_data_A, frame_no, mapping)
        current_joints_B, future_joints_B = get_joints(joint_data_B, frame_no, mapping)

        point_array(
            current_joints=current_joints_A,
            future_joints=None,
            figures=figures_A,
            ax=ax_json,
            swap_y_z=True,
            invert=True,
        )
        point_array(
            current_joints=current_joints_B,
            future_joints=None,
            figures=figures_B,
            ax=ax_json,
            swap_y_z=True,
            invert=True,
        )

    else:
        point_array(
            current_joints=joint_data_A[frame_no],
            future_joints=None,
            figures=figures_B,
            ax=ax_json,
            color="#75aaff",
        )
        robot_array(
            joints=joint_data_R, figures=figures_R, ax=ax_json, timestep=frame_no
        )

    if img_slide:
        plt.suptitle(
            get_title(
                task=task,
                episode=episode,
                dataset=dataset,
            ),
            y=0.9,
            fontsize=16,
        )

    plt.show()


def load_data(pwd_path, train_test, dataset, task, episode, img_slide, snapshot):
    mapping_file = f"{pwd_path}/mapping.json"
    if snapshot:
        episode_file = f"{pwd_path}/snapshot_data/{task}/{dataset}/data.json"
        video_path = f"{pwd_path}/snapshot_data/{task}/{dataset}/video.MP4"
    else:
        episode_file = f"{pwd_path}/{train_test}/{task}/{dataset}/{episode}/data.json"
        video_path = f"{pwd_path}/{train_test}/{task}/{dataset}/{episode}/video.MP4"

    if img_slide:
        video = extract_frames(video_path=video_path)
    else:
        print("Loading video .....")
        video = Video(video_path, embed=True, width=480, height=270)
        print("Loaded")
    with open(mapping_file, "r") as f:
        mapping = json.load(f)

    with open(episode_file, "r") as f:
        data = json.load(f)

    person_data = {}
    total_time = len(data[list(data.keys())[0]])
    for person, joint_data in data.items():
        person_data[person] = []
        for timestep_index, timestep in enumerate(joint_data):
            new_timestep = []
            for joint_index, joint_pos in enumerate(timestep):
                if all(coord == 0 for coord in joint_pos):
                    nearby_timesteps = [
                        joint_data[i]
                        for i in range(
                            max(0, timestep_index - total_time),
                            min(len(joint_data), timestep_index + total_time),
                        )
                        if i != timestep_index
                    ]
                    new_joint_pos = joint_pos
                    for nearby_timestep in nearby_timesteps:
                        nearby_joint_pos = nearby_timestep[joint_index]
                        if not all(coord == 0 for coord in nearby_joint_pos):
                            new_joint_pos = nearby_joint_pos
                            break
                    new_timestep.append(new_joint_pos)
                else:
                    new_timestep.append(joint_pos)
            person_data[person].append(new_timestep)

        # Convert the final person_data array to a NumPy array
        person_data[person] = np.array(person_data[person])

    return mapping, video, person_data, total_time


def visualize(pwd_path, train_test, dataset, task, episode, img_slide, snapshot):
    # load data
    mapping, video, person_data, total_time = load_data(
        pwd_path=pwd_path,
        train_test=train_test,
        dataset=dataset,
        task=task,
        episode=episode,
        img_slide=img_slide,
        snapshot=snapshot,
    )
    ep_num = "Snapshot" if snapshot else episode

    def run_plot(frame_no):
        update_plots(
            frame_no=frame_no,
            dataset=dataset,
            task=task,
            episode=ep_num,
            person_data=person_data,
            mapping=mapping,
            video=video,
            img_slide=img_slide,
        )

    # Create a slider to control the number of points
    slider = IntSlider(
        min=0,
        max=total_time - 50,
        value=0,
        description="Timestep: ",
        layout=Layout(
            height="36px", width="500px", display="flex", justify_content="center"
        ),
    )

    play = Play(
        min=0,
        max=total_time - 50,
        step=15,
        layout=Layout(
            height="36px", width="500px", display="flex", justify_content="center"
        ),
    )

    link = jslink((play, "value"), (slider, "value"))
    # Display the widget

    h_box_layout = Layout(
        display="flex",
        flex_flow="row",
        justify_content="space-between",
        align_items="center",
    )
    v_box_layout = Layout(
        display="flex", justify_content="center", align_items="center"
    )

    w = interactive(run_plot, frame_no=slider)

    print("Displaying content .....")
    if img_slide:
        return display(VBox([w.children[1], w.children[0], play], layout=v_box_layout))
    else:
        out = Output()
        with out:
            display(video)
        title = Label(
            get_title(
                task=task,
                episode=ep_num,
                dataset=dataset,
            ),
            layout=Layout(
                height="auto", width="auto", display="flex", justify_content="center"
            ),
        )
        title.style.font_size = "24px"
        return display(
            VBox(
                [
                    title,
                    HBox([w.children[1], out], layout=h_box_layout),
                    w.children[0],
                    play,
                ],
                layout=v_box_layout,
            )
        )
