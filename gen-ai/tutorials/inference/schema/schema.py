from gllm_inference.schema import (
    Attachment,
    AudioConstraint,
    AudioUnit,
    ContentPolicy,
    ImageConstraint,
    ImageUnit,
    OnViolation,
    TextConstraint,
)

attachment = Attachment.from_path("path/to/image.jpeg")

attachment = Attachment.from_url("https://example.com/image.png")

attachment = Attachment.from_data_url("data:image/jpeg;base64,<base64_encoded_image>")

attachment = Attachment.from_bytes(b"<file_bytes>")

policy = ContentPolicy(
    text=[
        TextConstraint(max_size=4000),
        TextConstraint(min_size=3, on_violation=OnViolation.RAISE),
    ],
    image=[
        ImageConstraint(unit=ImageUnit.PIXELS, max_size=1024),
        ImageConstraint(unit=ImageUnit.BYTES, max_size=2_000_000),
    ],
    audio=[
        AudioConstraint(unit=AudioUnit.SECONDS, max_size=60),
    ],
)
