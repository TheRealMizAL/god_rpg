# God RPG - ЛУЧШИЙ В МИРЕ!111!!!!11 ДВИЖОК ДЛЯ ТЕКСТОВЫХ RPG НА БАЗЕ TELEGRAM!!!!!

## Особенности
- Собственный язык описания сценариев GRD (God RPG dialogue), точно не скопированный с RenPy!
- Поддержка Aiogram из коробки (потому что я других фреймворков для телеграм-ботов не знаю, лол)
- Ну вам жалко что-ли, просто скажите что фреймворк топ((((


## GRD Hello world
Язык сделан максимально похожим на обычный питоновский код, так что для старта необходимо просто выучить парочку новых ключевых слов!

Зачем это вообще надо? Да просто для того, чтобы не писать тонны текста прямо в коде! Просто опишите желаемую структуру диалога
с нужными вам ветвлениями и условиями, а движок все сделает за вас. И никаких файлов с ключами для каждой фразы!
```python
ch1 = Character('Character 1')
ch2 = Character('Character 2')


label main:
    say "some_line"  # say - base character without name
    show some_image
    play some_audio

    choice:
        one:
            jump label_1
        two:
            jump label_2
        three:
            pass  # same as python pass

    if expr != False:
        say "This line will be shown only if expr = True"
    say "Without \"return\" or \"jump\" you'll be sent to label_1"

label label_1:
    ch1 f"Hey, I'm {ch1}, you're in a label 1!"
    return

label label_2:
    ch2 f"Hey, I'm {ch2}, you're in a label 2!"
    return
```

## Roadmap
1) Закончить GRD компилятор
2) Создать минимальный функционал движка
3) Дальше пить пиво
