##-- библиотеки отрисовки
from tkinter import *
from tkinter import font
from tkinter import ttk

##--<4>-- библиотеки диалоговых окон
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

##--<4>--  библиотеки для связи
import threading
from time import *
from socket import *

##-- вспомогательные библиотеки
import winsound
import inspect

# == переменные

##-- параметры доски
left_desk = 50  # -- положение левого нижнего угла доски
bottom_desk = 450
cell_size = 50  # -- размер клетки доски
desk_size = 8 * cell_size  # -- размер шахматной доски
flg_vid = 0  # -- вид доски: 0 - бедые внизу, 1 - черные внизу

##-- цвета элементов оформления
rect_colors = ["#8D89AF", "#EFEF8E"]
root_color = "thistle"  # -- цвет формы
sel_color = "red"
box_color = "pink"
col_names = "ABCDEFGH"
row_names = "12345678"

##-- списки тэгов фигур
whitefig_tags = ["wll", "whl", "wsb", "wfr", "wkr", "wsw", "whr", "wlr"]
blackfig_tags = ["bll", "bhl", "bsw", "bfr", "bkr", "bsb", "bhr", "blr"]

##-- списки фигур (элемент описания:   [ tag, img, adr ])
white_figs = []  # -- список активных белых фигур
black_figs = []  # -- список активных черных фигур

white_deleted = []  # -- список удаленных белых
black_deleted = []  # -- список удаленных черных

##-- вспомогательные переменные
btn_width = 14  # -- размер кнопок
photo_images = []
sound_mode = "off"  # --режим вкюченного звука

##-- переменные для индикации хода
sel_adr = ""  # -- выбранный адрес
sel_fignum = -1  # -- номер выбранной фигуры
sel_figlist = []  # -- список выбранной фигуры

##--переменные для записи ходов-
step_log = []  # -- лог ходов
step_num = 0  # -- внутренний номер хода
record_flag = 0  # -- признак режима записи ходов в лог(1/0)

##--<4>-- сетевые переменные
server_address = ('', 5400)  # -- например: ('10.1.0.180', 5400)
ip_partn = ""  # -- IP адрес партнера
net_mode = "local"  # -- режим работы клиента( "connect" при сетевой игре)
main_tau = 20  # -- время цикла главной программы в мс
lst_in = []  # -- очередь для принятых сообщений
busy_in = 0  # -- признак занятости очереди


# == общие функции
##--  print_funcname - вывести имя текущей функции
def print_funcname():
    print(inspect.stack()[1][3])


# == геометрические функции
##-- получить координаты на доске или в коробке по адресу
def adr2rowcol(adr):
    if len(adr) == 2:
        col = col_names.find(adr[0])
        row = row_names.find(adr[1])
        if flg_vid == 1: col = 7 - col;  row = 7 - row
    else:
        row = col_names.find(adr[1])
        col = int(adr[2]) + 9
        # col = col_names.find( adr[1] ) + 10
        # row = int(adr[2])-1
        if col > 12:
            col -= 4
    # print( "adr2rowcol:adr, row, col = ", adr, row, col)
    return row, col


##-- получить адрес по координатам на доске
def rowcol2adr(row, col):
    if row < 0 or row > 7:  # -- слишком ниэко или высоко
        return ""

    if 0 <= col < 8:  # -- мы на доске
        if flg_vid == 1: col = 7 - col;  row = 7 - row
        adr = col_names[col] + row_names[row]
    elif 10 <= col < 12:
        # adr = "d" + col_names[col-10]+ row_names[row]
        adr = "d" + col_names[row] + str(col - 9)
    elif 12 <= col < 14:
        # adr = "d" + col_names[col-6]+ row_names[row]
        adr = "d" + col_names[row] + str(col - 5)
    else:
        adr = ""
    return adr


##-- получить адрес по событию
def event2adr(event):
    row = (bottom_desk - event.y) // cell_size
    col = (event.x - left_desk) // cell_size
    # print( "event2adr:row,col = ", row, col )
    return rowcol2adr(row, col)


##-- получить координаты рисунка на доске по адресу
def adr2imagecoord(adr):
    row, col = adr2rowcol(adr)
    # print("adr2img2coord adr, row, col: ", adr, row,col)
    image_x = left_desk + (col + 0.5) * cell_size
    image_y = bottom_desk - (row + 0.5) * cell_size
    return image_x, image_y


# == функции для фигуры

##-- изменить цвет квадрата по его адресу
def set_rectcolor(adr, color):
    if adr == "":  return
    row, col = adr2rowcol(adr)
    if len(adr) == 2:
        tag = "r" + str(row) + str(col)
    else:
        tag = "dr" + str(row) + str(col)
    # print( row, col,", tag = ",tag)
    canv.itemconfig(tag, fill=color)


##-- подсветить квадрат
def set_rectbright(adr):
    set_rectcolor(adr, sel_color)


##-- вернуть фоновый цвет квадрата
def set_rectfon(adr):
    if len(adr) == 3:
        color = box_color
    elif len(adr) == 2:
        row, col = adr2rowcol(adr)
        color = rect_colors[(row + col) % 2]
    set_rectcolor(adr, color)


##-- сформировать начальный адрес по имени фигуры
def init_adr(fig_name):
    if fig_name in whitefig_tags:
        fig_index = whitefig_tags.index(fig_name)
        adr = col_names[fig_index] + "1"
    elif fig_name[:2] == "wp":
        fig_index = int(fig_name[2])
        adr = col_names[fig_index] + "2"
    elif fig_name in blackfig_tags:
        fig_index = blackfig_tags.index(fig_name)
        adr = col_names[fig_index] + "8"
    elif fig_name[:2] == "bp":
        fig_index = int(fig_name[2])
        adr = col_names[fig_index] + "7"
    else:
        adr = ""
    return adr


##-- передвинуть фигуру на заданную позицию доски или в коробку
def move_fig(fig, adr):
    global white_figs, black_figs, white_deleted, black_deleted
    if adr == "":  return
    fig_name, fig_img, fig_adr = fig
    fig_list = white_figs if fig_name[0] == "w" else black_figs
    del_list = white_deleted if fig_name[0] == "w" else black_deleted

    step_text = ""  # --<3>--
    if len(adr) == 2 and len(fig_adr) == 2:  # -- движение в пределах доски
        stepfig_dict = {"l": "Л", "h": "К", "s": "С", "f": "Ф", "k": "Кр", "p": ""}
        step_text = stepfig_dict[fig_name[1]] + fig_adr + "-" + adr
        pass
    elif len(adr) == 3 and len(fig_adr) == 2:  # -- снять с доски в коробку
        adr = "d" + init_adr(fig_name)
        fig_list.remove(fig)
        del_list.append(fig)

    elif len(adr) == 2 and len(fig_adr) == 3:  # -- вынуть из коробки на доску
        del_list.remove(fig)
        fig_list.append(fig)
    '''    
    fig[2] = adr
    image_x, image_y = adr2imagecoord(adr)
    canv.coords(fig_img, image_x, image_y)
    '''
    set_figpos(fig, adr)  # --<3>--
    return step_text


##-- получить фигуру (и список)  по ее адресу
def get_fignumlist(adr):
    if len(adr) == 2:
        for fig_list in [white_figs, black_figs]:
            for num in range(len(fig_list)):
                fig = fig_list[num]
                if fig[2] == adr:  return num, fig_list
    elif len(adr) == 3:
        for fig_list in [white_deleted, black_deleted]:
            for num in range(len(fig_list)):
                fig = fig_list[num]
                if fig[2] == adr:  return num, fig_list
    return (-1, [])


##-- выбрать фигуру по шелчку на ней (возвращает adr, fig, fig_list)
def select_fig(event):
    adr = event2adr(event)
    if adr == "":
        return ("", [], [])
    fig_num, fig_list = get_fignumlist(adr)
    return (adr, fig_num, fig_list)


##-- загрузить фигуру из файла
def load_fig(fig_name, adr):
    global photo_images
    # print_funcname()

    file_name = ".\\png\\" + fig_name[:2] + ".png"

    image_x, image_y = adr2imagecoord(adr)
    try:
        photo_image = PhotoImage(file=file_name)
        photo_images.append(photo_image)
        image = canv.create_image(image_x, image_y, image=photo_image)

        return [fig_name, image, adr]
    except:
        print("path error: ", file_name)
        return []


##--<4>-- показать ход в логе и передать партнеру в сетевом режиме
def disp_step(step_text):
    print(step_text)
    write_step(step_text)
    if net_mode == "connect":
        send_mess("step|" + step_text)


##-- выполнить ход фигуры по щелчку
def sel_field(event):
    global sel_adr, sel_fignum, sel_figlist
    adr, fig_num, fig_list = select_fig(event)
    # print( "sel_adr = ", sel_adr, ", adr = ", adr)

    if adr == "":  # -- щелкнули мимо коробки и доски просто снять выбор
        if len(sel_adr) == 2:
            set_rectfon(sel_adr)
            sel_adr = ""
            sel_fignum = -1
            sel_figlist = []
        return
    # -- новый адрес правильный
    if len(sel_adr) == 0 and fig_num < 0:
        # -- щелчок по пустой клетке без предварительного выбора
        return

    elif len(sel_adr) == 0 and fig_num >= 0:
        # -- просто выбрать фигуру и клетку, если там что-то стоит
        sel_adr, sel_fignum, sel_figlist = adr, fig_num, fig_list
        set_rectbright(sel_adr)
        return

    elif len(sel_adr) != 0 and fig_num < 0:
        # -- фигура была выбрана, новая клетка пуста - переместить
        fig = sel_figlist[sel_fignum]

        # --<3>-- проверить и отработать возможную рокировку
        step_text = move_fig(fig, adr)
        if record_flag == 1:
            disp_step(step_text)

        # -- отменить предыдущий выбор
        set_rectfon(sel_adr)
        sel_adr = ""
        sel_fignum = -1
        sel_figlist = []
        if sound_mode == "on":
            canv.after(10, step_sound)
        return

    elif len(sel_adr) != 0 and fig_num >= 0:
        # -- фигура была выбрана, новая клетка занята
        if len(adr) == 2 and len(sel_adr) == 2:
            # -- запрещено есть свою фигуру- перевыбираем ???
            if sel_figlist == fig_list:
                set_rectfon(sel_adr)
                sel_adr, sel_fignum, sel_figlist = adr, fig_num, fig_list
                set_rectbright(sel_adr)
                return
            # -- съесть фигуру соперника:
            prev_fig = fig_list[fig_num]
            res = move_fig(prev_fig, "dA1")
            # -- поставить свою на ее место
            fig = sel_figlist[sel_fignum]
            step_text = move_fig(fig, adr)  # --<3>--
            step_text = step_text.replace("-", ":")
            if record_flag == 1:
                disp_step(step_text)
            # -- отменить предыдущий выбор
            set_rectfon(sel_adr)
            sel_adr = ""
            sel_fignum = -1
            sel_figlist = []
            if sound_mode == "on":
                canv.after(10, step_sound)
            return

        elif len(adr) == 3 and len(sel_adr) == 2:
            # -- снять фигуру с доски
            fig = sel_figlist[sel_fignum]
            move_fig(fig, adr)
            # -- отменить предыдущий выбор
            set_rectfon(sel_adr)
            sel_adr = ""
            sel_fignum = -1
            sel_figlist = []
            return


##-- получить фигуру по ее имени
def get_figbyname(fig_name):
    fig_list = white_figs if fig_name[0] == "w" else black_figs
    for num in range(len(fig_list)):
        fig = fig_list[num]
        if fig[0] == fig_name:  return fig
    return []


##-- установить положение фигуры на доске
def set_figpos(fig, adr):
    fig[2] = adr
    image_x, image_y = adr2imagecoord(adr)
    canv.coords(fig[1], image_x, image_y)


##-- смена адреса фигуры в пределах доскибез проверок на ошибку
def jump_figondesk(beg_adr, end_adr):
    fig_num, fig_list = get_fignumlist(beg_adr)
    fig = fig_list[fig_num]
    set_figpos(fig, end_adr)


##-- очистить выбранную фигуру
def clear_sel():
    global sel_adr, sel_fignum, sel_figlist
    sel_adr = ""
    sel_fignum = -1
    sel_figlist = []


# == функции для доски
##--<4>-- очистить доску
def clear_sound():
    winsound.PlaySound("clear.wav", winsound.SND_FILENAME)


def clear_desk():
    for fig_num in range(len(white_figs) - 1, -1, -1):
        fig = white_figs[fig_num]
        move_fig(fig, "dA1")

    for fig_num in range(len(black_figs) - 1, -1, -1):
        fig = black_figs[fig_num]
        move_fig(fig, "dA1")

    if sound_mode == "on":
        canv.after(10, clear_sound)


##-- начальная расстановка
def init_desk():
    clear_desk()
    for fig_num in range(len(white_deleted) - 1, -1, -1):
        fig = white_deleted[fig_num]
        adr = fig[2][1:]
        move_fig(fig, adr)

    for fig_num in range(len(black_deleted) - 1, -1, -1):
        fig = black_deleted[fig_num]
        adr = fig[2][1:]
        move_fig(fig, adr)


##-- перерисовать сомволы по краям доски
def redraw_edge():
    canv.delete("let")
    # -- нарисовать нумерацию строк
    for row in range(8):
        x1 = left_desk - 15
        y1 = bottom_desk - (row + 0.5) * cell_size
        edge_text = str(row + 1) if flg_vid == 0 else str(8 - row)
        canv.create_text(x1, y1, text=edge_text, font=dFont, tag="let")
        canv.create_text(x1 + 430, y1, text=edge_text, font=dFont, tag="let")

    # -- нарисовать обозначения колонок
    for col in range(8):
        x1 = left_desk + (col + 0.5) * cell_size
        y1 = bottom_desk + 15
        edge_text = col_names[col] if flg_vid == 0 else col_names[7 - col]
        canv.create_text(x1, y1, text=edge_text, font=dFont, tag="let")
        canv.create_text(x1, y1 - 430, text=edge_text, font=dFont, tag="let")


##-- перерисовать доску, фигуры и пешки на доске
def redraw_desk():
    redraw_edge()
    for num in range(len(white_figs)):
        fig = white_figs[num]
        adr = fig[2]
        move_fig(fig, adr)
    for num in range(len(black_figs)):
        fig = black_figs[num]
        adr = fig[2]
        move_fig(fig, adr)


##-- нарисовать доску
def draw_desk():
    for row in range(8):
        global rects
        for col in range(8):
            x1 = left_desk + col * cell_size
            y1 = bottom_desk - row * cell_size
            x2 = x1 + cell_size
            y2 = y1 - cell_size
            rect_color = rect_colors[(row + col) % 2]
            rect = canv.create_rectangle(x1, y1, x2, y2, fill=rect_color,
                                         tag="r" + str(row) + str(col))
    redraw_edge()
    ##== нарисовать внешний край доски
    canv.create_rectangle(left_desk - 30, bottom_desk + 30, left_desk + 430, bottom_desk - 430)


##-- нарисовать места для срубленных фигур
def draw_figbox():
    for row in range(8):
        global rects
        for col in range(4):
            x1 = left_desk + col * cell_size + 500
            y1 = bottom_desk - row * cell_size
            x2 = x1 + cell_size
            y2 = y1 - cell_size
            rect = canv.create_rectangle(x1, y1, x2, y2, fill="pink",
                                         tag="dr" + str(row) + str(col + 10))


##-- загрузить и отрисовать фигуры с пешками
def load_allfigs():
    for col in range(8):
        white_adr = col_names[col] + "1"
        fig_name = whitefig_tags[col]
        fig = load_fig(fig_name, white_adr)
        white_figs.append(fig)

        black_adr = col_names[col] + "8"
        fig_name = blackfig_tags[col]
        fig = load_fig(fig_name, black_adr)
        black_figs.append(fig)

    for col in range(8):
        white_adr = col_names[col] + "2"
        fig_name = "wp" + str(col)
        fig = load_fig(fig_name, white_adr)
        white_figs.append(fig)

        black_adr = col_names[col] + "7"
        fig_name = "bp" + str(col)
        fig = load_fig(fig_name, black_adr)
        black_figs.append(fig)


# == функции для списка ходов
##-- очистить список ходов
def clear_log():
    global step_log, step_num, record_flag
    lbx_log.delete(0, END)
    step_log = []
    step_num = -1
    record_flag = 0
    btn_writemode["text"] = "Включить запись"


##-- загрузить список ходов
def load_log():
    global step_log, step_num, record_flag
    clear_log()
    clear_sel()

    record_flag = 0
    btn_writemode["text"] = "Включить запись"

    # -- выбрать файл из диалогового окна
    file_log = filedialog.askopenfilename(initialdir=".", title="Select logfile",
                                          filetypes=(("log files", "*.log"), ("all files", "*.*")))
    if len(file_log) < 1:  return

    # -- прочитать из него список строк с ходами
    print(file_log)
    fhn = open(file_log)
    file_lines = fhn.readlines()
    fhn.close()

    # -- подготовить и вывести ходы в листбокс
    for line in file_lines:
        line = line.upper()
        parts = line.split()
        for num, part in enumerate(parts):
            step = part if num == 0 else "             " + part
            lbx_log.insert(END, step)

    step_num = select_logstep(0)


##-- выбрать строку в спискек ходов
def select_logstep(index):
    try:
        lbx_log.select_clear(0, "end")
        lbx_log.selection_set(index)
        lbx_log.see(index)
        lbx_log.activate(index)
        lbx_log.selection_anchor(index)
        return index
    except:
        return -1


##-- сохранить список ходов в файл
def save_log():
    # -- выбрать файл из диалогового окна
    clear_sel()
    file_log = filedialog.asksaveasfilename(initialdir=".", title="Select logfile",
                                            filetypes=(("log files", "*.log"), ("all files", "*.*")))
    if len(file_log) < 1:  return
    if "." not in file_log:
        file_log += ".log"

    # -- подготовить список ходов листбокса для записи
    lst = list(lbx_log.get(0, END))
    text = ""
    for num in range(len(lst)):
        step = lst[num].strip()
        part = step if num % 2 == 0 else " " + step + "\n"
        text += part
    if len(lst) % 2 == 1:  text += "\n"

    # -- записать список ходов в файл
    fhn = open(file_log, "w")
    fhn.write(text)
    fhn.close()

    clear_log()


##--<4>-- выполнить ход из листбокса лога
def step_sound():
    winsound.PlaySound("step.wav", winsound.SND_FILENAME)


def make_step():
    global record_flag

    print("make_step")
    # -- получить номер текущего хода и выполнить сам ход
    try:
        step_index = lbx_log.curselection()[0]
        step_text = lbx_log.get(step_index)
    except:
        step_index = -1
        return
    # -- определить цвет фигур по отступу
    fig_color = "b" if step_text[0] == " " else "w"
    # -- определить ти хода и отработать его
    if "0-0-0" in step_text:  # -- длинная рокировка
        if fig_color == "w":  # -- длинная за белых
            jump_figondesk("E1", "C1")
            jump_figondesk("A1", "D1")
        else:  # -- длинная за черных
            jump_figondesk("E8", "C8")
            jump_figondesk("A8", "D8")

    elif "0-0" in step_text:  # -- короткая рокировка
        if fig_color == "w":  # -- длинная за белых
            jump_figondesk("E1", "G1")
            jump_figondesk("H1", "F1")
        else:  # -- длинная за черных
            jump_figondesk("E8", "G8")
            jump_figondesk("H8", "F8")

    elif ":" in step_text:  # -- взятие фигуры
        # -- определить начальный и конечный адреса
        delim_pos = step_text.index(":")
        adr_src = step_text[delim_pos - 2:delim_pos]
        adr_dst = step_text[delim_pos + 1:delim_pos + 3]
        # -- съесть фигуру соперника:
        fig_num, fig_list = get_fignumlist(adr_dst)
        prev_fig = fig_list[fig_num]
        res = move_fig(prev_fig, "dA1")
        # -- переместить свою фигуру
        jump_figondesk(adr_src, adr_dst)

    elif "-" in step_text:  # -- простой ход
        # -- определить начальный и конечный адреса
        delim_pos = step_text.index("-")
        adr_src = step_text[delim_pos - 2:delim_pos]
        adr_dst = step_text[delim_pos + 1:delim_pos + 3]
        # -- переместить свою фигуру
        jump_figondesk(adr_src, adr_dst)
    else:  # -- ошибка в нотации
        print("error: step_index, step_text = ", step_index, step_text)
    if sound_mode == "on":
        canv.after(10, step_sound)
    # -- перейти к следующему ходу
    step_index += 1
    select_logstep(step_index)


##-- записать ход в листбокс лога
def write_step(step_text):
    num = lbx_log.size()
    if num % 2 == 0:
        step = str(int(num // 2) + 1) + "." + step_text
    else:
        step = "             " + step_text
    lbx_log.insert(END, step)

    if net_mode == "connect":
        change_nextcolor()
        # end_mess("step|"+step)


# ==<4>== сетевые функции
##-- вывести принятое сообщение на консоль
def disp_mess(mess):
    print(mess)


##---  отправить сообщение по ТСР
def send_mess(mess):
    client = socket(AF_INET, SOCK_STREAM)
    bin_mess = bytes(mess, 'UTF-8')
    try:
        client.connect(server_address)
        client.sendall(bin_mess)
        # --<2>-- res = "OK"
        res = " "
    except:
        # --<2>--res = "not connected"
        res = "СЕРВЕР ВЫКЛЮЧЕН :("
    finally:
        client.close()
    return res


##-- аккуратно записать сообщение в очередь сообщений
def put_mess(mess):
    global lst_in, busy_in
    while busy_in:
        sleep(0.001)
    busy_in = 1
    lst_in.append(mess)
    busy_in = 0


##--- функция приема сообщений в потоке приема ( один пакет за  раз )
def work_in():
    global lst_in
    global busy_in
    locserv_addr = ('0.0.0.0', 5400)  # Сокет будет слушать все интерфейсы
    loc_sock = socket(AF_INET, SOCK_STREAM)
    loc_sock.bind(locserv_addr)  # связать с номером порта локального сервера
    loc_sock.listen(5)  # не более 5 ожидающих запросов

    while True:
        # -- ждать и получить сообщение от игрового сервера
        # --<2>--  print( "ready")
        connection, address = loc_sock.accept()
        # --<2>--  print('connected by', address)
        bin_data = connection.recv(1024)
        str_data = bin_data.decode("utf-8")
        # --<2>--  print( str_data )
        connection.close()

        # -- записать его в очередь сообщений
        put_mess(address[0] + "|" + str_data)

        # -- задержка потока
        sleep(0.001)


##-- отработать приглашение от партнера
def hndl_invite(lst_mess):
    global net_mode, ip_partn, flg_vid, record_flag, partn, server_address
    partn = lst_mess[2]
    MsgBox = messagebox.askquestion('Вас приглашаент ' + partn, 'Согласны сыграть?', icon='question')
    winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    # -- уточнить свой ник при отсутствии
    nick = var_nick.get()
    if not nick:
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        nick = simpledialog.askstring("замечание", "введите Ваш Ник ")

        var_nick.set(nick)

    if MsgBox == 'yes':
        net_mode = "connect"
        var_netmode.set("Сетевой")
        var_partn.set(partn)
        ip_partn = lst_mess[0]
        server_address = (ip_partn, 5400)
        init_desk()
        flg_vid = 1
        redraw_desk()
        clear_log()
        record_flag = 1
        var_next.set("Белые")
        res = send_mess("agree|" + nick)
    else:
        res = send_mess("refuse|" + nick)


##-- отработать согласие на игру от партнера
def hndl_agree(lst_mess):
    global net_mode, ip_partn, flg_vid, record_flag, partn
    partn = lst_mess[2]
    var_partn.set(partn)
    ip_partn = lst_mess[0]

    MsgBox = messagebox.showinfo("ответ: ", partn + ' согласен, начинаем игру', icon='warning')
    net_mode = "connect"
    var_netmode.set("Сетевой")
    flg_vid = 0
    init_desk()
    clear_log()
    record_flag = 1
    var_partn.set(partn)
    var_next.set("Белые")


##-- отработать отказ партнера от игры
def hndl_refuse(lst_mess):
    global net_mode, ip_partn, flg_vid, record_flag, partn
    partn = lst_mess[2]
    var_partn.set(partn)
    ip_partn = lst_mess[0]
    MsgBox = messagebox.showinfo("ответ: ", partn + ' отказался от игры :(', icon='warning')
    net_mode = "local"
    var_netmode.set("Локальный")
    record_flag = 0
    ip_partn = ""
    partn = ""
    var_partn.set(partn)


##-- отработать ход партнера
def hndl_step(lst_mess):  # --  ход = lst_mess[2]
    # -- записать ход партнера в список ходов и выполнить его
    step_text = lst_mess[2]
    write_step(step_text)
    select_logstep(END)
    make_step()


##-- изменить цвет фигур следующего хода
def change_nextcolor():
    cur_color = var_next.get()
    if cur_color == "Белые":
        var_next.set("Черные")
    else:
        var_next.set("Белые")


##-- главная функция, запускаемая в цикле
def main():
    global lst_in
    global busy_in

    ##-- проверить и вывести данные из очереди строк
    if len(lst_in) > 0:
        while busy_in:
            sleep(0.001)
        busy_in = 1
        str_in = lst_in.pop(0)
        busy_in = 0

        disp_mess(str_in)

        # -- обработать полученное сообщение
        lst_mess = str_in.split("|")
        if net_mode == "local":
            if lst_mess[1] == 'invite':
                hndl_invite(lst_mess)  # -- отработать приглашение
            elif lst_mess[1] == 'agree':
                hndl_agree(lst_mess)  # -- отработать согласие партнера
            elif lst_mess[1] == 'refuse':
                hndl_refuse(lst_mess)  # -- отработать отказ партнера
        elif net_mode == "connect" and ip_partn == lst_mess[0]:
            if lst_mess[1] == 'refuse':
                hndl_refuse(lst_mess)  # -- отработать отказ партнера от игры
            elif lst_mess[1] == 'step':
                hndl_step(lst_mess)  # -- отработать согласие партнера
    ##-- перезапуститься после задержки
    root.after(main_tau, main)


# == сформировать канву
root = Tk()
root.resizable(width=False, height=False)
dFont = font.Font(family="helvetica", size=12)
stl = ttk.Style()

root.configure(background=root_color)
stl.configure('.', font=dFont, background=root_color, foreground="black")

# ==<4>== элементы управления сетью
ttk.Label(root, text='Ваше имя:').grid(row=0, column=0, sticky=E, padx=5)

##-- поле вашего Ника
var_nick = StringVar()
var_nick.set("")
edt_nick = ttk.Entry(root, width=btn_width, textvariable=var_nick, font=dFont)
edt_nick.grid(row=0, column=1, padx=5, pady=5, sticky=W)

ttk.Label(root, text='Партнер:').grid(row=0, column=2, sticky=E, pady=5)

##-- поле ника и IP адреса пратнера
var_partn = StringVar()
var_partn.set("")
edt_partn = ttk.Entry(root, width=btn_width, textvariable=var_partn, font=dFont)
edt_partn.grid(row=0, column=3, padx=5, pady=5, sticky=W)

ttk.Label(root, text='режим игры:').grid(row=0, column=4, sticky=E, pady=5)

##-- поле режима игры
var_netmode = StringVar()
var_netmode.set("Локальный")
edt_netmode = ttk.Entry(root, width=btn_width, textvariable=var_netmode, font=dFont)
edt_netmode.grid(row=0, column=5, padx=5, pady=5, sticky=W)

ttk.Label(root, text='Очередь хода:').grid(row=1, column=0, sticky=E, padx=5)

##-- поле вашего Ника
var_next = StringVar()
var_next.set("")
edt_next = ttk.Entry(root, width=btn_width, textvariable=var_next, font=dFont)
edt_next.grid(row=1, column=1, padx=5, pady=5, sticky=W)


##-- кнопка приглашения партнера
def fnc_invite():
    global ip_partn, server_address, net_mode, flg_vid, record_flag
    # -- блокировать в режиме сетевой игры
    if net_mode == "connect":  return

    # -- отработать ошибку заполнения ника и ip_partn
    nick = var_nick.get()
    ##--ip_partn = var_partn.get()
    print(ip_partn, nick)
    ip_partn = simpledialog.askstring("замечание", "введите IP-адрес партнера", initialvalue=ip_partn)
    if not nick:
        nick = simpledialog.askstring("замечание", "введите Ваш Ник ")
        var_nick.set(nick)

    # -- отправить партнеру команду "invite|nick"
    server_address = (ip_partn, 5400)
    print(server_address)
    res = send_mess("invite|" + nick)
    print(res)
    if len(res) > 2:
        messagebox.showinfo("Ошибка связи :(", res)


ttk.Button(root, text="Пригласить", width=btn_width,
           command=fnc_invite).grid(row=1, column=3, sticky=W, pady=5, padx=5)


##-- кнопка отказа от сети
def fnc_refuse():
    global ip_partn, server_address, net_mode
    # -- блокировать в локальном режиме
    if net_mode == "local":  return

    # -- переключиться в локальный режим
    res = send_mess("refuse|nick")
    # ip_partn = " "
    var_partn.set("")
    server_address = ("", 0000)
    net_mode = "local"
    var_netmode.set("Локальный")


ttk.Button(root, text="Отключиться", width=btn_width,
           command=fnc_refuse).grid(row=1, column=5, sticky=W, pady=5, padx=5)

# == панель с канвой
pnl_left = Frame(root)
pnl_left.grid(row=2, column=0, columnspan=6, rowspan=10, pady=10, padx=10)

canv = Canvas(pnl_left, width=desk_size + 400, height=desk_size + 100)  # , background = 'pink')
canv.pack()


##-- вспомогательный обработчик для канвы
def disp_rowcol(event):
    adr = event2adr(event)
    row, col = adr2rowcol(adr)
    tag = "r" + str(row) + str(col)

canv.bind("<Button-3>", disp_rowcol)

##-- обработать щелчок по полю доски
canv.bind("<Button-1>", sel_field)

# == правая панель с кнопками
pnl_right = Frame(root, background=root_color)
pnl_right.grid(row=2, column=8, columnspan=2)


##-- вывести сообщение о блокировке в сетевом режиме
def block_bynet():
    messagebox.showinfo("блокировка: ", "в сетевом режиме не работает :(", icon='warning')


##-- кнопка очистки доски
def fnc_clear():
    if net_mode == "connect":
        block_bynet()
        return
    clear_desk()


ttk.Button(pnl_right, text="Очистить доску", width=btn_width,
           command=fnc_clear).grid(row=1, column=0,
                                   sticky=N, pady=5, padx=5)


##-- кнопка новой игры
def fnc_init():
    if net_mode == "connect":
        block_bynet()
        return
    init_desk()


ttk.Button(pnl_right, text="Новая игра", width=btn_width,
           command=fnc_init).grid(row=2, column=0,
                                  sticky=N, pady=5, padx=5)


##-- кнопка перевернуть доску
def fnc_rotatedesk():
    global flg_vid

    if net_mode == "connect":
        block_bynet()
        return

    flg_vid = 1 if flg_vid == 0 else 0
    redraw_desk()


ttk.Button(pnl_right, text="Повернуть доску", width=btn_width,
           command=fnc_rotatedesk).grid(row=3, column=0,
                                        sticky=N, pady=5, padx=5)


##-- кнопка очистки списка ходов
def fnc_clearlog():
    if net_mode == "connect":
        block_bynet()
        return
    clear_log()


ttk.Button(pnl_right, text="Очистить лог", width=btn_width,
           command=fnc_clearlog).grid(row=5, column=0,
                                      sticky=N, pady=5, padx=5)


##-- кнопка загрузки партии
def fnc_loadlog():
    if net_mode == "connect":
        block_bynet()
        return
    load_log()


ttk.Button(pnl_right, text="Загрузить лог", width=btn_width,
           command=fnc_loadlog).grid(row=6, column=0,
                                     sticky=N, pady=5, padx=5)


##-- кнопка сохранения ходов партии
def fnc_savelog():
    if net_mode == "connect":
        block_bynet()
        return
    save_log()


ttk.Button(pnl_right, text="Записать лог", width=btn_width,
           command=fnc_savelog).grid(row=7, column=0,
                                     sticky=N, pady=5, padx=5)


##-- кнопка выполнения текущего хода партии
def fnc_makestep():
    if net_mode == "connect":
        block_bynet()
        return
    make_step()


ttk.Button(pnl_right, text="Выполнить ход", width=btn_width,
           command=fnc_makestep).grid(row=8, column=0,
                                      sticky=N, pady=5, padx=5)


##-- кнопка повторного начала партии
def fnc_repeatplay():
    if net_mode == "connect":
        block_bynet()
        return
    init_desk()
    select_logstep(0)


ttk.Button(pnl_right, text="Начать сначала", width=btn_width,
           command=fnc_repeatplay).grid(row=9, column=0,
                                        sticky=N, pady=5, padx=5)


##-- кнопка включения.выключения режима щаписи ходов
def fnc_recordonoff():
    global record_flag

    if net_mode == "connect":
        block_bynet()
        return

    if record_flag == 0:
        clear_log()
        btn_writemode["text"] = "Закончить запись"
        record_flag = 1
    else:
        record_flag = 0
        btn_writemode["text"] = "Включить запись"


btn_writemode = ttk.Button(pnl_right, text="Включить запись", width=btn_width,
                           command=fnc_recordonoff)
btn_writemode.grid(row=10, column=0, sticky=N, pady=5, padx=5)


##-- кнопка включения.выключения звука
def fnc_soundonoff():
    global sound_mode

    if sound_mode == "on":
        btn_soundmode["text"] = "Включить звук"
        sound_mode = "off"
    else:
        sound_mode = "on"
        btn_soundmode["text"] = "Отключить звук"


btn_soundmode = ttk.Button(pnl_right, text="Отключить звук", width=btn_width,
                           command=fnc_soundonoff)
btn_soundmode.grid(row=11, column=0, sticky=N, pady=5, padx=5)

# == правая панель со списком ходов
ttk.Label(root, text='список ходов').grid(row=1, column=10, padx=5, pady=5)
pnl_log = Frame(root)
pnl_log.grid(row=2, column=10, rowspan=11, padx=5, pady=5, sticky=N)

lbx_log = Listbox(pnl_log, width=20, height=26, font=dFont)
lbx_log.pack(side="left", fill="y")
lbx_scbr = Scrollbar(pnl_log, orient="vertical")
lbx_scbr.pack(side="right", fill="y")

lbx_scbr.config(command=lbx_log.yview)
lbx_log.config(yscrollcommand=lbx_scbr.set)

# == действия при запуске программы
draw_desk()  # -- нарисовать доску
draw_figbox()  # -- нарисовать места для срубленных фигур
load_allfigs()  # -- загрузить и отрисовать фигуры с пешками

##--<4>--  запустить поток приема сообщений
tr_in = threading.Thread(target=work_in)
tr_in.daemon = True
tr_in.start()

##--<4>--  запустить главную функцию
main()

# == запустить обработку событий
root.mainloop()
