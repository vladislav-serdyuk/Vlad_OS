"""
Модуль для взлома пентагона
"""

# Импорт библиотеки wx
import wx


# создание класса MyFrame
class MyFrame(wx.Frame):
    # Функция инициализации класса
    def __init__(self):
        # Заголовок окна
        wx.Frame.__init__(self, None, title="Взлом пентагона", size=(420, 170),
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        # создание панели
        panel = wx.Panel(self)
        # Изменение размера шрифта
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(10)
        panel.SetFont(font)
        # Создание диалогового окна с прогресс баром
        pulse_dlg = wx.ProgressDialog(title="Взлом пентагона", message="Ведется атака на пентагон...", maximum=100)
        # Цикл, в котором мы заставляем двигаться наш прогресс бар
        for i in range(100):
            wx.MilliSleep(250)
            pulse_dlg.Update(1 * i)
        # Создание сайзера, текста и кнопки
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        txt = wx.StaticText(panel, label='Пентагон успешно взломан!')
        but = wx.Button(panel, label='Nice!')
        main_sizer.Add(txt, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=30)
        main_sizer.Add(but, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=20)
        # Сайзер на панель
        panel.SetSizer(main_sizer)
        # вызов функции при нажатии на кнопку
        self.Bind(wx.EVT_BUTTON, lambda event: self.nice)

    # функция
    def nice(self):
        self.Destroy()


def start() -> None:
    """
    Взлом пентагона
    :return: None
    """
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
