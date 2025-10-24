import os
from app import create_app, db
from app.models import Destination, Image
from urllib.request import urlretrieve
from PIL import Image as PILImage, ImageDraw, ImageFont

SAMPLE_IMAGES = [
    ("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?w=1200", "Forest cabin"),
    ("https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=1200", "Mountain lake"),
    ("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200", "Beach sunrise"),
]

def _make_placeholder(path: str, text: str = "Digital Detox") -> None:
    width, height = 1200, 800
    img = PILImage.new('RGB', (width, height), color=(20, 26, 23))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    tw, th = draw.textlength(text, font=font), 14
    draw.text(((width - tw) / 2, (height - th) / 2), text, fill=(150, 220, 190), font=font)
    img.save(path, format='JPEG', quality=90)

def download_to_uploads(app, url, filename, placeholder_text: str = "Digital Detox"):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(path):
        try:
            urlretrieve(url, path)
        except Exception:
            _make_placeholder(path, text=placeholder_text)
    return filename

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    places = [
        Destination(
            name="Still Waters Retreat",
            location="Banff, Canada",
            description="A secluded lakeside lodge encouraging mindfulness, journaling, and guided forest bathing. Strictly no screens.",
            category="retreat",
            has_wifi=False,
            allows_screens=False,
        ),
        Destination(
            name="Cedar Grove Off‑Grid Resort",
            location="Oregon, USA",
            description="Solar-powered tiny cabins deep in old-growth forest. Communal meals, yoga, and star-gazing.",
            category="resort",
            has_wifi=False,
            allows_screens=False,
        ),
        Destination(
            name="Zen Bluff Mindfulness Point",
            location="Kyoto, Japan",
            description="Clifftop meditation decks with tea ceremony workshops. Devices stored on arrival.",
            category="mindfulness",
            has_wifi=False,
            allows_screens=False,
        ),
    ]

    db.session.add_all(places)
    db.session.commit()

    # Add sample images to first destination
    for idx, (url, cap) in enumerate(SAMPLE_IMAGES, start=1):
        fname = f"sample_{idx}.jpg"
        filename = download_to_uploads(app, url, fname, placeholder_text=cap)
        img = Image(destination_id=places[0].id, filename=filename, caption=cap, is_primary=(idx == 1))
        db.session.add(img)

    db.session.commit()
    print("Database seeded with sample data.")
