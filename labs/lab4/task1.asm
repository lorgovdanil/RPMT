; Программа для вывода "Hello World" на экран LC-3
.ORIG x3000        ; Начало программы

LEA R0, STRING     ; Загружаем адрес строки в R0
PUTS               ; Вывод строки на экран

HALT               ; Остановка программы

STRING .STRINGZ "Hello World" ; Определение строки

.END
