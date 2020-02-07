def image_urls():
    """Generate all radar map images"""
    baseurl = "http://alertario.rio.rj.gov.br/upload/Mapa/semfundo/radar"
    for i in range(1, 21):
        yield "{}{:03d}.png".format(baseurl, i)


def get_image_from_url(url):
    """Fetch image from URL and return PIL Image object"""
    from PIL import Image
    import requests
    from io import BytesIO

    response = requests.get(url)

    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        return None


def image_opaque_percent(img):
    """Return percentage of pixels fully opaque

    The images in this case are only fully transparent or opaque, ie:

        >>> set(img.getdata(3))
        {0, 255}

    See:
        https://pillow.readthedocs.io/en/latest/reference/Image.html#PIL.Image.Image.getdata
    """

    total = len(img.getdata(3))
    opaque = sum(x != 0 for x in img.getdata(3))

    return float(opaque) / total * 100


def percent_rain(pc):
    """Return percentage of rain in image minus sundries (time, legend)"""
    sundries = 1.87
    return (pc-sundries)


if __name__ == "__main__":
    for url in image_urls():
        img = get_image_from_url(url)
        if img:
            rain = percent_rain(image_opaque_percent(img))
        else:
            print("Skipping blank image")
            continue

        print("Rain for {0} is: {1:.2f}%".format(url.rsplit("/", 1)[1], rain))
