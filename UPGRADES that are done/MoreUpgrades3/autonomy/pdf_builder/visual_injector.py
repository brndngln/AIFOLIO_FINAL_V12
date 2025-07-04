from reportlab.platypus import Image, Spacer

def insert_visuals(story, image_paths):
    for image in image_paths:
        try:
            story.append(Image(image, width=300, height=200))
            story.append(Spacer(1, 12))
        except Exception:
            continue