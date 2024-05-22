import json
import os
import scipy.constants as constants
import scipy.special as special
import numpy as np
import xml.dom.minidom
import matplotlib.pyplot as plt
import wget


D = None
FMIN = None
FMAX = None
SP_LIGHT = 299792458 # meters per second

#обрабатываем событие скачивания
try:
    wget.download('https://jenyay.net/uploads/Student/Modelling/task_rcs.xml')
except:
    print(-1)

# парсить xml будем через minidom
res = xml.dom.minidom.parse('task_rcs.xml')

parsVariant = res.getElementsByTagName('variant')

# Находим нужный вариант и получаем значения
for s in parsVariant:
    temp = (float(s.getAttribute('number')))
    if(temp == 3):
        D = float(s.getAttribute('D'))
        FMIN = float(s.getAttribute('fmin'))
        FMAX = float(s.getAttribute('fmax'))

# Вывод проверки значений
print(D)
print(FMIN)
print(FMAX)

# Создаем вспомогательные переменные
#значение радиуса
R = float(D/2)
#значения разброса частот с шагом 10000
freq_range = range(int(FMIN) , int(FMAX), 100000)

#очищаем скаченый файл
os.remove('task_rcs.xml')


# Класс отвечает за рассчет ЭПР,
class CalculateEDA:
    def __init__(self, r, frequency):
        # в конструкторе задаем начальные переменные рассчета
        self.radius = r
        self.wave_length = 0
        self.k = 0
        self._freq_range_ = frequency

    def a_n(self, n):
        numerator = np.longdouble(special.spherical_jn(n, self.k * self.radius))
        divider = self.h_n(n, self.k * self.radius)
        return np.divide(numerator, divider)

    def b_n(self, n):
        numerator = self.k * self.radius * np.longdouble(special.spherical_jn(n - 1, self.k * self.radius)) - n * np.longdouble(special.spherical_jn(n, self.k * self.radius))
        divider = self.k * self.radius * self.h_n(n - 1, self.k * self.radius) - n * self.h_n(n, self.k * self.radius)
        return np.divide(numerator, divider)

    def h_n(self, n, arg):
        return np.clongdouble(special.spherical_jn(n, arg) + 1j*special.spherical_yn(n, arg))

    def EDA(self):
        coef = self.wave_length**2 / constants.pi
        partForml = 0
        # оператор суммы в формуле c верхним пределом 50
        for n in range(1, 50):
            partForml += (-1)**n * (n + 0.5) * (self.b_n(n) - self.a_n(n))
        result = coef * abs(partForml) ** 2
        return result

    # функция запускает процесс просчета для введеных границ частоты
    def calculateData(self):
        self.data = []
        for freq in self._freq_range_:
            # обновляем длину волны и волновое число
            self.wave_length = np.longdouble(constants.speed_of_light / freq)
            self.k = np.longdouble(2 * constants.pi / self.wave_length)
            # получаем значение ЭПР для новых параметров
            temp_eda = self.EDA()
            self.data.append({"freq": float(freq), "lambda": float(self.wave_length), "rcs": float(temp_eda)})
        return self.data

class Output:
    def __init__(self, data):
        # в данном случае в конструкторе нас интересует только передача массива с данными о точках
        self.data = data
    # функция дял создания графика
    def drawPlotData(self):
        freq = [d["freq"] for d in self.data]
        rcs = [d["rcs"] for d in self.data]
        plt.plot(freq, rcs)
        plt.ylabel('RCS')
        plt.xlabel('Frequency')
        plt.title('RCS from frequency')
        plt.grid()
        plt.show()
    def saveToJson(self, filename):
        with open(filename, 'w') as f:
            json.dump({"data": self.data}, f, indent=4)


# Создаем объект рассчета
calculator = CalculateEDA(R, freq_range)
data = calculator.calculateData()

# Содаем объект отвечающий за вывод
output = Output(data)
output.saveToJson('result.json')
output.drawPlotData()
