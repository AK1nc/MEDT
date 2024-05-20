import os
import sys
import xml.dom.minidom
from matplotlib import pyplot as plt
import wget
from sys import argv


# Устанавливаем дефолтное значение переменной file_name на случай запуска из програмных оболочек (я использовал pycharm)
if(len(argv) == 1):
    file_name = 'http://u1440187.isp.regruhosting.ru/EDM_lab/results.xml'
else:
    # если len(argv) > 1 значит в консоль были переданны данные, значит запускаем сценарий с вводом из консоли
    namef = sys.argv[1]
    file_name = 'http://u1440187.isp.regruhosting.ru/EDM_lab/' + namef
    print('Введенное имя файла: ' + str(sys.argv[1]))

print("Enter line thickness: ")
lineWidth = input()

x = []
y = []


try:
    # Обработка подгрузчика файла (здесь используем wget для только загрузки файла)
    wget.download(file_name)
    # Черед minidom подгружаем таблицу данных results.xml
    res = xml.dom.minidom.parse('results.xml')
    parX = res.getElementsByTagName('x')
    parY = res.getElementsByTagName('y')
except:
    parX = 0
    parY = 0
    print(-5)


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

#очищаем скаченый фал
os.remove('results.xml')
