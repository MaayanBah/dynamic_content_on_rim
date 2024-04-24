import os
from enum import Enum


class Videos(Enum):
    TomAndJerry_high = 1
    TomAndJerry_low = 2
    Neiruz_high = 3
    Neiruz_low = 4


def video_name_to_path(video_name: str):
    # TODO Neiruz videos are wrong
    videos: dict[Videos, str] = {
        Videos.TomAndJerry_high:
            r"C:\Maayan\First degree\fourth year\Project\run-experiment\assets\final_videos\Tom_and_Jerry.mp4",
        Videos.TomAndJerry_low:
            r"C:\Maayan\First degree\fourth year\Project\run-experiment\assets\final_videos\Tom_and_Jerry_low_contrast.mp4",
        Videos.Neiruz_high:
            r"C:\Maayan\First degree\fourth year\Project\run-experiment\assets\gabor_patch_videos\10_2.avi",
        Videos.Neiruz_low:
            r"C:\Maayan\First degree\fourth year\Project\run-experiment\assets\gabor_patch_videos\10_2.avi"
    }

    if "tom_high" in video_name:
        return videos[Videos.TomAndJerry_high]
    if "tom_low" in video_name:
        return videos[Videos.TomAndJerry_low]
    if "niruz_high" in video_name:
        return videos[Videos.Neiruz_high]
    if "niruz_low" in video_name:
        return videos[Videos.Neiruz_low]

def main():
    dynamic_script_edit = (
        r"C:\Maayan\First degree\fourth year\Project\dynamic_content_on_rim\dynamic_content_on_rim.git\dynamic_rim.py"
    )
    ex_7 = (
        r"C:\Maayan\First degree\fourth year\Project\pupil_invisible\experiment_data\test_real_data\experiments_raw\ex_7"
    )
    image_7 = (
        r"C:\Maayan\First degree\fourth year\Project\pupil_invisible\experiment_data\test_real_data\corners_7\image.json"
    )
    corners_7 = (
        r"C:\Maayan\First degree\fourth year\Project\pupil_invisible\experiment_data\test_real_data\corners_7\points.json"
    )
    rim_7 = r"C:\Maayan\First degree\fourth year\Project\pupil_invisible\experiment_data\test_real_data\rim_7"
    print(os.listdir(ex_7))
    count_c = 0
    for video in os.listdir(ex_7):
        raw_path = os.path.join(ex_7, video)
        output_path = os.path.join(ex_7, video, "mapped")
        output_video = os.path.join(output_path, "merged_video.mp4")
        output_csv = os.path.join(output_path, "gaze.csv")
        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        if not os.path.isfile(output_csv) or not os.path.isfile(output_video):
            count_c += 1
            command = (f"python \"{dynamic_script_edit}\""
                       f" --screen_video_path \"{video_name_to_path(video)}\" --raw_folder_path \"{raw_path}\""
                       f" --rim_folder_path \"{rim_7}\" --corners_screen \"{corners_7}\" --corners_image \"{image_7}\" "
                       f" --out_video_path \"{output_video}\" --out_csv_path \"{output_csv}\"")
            print(command, "\n\n")


if __name__ == "__main__":
    main()