import body

d1 =r""  # от куда
d2 = r""  # куда
extension = 'jpg'  # с каким расширением
thread = 1  # сколько потоков задейсвовать
print_consol = False  # вывод кол-во обработанных файлов
del_file = False  # удалять исходные файлы
print_time_finish = True  # вывод времени работы программы

if __name__ == '__main__':
    body.main()

#могут вылетать в консоль ошибки, но они не влияют на работу