from exif import Image
import piexif
from pymediainfo import MediaInfo

import settings

dictionary_of_months = {'01': 'январь',
                        '02': 'февраль',
                        '03': 'март',
                        '04': 'апрель',
                        '05': 'май',
                        '06': 'июнь',
                        '07': 'июль',
                        '08': 'август',
                        '09': 'сентябрь',
                        '10': 'октябрь',
                        '11': 'ноябрь',
                        '12': 'декабрь'}

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

def time_counter(start, end):
    day = 0
    hour = 0
    min = 0
    sec = int(end - start)

    while sec // (24 * 60 * 60) != 0:
        day += 1
        sec = sec // (24 * 60 * 60)
    while sec // (60 * 60) != 0:
        hour += 1
        sec = sec // (60 * 60)
    while sec // (60) != 0:
        min += 1
        sec = sec // (60)
    if settings.print_time_finish:
        print(f"Программа работала\n Дней - {day}\nЧасов - {hour}\nМинут - {min}\nСекунд - {sec}")

