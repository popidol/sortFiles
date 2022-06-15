from exif import Image
import piexif
from pymediainfo import MediaInfo


def info_file_exif(directory, prin):
    img = Image(directory)
    dictionary = {}
    count = len(img.list_all())

    for i in range(count):
        key = img.list_all()[i]
        try:
            f = ((img.list_all())[i])
            info = img.get(f)
        except:
            info = None

        if (prin == True):
            print(f"{key} - {info}")
        dictionary.update({key: info})
    return dictionary

def info_file_pymediainfo(directory, prin):
    arry = []
    count = len(MediaInfo.parse(directory).to_data().get("tracks"))
    for j in range(count):
        for i in range(len(MediaInfo.parse(directory).to_data().get("tracks")[j].items())):
            key = (list((MediaInfo.parse(directory).to_data().get("tracks")[j])))[i]
            info = MediaInfo.parse(directory).to_data().get('tracks')[j].get(key)
            if (prin == True):
                print(f"{key} - {info}")
            arry.append(key)
            arry.append(info)
    return arry


def info_file_piexif(directory, prin):
    exif_dict = piexif.load(directory)
    dictionary = {}
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[ifd]:
            key = piexif.TAGS[ifd][tag]['name']
            info = exif_dict[ifd][tag]
            if (prin == True):
                print(f"{key} - {info}")
            dictionary.update({key: info})
        return dictionary

def info_file_pil(directory, prin):
    from PIL.ExifTags import TAGS
    from PIL import Image
    image = Image.open(directory)
    exifdata = image.getexif()
    for tag_id in exifdata:
        # получить имя тега вместо идентификатора
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # декодировать байты
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag}: {data}")

# d1 =r"D:\photo\jpeg\IMG_20180811_140540-01.jpeg"
#
# try:
#     print('1--------------------------------------------------------------------')
#     info_file_exif(d1, True)
# except:
#     print('1-ошибка-------------------------------------------------------------------')
# try:
#     print('2--------------------------------------------------------------------')
#     info_file_pymediainfo(d1, True)
# except:
#     print('2-ошибка-------------------------------------------------------------------')
# try:
#     print('3--------------------------------------------------------------------')
#     info_file_piexif(d1, True)
# except:
#     print('3-ошибка-------------------------------------------------------------------')
# try:
#     print('4--------------------------------------------------------------------')
#     info_file_pil(d1, True)
# except:
#     print('4-ошибка-------------------------------------------------------------------')

