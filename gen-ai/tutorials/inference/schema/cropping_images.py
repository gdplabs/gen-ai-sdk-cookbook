"""Schema: cropping images.

Reference: https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference/schema#cropping-images
"""

from pathlib import Path

from gllm_inference.schema import Attachment, BoxCoordinates


def main() -> None:
    """Crop a region of an image attachment and save it."""
    image = Attachment.from_path(str(Path(__file__).parent / "data" / "sample.png"))

    cropped = image.crop(
        BoxCoordinates(top=0.18, bottom=0.76, left=0.22, right=0.81),
        filename="cropped.png",
    )
    cropped.write_to_file("cropped.png")
    print(cropped.filename)


if __name__ == "__main__":
    main()
