# time1 = "2022-06-12 01:14:44.945"
# time = "2018-01-05 10:12:36"
#
# time1 = time1[0:4]
# print(time1)
#
# win = ""
# year_array = []
# year = ""
# year1 = ""
# month_array = []
# month = ""
# month1 = ""
# day_array = []
# day = ""
# day1 = ""
#
# #год
#
# year_array.append(time[4])
# year_array.append(time[5])
# year_array.append(time[6])
# year_array.append(time[7])
# year = int(year.join(year_array))
# year_array.clear()
# year_array.append(time1[4])
# year_array.append(time1[5])
# year_array.append(time1[6])
# year_array.append(time1[7])
# year1 = int(year1.join(year_array))
# if (year == year1):
#     #месяц
#     month_array.append(time[9])
#     month_array.append(time[10])
#     month = int(month.join(month_array))
#     month_array.clear()
#     month_array.append(time1[9])
#     month_array.append(time1[10])
#     month1 = int(month1.join(month_array))
#     if (month == month1):
#         # день
#         day_array.append(time[12])
#         day_array.append(time[13])
#         day = int(day.join(day_array))
#         day_array.clear()
#         day_array.append(time1[12])
#         day_array.append(time1[13])
#         day1 = int(day1.join(day_array))
#         if(day == day1):print("Одинаковые")
#         elif (day < day1):win = time
#         elif (day > day1):win = time1
#     elif (month < month1):win = time
#     elif (month > month1):win = time1
# elif (year < year1):win = time
# elif (year > year1):win = time1
#
#
#