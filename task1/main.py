import math
from xml.dom import minidom
from matplotlib import pyplot as plt
import numpy


LEFT_BOLDER = -15.
RIGHT_BOLDER = 15.
STEP = 0.1
CONST_A = 1.34941
# создаем массивы для заполнения точками
x_t = []
y_t = []
def f_x(x):
    return -0.0001 * (math.fabs(math.sin(x) * math.sin(CONST_A) * math.exp(math.fabs(100 - (math.sqrt(x ** 2 + CONST_A ** 2) / math.pi)))) + 1) ** 0.1

root = minidom.Document()
root.toxml(encoding="utf-8")

xml = root.createElement('data')
root.appendChild(xml)

for x in numpy.arange(LEFT_BOLDER, RIGHT_BOLDER, STEP):
    tempRowX = root.createElement('x')

    tempRowY = root.createElement('y')
    productChild = root.createElement('row')
    productChild.appendChild(tempRowX)
    productChild.appendChild(tempRowY)
    
    # что бы два раза не считать f_x создадим временную переменную
    tempF_X = f_x(x)
    sizeX = root.createTextNode(str(x))

    x_t.append(float(x))
    y_t.append(float(tempF_X))
    sizeY = root.createTextNode(str(tempF_X))

    tempRowX.appendChild(sizeX)
    tempRowY.appendChild(sizeY)

    xml.appendChild(productChild)

xml_str = root.toprettyxml(indent="\t")

# используя matplotlib создаем график
plt.plot(x_t, y_t)
# Adding title, xlabel and ylabel
plt.title('')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()
save_path_file = "results.xml"

with open(save_path_file, "w") as f:
    f.write(xml_str)
