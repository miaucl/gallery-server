"""Format functions."""

from io import BytesIO

from PIL import Image, ImageFilter, ImageOps

from .dithering import convert_image_to_bmp_with_palette


def format_image(
    image: Image.Image,
    format: str,
    size: str | None = None,
    fit: str = "cover",
    filter: str | None = None,
    dithering_palette: str | None = None,
) -> BytesIO:
    """Pick an image from the folder based on the seed.

    Parameters
    ----------
    image
        The image
    format
        The output format of the image ["png", "jpeg", "bmp", "gif"]
    size
        A size of the image
    fit
        The fitting of the image when resized ["cover", "contain"]
    filter
        The filter applied to the image ["grayscale", "sepia", "blur", "dithering"]
    dithering_palette
        The dithering palette to use when format is `bmp` ["black-white", "black-white-yellow", "black-white-red", "4-color", "6-color", "n-color"]

    Returns
    -------
    BytesOI
        The converter image in RAM

    Raises
    ------
    ReferenceError
        If no image is present

    """
    img = image.copy()

    if size:
        width, height = map(int, size.split("x"))
        if fit == "cover":
            img = ImageOps.fit(img, (width, height))
        elif fit == "contain":
            img.thumbnail((width, height), Image.Resampling.LANCZOS)

    # Apply filters
    if filter == "grayscale":
        img = ImageOps.grayscale(img)
    elif filter == "sepia":
        sepia = Image.new("RGB", img.size)
        sepia_data = [
            (
                int(r * 0.393 + g * 0.769 + b * 0.189),
                int(r * 0.349 + g * 0.686 + b * 0.168),
                int(r * 0.272 + g * 0.534 + b * 0.131),
            )
            for (r, g, b) in img.getdata()
        ]
        sepia.putdata(sepia_data)
        img = sepia
    elif filter == "blur":
        img = img.filter(ImageFilter.BLUR)
    elif filter == "dithering" and format == "bmp":
        if dithering_palette is not None:
            img = convert_image_to_bmp_with_palette(img, dithering_palette)
        else:
            raise ValueError("Cannot dither without palette")

    # Format
    img_io = BytesIO()
    img.save(img_io, format=format)
    img_io.seek(0)

    return img_io
