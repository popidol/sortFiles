import os.path
from exif import Image
import piexif
import shutil
from pymediainfo import MediaInfo
from threading import Thread
import numpy as np


def sort_format_directory(directory, extension):
    arr = []
    count_full, count = 0, 0
    for address, dirs, files in os.walk(directory):
        for name in files:
            count_full += 1
            p = os.path.join(address, name)
            if p.find(f".{extension}") != -1:
                count += 1
                arr.append(p)
    print(f"файлов с нужным расширением - {count}")
    print(f"файлов всего - {count_full}")
    return arr

def copy_files_new_directory(old_directories, new_directory):
    c = 0
    if (os.path.exists(new_directory) != True): os.mkdir(new_directory)
    for i in range(len(old_directories)):
        if old_directories[i].find('jpg') != -1:
            pass
        elif old_directories[i].find('JPG') != -1:
            pass
        else:
            try:
                array = info_file_pymediainfo(old_directories[i], False)
                file_creation_date, file_creation_date__local, \
                file_last_modification_date, file_last_modification_date__local = None, None, None, None
                for j in range(len(array) - 2):
                    if (array[j] == 'file_creation_date'):  # UTC 2022-06-12 01:14:44.945
                        if (array[j + 1][0] == 'U'):
                            array[j + 1] = array[j + 1].replace("UTC ", "")
                        if (file_creation_date == None):
                            file_creation_date = array[j + 1]
                        else:
                            file_creation_date = comparison_date(file_creation_date, array[j + 1])
                    if (array[j] == 'file_creation_date__local'):  # 2022-06-12 04:14:44.945
                        if (array[j + 1][0] == 'U'):
                            array[j + 1] = array[j + 1].replace("UTC ", "")
                        if (file_creation_date__local == None):
                            file_creation_date__local = array[j + 1]
                        else:
                            file_creation_date__local = comparison_date(file_creation_date__local, array[j + 1])
                    if (array[j] == 'file_last_modification_date'):  # UTC 2022-03-26 03:54:04.000
                        if (array[j + 1][0] == 'U'):
                            array[j + 1] = array[j + 1].replace("UTC ", "")
                        if (file_last_modification_date == None):
                            file_last_modification_date = array[j + 1]
                        else:
                            file_last_modification_date = comparison_date(file_last_modification_date, array[j + 1])
                    if (array[j] == 'file_last_modification_date__local'):  # 2022-03-26 06:54:04.000
                        if (array[j + 1][0] == 'U'):
                            array[j + 1] = array[j + 1].replace("UTC ", "")
                        if (file_last_modification_date__local == None):
                            file_last_modification_date__local = array[j + 1]
                        else:
                            file_last_modification_date__local = comparison_date(file_last_modification_date__local,
                                                                                 array[j + 1])
                    # видео
                    if (array[j] == 'encoded_date'): pass  # UTC 2018-01-05 10:12:36
                    if (array[j] == 'tagged_date'): pass  # UTC 2020-05-01 13:46:11
                min_data = comparison_date(comparison_date(file_creation_date, file_creation_date__local),
                                           comparison_date(file_last_modification_date,
                                                           file_last_modification_date__local))
            except:
                pass
            if (min_data != None):
                year = min_data[0:4]
                month = min_data[5:7]
                if month == "01":
                    zz = "январь"
                elif month == "02":
                    zz = "февраль"
                elif month == "03":
                    zz = "март"
                elif month == "04":
                    zz = "апрель"
                elif month == "05":
                    zz = "май"
                elif month == "06":
                    zz = "июнь"
                elif month == "07":
                    zz = "июль"
                elif month == "08":
                    zz = "август"
                elif month == "09":
                    zz = "сентябрь"
                elif month == "10":
                    zz = "октябрь"
                elif month == "11":
                    zz = "ноябрь"
                elif month == "12":
                    zz = "декабрь"
                else:
                    zz = "no"

                lam_directory = new_directory + '\\' + year
                if (os.path.exists(lam_directory) != True):
                    os.mkdir(new_directory + '/' + year)
                lam_directory = new_directory + '\\' + year + '\\' + zz
                if (os.path.exists(lam_directory) != True):
                    os.mkdir(new_directory + '/' + year + '/' + zz)
            lam_directory = new_directory + '\\' + year + '\\' + zz
            shutil.copy2(old_directories[i], lam_directory)
            # os.remove(old_directories[i])#удалять исходник
            if i == (100 + c):
                print(f"перемешенно {i} файлов")
                c += 100


def comparison_date(date1, date2):
    if (date1 == None and date2 != None): return date2
    if (date2 == None and date1 != None): return date1
    if (date1 == None and date2 == None): return None
    date = ""
    year_array = []
    year = ""
    year1 = ""
    month_array = []
    month = ""
    month1 = ""
    day_array = []
    day = ""
    day1 = ""
    # год
    year_array.append(date1[0])
    year_array.append(date1[1])
    year_array.append(date1[2])
    year_array.append(date1[3])
    year = int(year.join(year_array))
    year_array.clear()
    year_array.append(date2[0])
    year_array.append(date2[1])
    year_array.append(date2[2])
    year_array.append(date2[3])
    year1 = int(year1.join(year_array))
    if (year == year1):
        # месяц
        month_array.append(date1[5])
        month_array.append(date1[6])
        month = int(month.join(month_array))
        month_array.clear()
        month_array.append(date2[5])
        month_array.append(date2[6])
        month1 = int(month1.join(month_array))
        if (month == month1):
            # день
            day_array.append(date1[8])
            day_array.append(date1[9])
            day = int(day.join(day_array))
            day_array.clear()
            day_array.append(date2[8])
            day_array.append(date2[9])
            day1 = int(day1.join(day_array))
            if (day == day1):
                date = date1
            elif (day < day1):
                date = date1
            elif (day > day1):
                date = date2
        elif (month < month1):
            date = date1
        elif (month > month1):
            date = date2
    elif (year < year1):
        date = date1
    elif (year > year1):
        date = date2

    return date

def info_file_exif(directory, prin):
    img = Image(directory)
    dictionary = {}
    for i in range(len(img.list_all())):
        key = img.list_all()[i]
        try:
            info = img.get(img.list_all()[i])
        except:
            info = None
        if (prin == True):
            print(f"{key} - {info}")
        dictionary.update({key: info})
    return dictionary

def info_file_pymediainfo(directory, prin):
    arry = []
    try:
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
    except:
        pass

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
        print(f"{tag:25}: {data}")

d1 = r"D:\photo\doc" #от куда
d2 = r"D:\photo\doc" #куда
extension = 'doc'#с каким расширением
tred = 10 #сколько потоков задейсвовать

for array in (np.array_split(sort_format_directory(d1, extension), tred)):
    b = list(array)
    th1 = Thread(target=copy_files_new_directory, args=(b, d2))
    th1.start()

