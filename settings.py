import body

d1 =r"F:\все"  # от куда
d2 = r"F:\photo\jpg"  # куда
extension = 'jpg'  # с каким расширением
thread = 5  # сколько потоков задейсвовать
print_consol = False  # вывод кол-во обработанных файлов
del_file = False  # удалять исходные файлы
print_time_finish = True  # вывод времени работы программы

if __name__ == '__main__':
    body.main()

#могут вылетать в консоль ошибки, но они не влияют на работу



# Exception in thread Thread-9 (copy_files_new_directory):
# Traceback (most recent call last):
#   File "C:\Program Files\Python310\lib\threading.py", line 1009, in _bootstrap_inner
#     self.run()
#   File "C:\Program Files\Python310\lib\threading.py", line 946, in run
#     self._target(*self._args, **self._kwargs)
#   File "C:\Users\krasnov\PycharmProjects\sortFhoto\body.py", line 80, in copy_files_new_directory
#     lam_directory = new_directory + '\\' + year + '\\' + zz
# TypeError: can only concatenate str (not "NoneType") to str