# WIND_PLACEHOLDER
def generate_cover(title, style="minimal"):
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (1024, 768), color="white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((100, 100), title, font=font, fill="black")
    path = f"covers/{title.replace(' ', '_')}.png"
    img.save(path)
    return path
