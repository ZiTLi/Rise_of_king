import random
import matplotlib.pyplot as plt

# Равномерное распределение
uniform_values = [random.uniform(0, 1) for _ in range(1000)]

# Нормальное распределение
gauss_values = [random.gauss(0, 1) for _ in range(1000)]

#Визуализация
plt.hist(uniform_values, bins=50, alpha=0.5, label='Uniform')
plt.hist(gauss_values, bins=50, alpha=0.5, label='Gauss')
plt.legend()
plt.show()