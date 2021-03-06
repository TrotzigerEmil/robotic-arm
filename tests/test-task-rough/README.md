# Тесты

## Общие условия ##

Производится решение задачи, описываемой файлом files/test-task-rough.json. Установлено минимальное значение феромона, равное 1E-12 (т. е. ниже этого уровня феромон не опускается). Весовая функция возвращает длину шага сетки, если ребро существует, и +inf в противном случае.

## Наборы тестов ##

Существует набор параметров, называемый базовым. Остальные наборы параметров отличаются от базового лишь одним параметром. Параметр количества итераций остается постоянным и равен 100.

Обозначения параметров:
+ &alpha; - параметр, определяющий влияние кол-ва феромона на выбор;
+ &beta; - параметр, определяющий влияние веса ребра на выбор;
+ &gamma; - параметр, определяющий влияние направления движения относительно кратчайшего направления до конечной точки на выбор;
+ &phi; - начальный уровень феромона;
+ &rho; - скорость испарения феромона;
+ Q - количество феромона, откладываемое муравьем;
+ N - количество муравьев.

| № | &alpha; | &beta; | &gamma; | &phi; | &rho; | Q | N | i | Выполнен | Примечания |
|:- | ------: | -----: | ------: | ----: | ----: | -:| -:| -:| -------- | :--------- |
|0|1.0|1.0|0.0|1E-9|0.25|1.0|64|100|&#9745;|Базовый набор параметров|
