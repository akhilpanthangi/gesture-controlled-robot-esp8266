# GitHub Upload Guide

## Repository settings

- **Name:** `gesture-controlled-robot-esp8266`
- **Description:** `Real-time hand-gesture-controlled robot using Python, OpenCV, MediaPipe, NodeMCU ESP8266 and an L298N motor driver.`
- **Visibility:** Public
- **Add README:** No
- **Add .gitignore:** No
- **Choose a license:** None — the MIT License file is already included

## Upload

1. Create the empty repository using the settings above.
2. Extract the downloaded project ZIP on your computer.
3. Open the extracted `gesture-controlled-robot-esp8266` folder.
4. On the empty GitHub repository page, select **uploading an existing file**.
5. Drag the `firmware`, `media` and `software` folder icons from Windows File
   Explorer into the upload area. GitHub may list their individual files while
   uploading; it will reconstruct the folders after the commit.
6. Drag `.gitignore`, `README.md`, `LICENSE`, `requirements.txt` and this guide
   into the same upload area.
7. Confirm that the file paths still begin with `firmware/`, `media/` or
   `software/` where appropriate.
8. Enter this commit message:

   `Initial commit: add gesture-controlled robot project`

9. Select **Commit changes**.

## Suggested topics

`gesture-control`, `computer-vision`, `mediapipe`, `opencv`, `python`,
`esp8266`, `nodemcu`, `robotics`, `iot`, `l298n`

## Final checks

- Confirm that the README appears on the repository home page.
- Confirm that `media/demo.mp4` opens successfully.
- Confirm that the public firmware contains `YOUR_ROBOT_WIFI_PASSWORD`, not
  your real password.
