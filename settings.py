import body

d1 = r"D:\photo"  # от куда
d2 = r"D:\photo"  # куда
extension = 'jpg'  # с каким расширениемчасы
thread = 5  # сколько потоков задейсвовать
print_consol = True  # вывод кол-во обработанных файлов
del_file = False  # удалять исходные файлы
print_time_finish = True  # вывод времени работы программы

if __name__ == '__main__':
    body.main()
