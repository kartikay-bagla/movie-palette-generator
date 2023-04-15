import cv2
import numpy as np

import typer
import os


def _resize_frame(frame: np.ndarray, factor: int) -> np.ndarray:
    return cv2.resize(frame, (frame.shape[1] // factor, frame.shape[0] // factor))


def _get_dom_color_from_frame(frame: np.ndarray):
    # Flatten frame to 1D array
    pixels = frame.reshape(-1, 3)

    k = 1  # number of clusters
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, _, centers = cv2.kmeans(
        np.float32(pixels), k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    # Convert center color from float to integer
    return np.round(centers[0]).astype(int)


def _display_dom_color_and_frame(frame: np.ndarray, dominant_color: np.ndarray):
    dominant_color_display = np.zeros((100, 100, 3), dtype=np.uint8)
    dominant_color_display[:, :] = dominant_color
    cv2.imshow("Dominant Color", dominant_color_display)
    cv2.imshow("Frame", frame)


def _create_output_frame(
    dom_colors: list[np.ndarray], output_height: int, output_length: int
) -> np.ndarray:
    out_array = np.zeros((output_height, len(dom_colors), 3), dtype=np.uint8)
    for i, col in enumerate(dom_colors):
        out_array[:, i, :] = col
    return cv2.resize(out_array, (output_length, output_height))


def create_palette(
    input_file_name: str = typer.Argument(
        ..., help="Path to input file. Example: input.mp4"
    ),
    output_file_name: str = typer.Argument(
        ...,
        help="Path to output file. Will raise error if file already exists unless"
        " output_file_overwrite is set. Example: output.png",
    ),
    output_file_overwrite: bool = typer.Option(
        False, help="If this is set, will overwrite output file if it exists."
    ),
    input_resize_factor: int = typer.Option(
        1, help="Factor by which to scale down image. Cannot be less than 1."
    ),
    output_height: int = typer.Option(540, help="Height of output palette in pixels."),
    output_length: int = typer.Option(1920, help="Length of output palette in pixels."),
    debug_show_dom_color_and_frame: bool = typer.Option(
        False,
        help="Show dominant color for each frame. Press q to quit, n to move forward.",
    ),
):
    # Load video file
    if not os.path.exists(input_file_name):
        raise FileNotFoundError("Given input file does not exist.")
    cap = cv2.VideoCapture(input_file_name)

    dom_colors = []

    # Loop through frames
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame for faster processing (optional)
        if input_resize_factor >= 1:
            frame = _resize_frame(frame=frame, factor=input_resize_factor)

        # Get dominant color
        dominant_color = _get_dom_color_from_frame(frame=frame)
        dom_colors.append(dominant_color)

        # Display dominant color
        if debug_show_dom_color_and_frame:
            _display_dom_color_and_frame(frame=frame, dominant_color=dominant_color)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):  # Quit
                break
            elif key == ord("n"):  # Next frame
                continue

    output_frame = _create_output_frame(
        dom_colors=dom_colors, output_height=output_height, output_length=output_length
    )

    if os.path.exists(output_file_name) and not output_file_overwrite:
        raise FileExistsError(
            "Given output file already exists. To overwrite, use output_file_overwrite."
        )
    cv2.imwrite(output_file_name, output_frame)

    cap.release()

    if debug_show_dom_color_and_frame:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    typer.run(create_palette)
