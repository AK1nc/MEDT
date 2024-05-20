import numpy as np
import matplotlib.pyplot as plt


# Задаем функцию
def f(x1, x2):
    return und_sum(x1) + und_sum(x2) - und_cos(x1, 1)*und_cos(x2, 2)
def und_sum(x):
    return (x**2)/4000
def und_cos(x, param):
    return np.cos(x/param**0.5) + 1

x1 = np.linspace(-10.0, 10.0, 500)
x2 = np.linspace(-10.0, 10.0, 500)
X1, X2 = np.meshgrid(x1, x2)
# формируем данные о значении функции по сформированным выше точкам
Y = f(X1, X2)


fig = plt.figure(figsize=(8, 8))


# создание 3х мерной поверхности
# добовляем subplot с настройкой 3д графика
plot1 = fig.add_subplot(221, projection='3d')
# задаем параметры графика
plot1.plot_surface(X1, X2, Y, cmap='viridis')
# задаем имя
plot1.set_title('трехмерный вид')
# называем оси
plot1.set_xlabel("x1", loc='right', labelpad = 1.)
plot1.set_ylabel("x2", labelpad = 1.)
plot1.set_zlabel("f(x1,x2)", labelpad = 0.5)


# Поверхность сверху
plot2 = fig.add_subplot(222)
plot2.contourf(X1, X2, Y, levels=50, cmap='viridis')
plot2.set_title('Поверхность сверху')
# называем оси
plot2.set_xlabel("x1", loc='right', labelpad = 1.)
plot2.set_ylabel("x2", labelpad = 0.5)

#увеличиваем колличество точек для плавности представления 2д графиков
x1 = np.linspace(-10.0, 10.0, 3000)
x2 = np.linspace(-10.0, 10.0, 3000)

# Построение рафика y = f(x1) когда x2 = 0
plot3 = fig.add_subplot(223)
plt.plot(x1, f(x1, 0))
plot3.set_title('y = f(x1) -> x2 = 0')
# называем оси
plot3.set_xlabel("x1", loc='right', labelpad = 1.)
plot3.set_ylabel("f(x1)", labelpad = 1.)

# Построение рафика y = f(x2) когда x1 = 0
plot4 = fig.add_subplot(224)
plt.plot(x2, f(0, x2))
plot4.set_title('y = f(x2) -> x1 = 0')
# называем оси
plot4.set_xlabel("x2", loc='right', labelpad = 1.)
plot4.set_ylabel("f(x2)", labelpad = 1.)

plt.tight_layout()
plt.show()