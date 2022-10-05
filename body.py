import os.path
import shutil
from threading import Thread
import numpy as np
import info
import settings
from exif import Image
from pymediainfo import MediaInfo
from datetime import datetime



def main():
    def start():
        all_required_files = 0
        processed_files = 0

        def sort_format_directory(directory, extension):
            arr = []
            count_full, count = 0, 0
            for address, dirs, files in os.walk(directory):
                for name in files:
                    count_full += 1
                    p = os.path.join(address, name).split(".")
                    p = p[len(p) - 1]
                    if p.lower().find(f"{extension}") != -1:
                        count += 1
                        arr.append(os.path.join(address, name))
            print(f"файлов с нужным расширением - {count}")
            print(f"файлов всего - {count_full}")

            nonlocal all_required_files
            all_required_files = count
            return arr

        def copy_files_new_directory(old_directories, new_directory):

            if os.path.exists(new_directory) != True: os.mkdir(new_directory)

            for i in range(len(old_directories)):
                min_data = None
                file = old_directories[i]
                if (file.lower().find('jpg') != -1) or (file.lower().find('jpeg') != -1):
                    try:
                        img = Image(file)
                        min_data = comparison_date(img.get('datetime'), min_data)
                        min_data = comparison_date(img.get('datetime_original'), min_data)
                        min_data = comparison_date(img.get('datetime_digitized'), min_data)
                        min_data = comparison_date(img.get('gps_datestamp'), min_data)
                        if int(min_data[0:4]) == 1980:
                            min_data = None
                    except:pass
                if min_data == None:
                    for j in range(len(MediaInfo.parse(file).to_data().get("tracks"))):
                        if ((
                                MediaInfo.parse(file).to_data().get('tracks')[j].get('file_creation_date')) != None):
                            min_data = comparison_date((MediaInfo.parse(file).to_data().get('tracks')[j].get(
                                'file_creation_date').replace("UTC ", "")), min_data)
                        if ((MediaInfo.parse(file).to_data().get('tracks')[j].get(
                                'file_creation_date__local')) != None):
                            min_data = comparison_date((MediaInfo.parse(file).to_data().get('tracks')[j].get(
                                'file_creation_date__local').replace("UTC ", "")), min_data)
                        if ((MediaInfo.parse(file).to_data().get('tracks')[j].get(
                                'file_last_modification_date')) != None):
                            min_data = comparison_date((MediaInfo.parse(file).to_data().get('tracks')[j].get(
                                'file_last_modification_date').replace("UTC ", "")), min_data)
                        if ((MediaInfo.parse(file).to_data().get('tracks')[j].get(
                                'file_last_modification_date__local')) != None):
                            min_data = comparison_date((MediaInfo.parse(file).to_data().get('tracks')[j].get(
                                'file_last_modification_date__local').replace("UTC ", "")), min_data)
                        if ((MediaInfo.parse(file).to_data().get('tracks')[j].get('encoded_date')) != None):
                            min_data = comparison_date(
                                (MediaInfo.parse(file).to_data().get('tracks')[j].get('encoded_date').replace(
                                    "UTC ", "")), min_data)
                        if ((MediaInfo.parse(file).to_data().get('tracks')[j].get('tagged_date')) != None):
                            min_data = comparison_date(
                                (MediaInfo.parse(file).to_data().get('tracks')[j].get('tagged_date').replace(
                                    "UTC ", "")), min_data)
                # тут нужен обрабочек ошибок
                try:
                    if (min_data != None):
                        year = min_data[0:4]
                        month = min_data[5:7]
                        zz = info.dictionary_of_months.get(month)
                        lam_directory = new_directory + '\\' + year
                        if (os.path.exists(lam_directory) != True):
                            os.mkdir(new_directory + '/' + year)
                        lam_directory = new_directory + '\\' + year + '\\' + zz
                        if (os.path.exists(lam_directory) != True):
                            os.mkdir(new_directory + '/' + year + '/' + zz)
                        lam_directory = new_directory + '\\' + year + '\\' + zz
                        name_file = (old_directories[i].split('\\'))[len(old_directories[i].split('\\')) - 1]

                        def copy():
                            nonlocal lam_directory
                            if os.path.exists(lam_directory + '\\' + name_file):
                                lam_directory = lam_directory + '\\' + 'файлы с одиновым названием'
                                if os.path.exists(lam_directory) == False:
                                    os.mkdir(lam_directory)
                                copy()
                            return

                        copy()
                        shutil.copy2(old_directories[i], lam_directory)
                        if settings.del_file:
                            os.remove(old_directories[i])
                        if settings.print_consol:
                            plus()
                except:print(f'Не удалось записать файл - {file}')

        def comparison_date(date1, date2):
            # надо переисать эту штуку в человеческий вариант

            if date1 is None:
                return date2
            elif date2 is None:
                return date1

            if int(date1[0:4]) == 1980:
                return date2
            if int(date2[0:4]) == 1980:
                return date1
            if int(date1[0:4]) == 1970:
                return date2
            if int(date2[0:4]) == 1970:
                return date1
            if int(date2[0:4]) > 2022:
                return date1
            if int(date1[0:4]) > 2022:
                return date2




            date_time1 = datetime(int(date1[0:4]), int(date1[5:7]), int(date1[8:10]))
            date_time2 = datetime(int(date2[0:4]), int(date2[5:7]), int(date2[8:10]))
            if date_time1 < date_time2:
                return date1
            else:
                return date2


        def plus():
            nonlocal all_required_files
            nonlocal processed_files
            processed_files += 1
            print(f'Обработано файлов {processed_files}/{all_required_files}')

        if settings.thread == 1:
            copy_files_new_directory(sort_format_directory(settings.d1, settings.extension), settings.d2)
        elif settings.thread > 1:
            for info_file in (np.array_split(sort_format_directory(settings.d1, settings.extension), settings.thread)):
                b = list(info_file)
                th1 = Thread(target=copy_files_new_directory, args=(b, settings.d2))
                th1.start()
            th1.join()
        else:
            print('Недопустимое кол-во потоков')
    start()

