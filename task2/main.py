import os
import sys
import xml.dom.minidom
from matplotlib import pyplot as plt
import wget
from sys import argv


x = []
y = []


# Устанавливаем дефолтное значение переменной file_name на случай запуска из програмных оболочек (я использовал pycharm)
if(len(argv) == 1):
    #сдесь будем брать файл с моего внешнего сервера где он хранится
    file_name = 'http://u1440187.isp.regruhosting.ru/EDM_lab/results.xml'
    wget.download(file_name)
    file_name = 'results.xml'
else:
    # если len(argv) > 1 значит в консоль были переданны данные, значит запускаем сценарий с вводом из консоли
    namef = sys.argv[1]
    # если в консоль введено имя
    file_name = namef
    print('Введенное имя файла: ' + str(sys.argv[1]))

if(len(argv) == 3):
    # если в консоль был передан не обязательный параметр толщины линии
    lineWidth = sys.argv[2]
else:
    # если не обязательный параметр не был введен в консоль
    print("Enter line thickness: ")
    lineWidth = input()



# Черед minidom подгружаем таблицу данных results.xml
res = xml.dom.minidom.parse(file_name)
parX = res.getElementsByTagName('x')
parY = res.getElementsByTagName('y')



for s in parX:
    x.append(float(s.firstChild.nodeValue))
for l in parY:
    y.append(float(l.firstChild.nodeValue))
try:
    # используя matplotlib создаем график
    plt.plot(x, y, linewidth = lineWidth)
    # Adding title, xlabel and ylabel
    plt.title('')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.show()
except:
    print(-2)

# очищаем скаченый фал
# в случае если файл не скачивался, система не найдет такой файл и не вызвав ошибки ничего не очистит
os.remove('results.xml')
