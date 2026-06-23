"""Image asset generation: favicon.ico and og.png."""

from pathlib import Path


def _find_font(candidates: list, size: int):
    """Return the first loadable ImageFont from a list of path strings."""
    try:
        from PIL import ImageFont
        for path in candidates:
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
        return ImageFont.load_default()
    except ImportError:
        return None


# Common system font paths per OS (tried in order)
_BOLD_SERIF = [
    r"C:\Windows\Fonts\georgiab.ttf",
    r"C:\Windows\Fonts\arialbd.ttf",
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
    "/Library/Fonts/Georgia Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]
_DISPLAY = [
    r"C:\Windows\Fonts\impact.ttf",
    r"C:\Windows\Fonts\georgiab.ttf",
    "/System/Library/Fonts/Supplemental/Impact.ttf",
    "/Library/Fonts/Impact.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
]
_SERIF_ITALIC = [
    r"C:\Windows\Fonts\georgiai.ttf",
    r"C:\Windows\Fonts\georgia.ttf",
    "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
    "/Library/Fonts/Georgia Italic.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifItalic.ttf",
]
_MONO = [
    r"C:\Windows\Fonts\lucon.ttf",
    r"C:\Windows\Fonts\cour.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttf",
    "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
]


def build_favicon(output: str = "docs/favicon.ico") -> bool:
    """Generate a dark-background 'J' monogram favicon at 16/32/48 px."""
    try:
        from PIL import Image, ImageDraw

        SZ = 96
        img  = Image.new("RGBA", (SZ, SZ), (5, 5, 5, 255))
        draw = ImageDraw.Draw(img)
        font = _find_font(_BOLD_SERIF, 64)

        text = "J"
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            ((SZ - tw) // 2 - bbox[0], (SZ - th) // 2 - bbox[1]),
            text, font=font, fill=(244, 244, 239, 255),
        )
        img.save(output, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
        return True
    except Exception as e:
        print(f"   ⚠️  favicon.ico no generado: {e}")
        return False


def build_og_image(nombre: str, titulo: str, site_url: str,
                   output: str = "docs/og.png") -> bool:
    """Generate a 1200×630 Open Graph image."""
    try:
        from PIL import Image, ImageDraw

        W, H  = 1200, 630
        WHITE = (244, 244, 239)
        GRAY  = (90, 90, 90)
        MID   = (55, 55, 55)

        img  = Image.new("RGB", (W, H), (5, 5, 5))
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, 7, H], fill=WHITE)

        name_font = _find_font(_DISPLAY,      128)
        sub_font  = _find_font(_SERIF_ITALIC,  42)
        url_font  = _find_font(_MONO,          24)

        PAD   = 90
        parts = nombre.upper().split(" ", 1)
        draw.text((PAD, 155), parts[0],                           font=name_font, fill=WHITE)
        draw.text((PAD, 290), parts[1] if len(parts) > 1 else "", font=name_font, fill=WHITE)
        draw.text((PAD, 456), titulo,                             font=sub_font,  fill=GRAY)
        draw.rectangle([PAD, 540, W - PAD, 541], fill=MID)
        draw.text((PAD, 556), site_url.removeprefix("https://"),  font=url_font,  fill=GRAY)

        img.save(output, "PNG", optimize=True)
        return True
    except Exception as e:
        print(f"   ⚠️  og.png no generado: {e}")
        return False
