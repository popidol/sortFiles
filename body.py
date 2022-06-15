import os.path
import shutil
from threading import Thread
import numpy as np
import info
import time
import settings


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
                    # надо написать вызов только с нужными ключами
                    try:
                        info_file = info.info_file_exif(old_directories[i], False)
                        if ('datetime' in info_file) == True:
                            min_data = comparison_date(info_file.get('datetime'), min_data)
                        if ('datetime_original' in info_file) == True:
                            min_data = comparison_date(info_file.get('datetime_original'), min_data)
                        if ('datetime_digitized' in info_file) == True:
                            min_data = comparison_date(info_file.get('datetime_digitized'), min_data)
                        if ('gps_datestamp' in info_file) == True:
                            min_data = comparison_date(info_file.get('gps_datestamp'), min_data)
                    except:
                        min_data = None

                if min_data == None:
                    #нужно переписать в словарь только с этими ключами
                    info_file = info.info_file_pymediainfo(old_directories[i], False)
                    for j in range(0, len(info_file) - 2, 2):
                        if info_file[j] == ('file_creation_date' or \
                                            'file_creation_date__local' or \
                                            'file_last_modification_date' or \
                                            'file_last_modification_date__local' or \
                                            'encoded_date' or \
                                            'tagged_date'):
                            if (info_file[j + 1][0] == 'U'):
                                info_file[j + 1] = info_file[j + 1].replace("UTC ", "")
                            if (min_data == None):
                                min_data = info_file[j + 1]
                            else:
                                min_data = comparison_date(min_data, info_file[j + 1])

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

        def comparison_date(date1, date2):
            # надо переисать эту штуку в человеческий вариант
            if (date1 == None and date2 != None): return date2
            if (date2 == None and date1 != None): return date1
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

    t1 = time.time()
    start()
    t2 = time.time()
    info.time_counter(t1, t2)


