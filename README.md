# differentiating_deep_neural_network

## Описание

Программа для обучения нейронной сети дифференцированию заданных выражений по одной переменной

Подготовлено в качестве выпускного задания по курсу "Практические методы разработки и реализации нейронных сетей. Продвинутый уровень" от ФГАОУ ВО "Северный (Арктический) федеральный университет имени М.В. Ломоносова" (https://cat.2035.university/rall/course/6450/)


### Подготовка данных для обучения 
Все используемые для работы выражения записываются в LaTex нотации с пробелом в качестве разделителя операторов  

* Данные для обучения формируются при запуске файла generating_of_the_dataset.py, который использует в своей работе шаблоны из файла dataset/template_formulas.txt и символы из файлов dataset/alphabet.txt и dataset/numbers.txt
* Результат генерации находится в файле dataset/differentiating_expressions.csv в формате Comma-Separated Values, где первый столбец - это переменная, второй - дифференцируемое выражение, третий - результат дифференцирования.
* Содержимое файла dataset/differentiating_expressions.csv пригодно для обучения (т.е. запускать generating_of_the_dataset.py не требуется)

Данные для обучения формируются в виде двух фраз:
1. Первая фраза подаётся на кодер. Начинается со служебного символа начала фразы <sos>, далее идёт переменная по которой проводится дифференцирование, после чего записывается дифференцируемое выражение. Фраза заканчивается служебным символом <eos>.
2. Вторая фраза представляет собой результат дифференцирования. Фраза начинается и заканчивается теми же служебными символами, что и предыдущая фраза.

### Модель

Используется модель типа seq2seq с включённым механизмом внимания. В качестве основы была взята версия https://www.tensorflow.org/tutorials/text/nmt_with_attention

Возможные улучшения этой модели:
1. В кодере использовать двунаправленный скрытый gru-слой
2. В модуле внимания увеличить количество элементов первого слоя исходя из количества элементов на крытых слоях кодера и декодера 

### Обучение

В цикле обучения на кодер подаётся первая фраза. На каждом этапе обработки фразы срытое состояния кодера подаётся в модуль внимания. После отработки кодера, скрытое состояния и результат работы модуля внимания подаются в декодер.
По результату вычисляется ошибка и производится оптимизация DNN.

Обучение на этапе работы декодера с вероятностью, определяемой величиной teacher_forcing_ratio, происходит по схеме "обучение, управляемое учителем", что значительно повышает сходимость.

### Проверка результата обучение

В разделе "Restore the latest checkpoint and test" приводится результат обучения модуля внимания. Приводится зависимость элементов второй фразы от первой.

В конце этого раздела приводится результат сравнения целевых выражений и выражений, выданный сеть. Сравнение осуществляется по схеме Bilingual Evaluation Understudy методом nltk.translate.bleu_scor.sentence_bleu  

### Демонстрация использования обученной DNN

В "человеческом" виде (а не в виде LaTex-выражений) результат работы сети можно посмотреть в разделе "Drawing"

Если запустить весь радел, то произойдёт установка в colab
1. Texlive - программы, необходимой для компиляции теховских файлов в pdf
2. Imagemagick - программа, необходимая для конвертации pdf в png файл.
После установки необходимо дать разрешение Imagemagick на чтения pdf фалов. Для этого служит команда
    
        %cp -i utils/policy.xml /etc/ImageMagick-6/
        
Обязательно дайте согласие!

После этих процедур будет происходить компиляция требуемых выражений и выражений, выдаваемых сетью.
Результаты будут отображаться в виде картинок и LaTex-выражений.