"""
Image Drawing and Generation for 0.91" 128 by 32 OLED Displays
"""

import pkg_resources

from PIL import Image, ImageDraw, ImageFont, ImageChops

from . import WIDTH, HEIGHT

def generate_status_image(header: str, body: str, footer: str, invert=False) -> Image.Image:    
    """Generates an image to be displayed on the OLED display

    Parameters
    ----------
    header : str
        Status Header, placed small and ontop of the main message in the image.
    body : str
        Message Body, the bulk of the status, placed large and centered.
    footer : str
        Status Footer, the 'page number' of the status message, placed small in the lower right.
    invert : bool, optional
        Images are light on dark by default, if `True` image will be dark on light.
    
    Returns
    -------
    PIL.Image.Image
        Image ready to be displayed on the OLED display
    """

    # Create Blank Drawable Image
    image = Image.new('1', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)

    # Initialize Fonts
    tiny_font = ImageFont.truetype(pkg_resources.resource_filename('oled_status', 'fonts/ProggyVector Regular.ttf'), 8)
    small_font = ImageFont.truetype(pkg_resources.resource_filename('oled_status', 'fonts/ProggyVector Regular.ttf'), 10)
    big_font = ImageFont.truetype(pkg_resources.resource_filename('oled_status', 'fonts/OpenSans-Bold.ttf'), 14)

    # Draw Header and Body on Image
    draw.text((0, 0), header.upper(), 255, small_font)
    draw.text((0, 8), body, 255, big_font)

    # Calculate Footer Offset (right justify) and Draw
    footer_length = tiny_font.getlength(footer)
    draw.text((WIDTH - footer_length, 22), footer, 255, tiny_font)

    if invert:
        return ImageChops.invert(image)
    
    return image

if __name__ == '__main__':
    image = generate_status_image('OLED-Status', 'Important Status', '0/0')
    image.save('test.png')