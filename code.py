from tkinter import *
from tkinter.ttk import Notebook, Progressbar, Separator
import mangadex
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime
import threading, requests, mysql.connector, queue, os, shutil

window = Tk()
q = queue.Queue()
t = threading
api = mangadex.Api()
mydb = mysql.connector.Connect(host='127.0.0.1', user='root', password='imgonkms', port='3306', autocommit=True)
mycursor = mydb.cursor()


class ViewMenu:
    def __init__(self, window):
        def adjust_scrollregion(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        mycursor.execute('create database if not exists histori;')
        mycursor.execute('create database if not exists download;')

        mycursor.execute('create table if not exists download.manga(mangaid varchar(100) primary key, title varchar(100), date_added datetime);')
        mycursor.execute('create table if not exists histori.manga(mangaid varchar(100) primary key, title varchar(100), date_added datetime);')

        self.current_text = ''

        window.bind('<Return>', lambda event: self.result(self.textbar))

        self.menu_frame = Frame(window)
        self.menu_frame.pack(fill=BOTH, expand=True)

        self.notebook = Notebook(self.menu_frame)

        self.searchtab = Frame(self.notebook)
        self.historytab = Frame(self.notebook)
        self.downloadtab = Frame(self.notebook)
        self.settingstab = Frame(self.notebook)

        self.notebook.add(self.searchtab, text='Search')
        self.notebook.add(self.historytab, text='History')
        self.notebook.add(self.downloadtab, text='Downloads')
        self.notebook.add(self.settingstab, text='Settings')

        self.notebook.pack(expand=True, fill=BOTH)

        #   Search Tab
        self.searchtab_frame = Frame(self.searchtab, relief=FLAT)
        self.searchtab_frame.pack(expand=TRUE, fill=BOTH)

        self.canvas = Canvas(self.searchtab_frame, relief=FLAT)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.scroll = Scrollbar(self.searchtab_frame, bd=0, command=self.canvas.yview)
        self.scroll.pack(side=RIGHT, fill=Y)

        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.canvas.bind('<Configure>', lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.scroll_frame = Frame(self.canvas, padx=150)

        self.screen_width = self.scroll_frame.winfo_screenwidth()
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor='n')

        self.scroll_frame.bind("<Configure>", adjust_scrollregion, add="+")

        self.searchbox_frame = Frame(self.scroll_frame)
        self.searchbox_frame.pack(side=TOP, ipady=40)

        self.textbar = Text(self.searchbox_frame, height=1, font='Lato 12', width=130, padx=6, pady=8, relief=FLAT)
        self.textbar.pack(side=LEFT)

        self.searchbutton = Button(self.searchbox_frame, text='Search', font='Lato 12 bold',  bg='#ed603d', fg='#fdfdfd', padx=6, pady=2, relief=FLAT, command=lambda: t.Thread(target=lambda:self.result(self.textbar)).start())
        self.searchbutton.pack(side=RIGHT)
        self.searchbutton.bind('<Return>', lambda event: self.result(self.textbar))

        self.result_frame = Frame(self.scroll_frame)
        self.result_frame.pack(side=TOP)

        # History Tab
        self.historytab_frame = Frame(self.historytab)
        self.historytab_frame.pack(expand=TRUE, fill=BOTH)

        self.canvas_history = Canvas(self.historytab_frame)
        self.canvas_history.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.scroll_history = Scrollbar(self.historytab_frame, bd=0, command=self.canvas_history.yview)
        self.scroll_history.pack(side=RIGHT, fill=Y)

        self.canvas_history.configure(yscrollcommand=self.scroll_history.set)
        self.canvas_history.bind('<Configure>', lambda event: self.canvas_history.configure(scrollregion=self.canvas_history.bbox('all')))

        self.scroll_frame_history = Frame(self.canvas_history, padx=150)

        self.canvas_history.create_window((0, 0), window=self.scroll_frame_history, anchor='n')

        self.scroll_frame_history.bind("<Configure>", adjust_scrollregion)

        self.frame = Frame(self.scroll_frame_history)
        self.frame.pack(side=TOP)

        mycursor.execute(f"SELECT COUNT(*) FROM histori.manga;")
        self.count = mycursor.fetchall()[0][0]

        for i in range(self.count):
            mycursor.execute(f"SELECT * FROM histori.manga order by date_added desc;")
            self.id = mycursor.fetchall()[i][0]
            threading.Thread(target=lambda:self.add_result(self.id, self.frame, i)).start()

        #   Downloads Tab
        self.downloadtab_frame = Frame(self.downloadtab)
        self.downloadtab_frame.pack(expand=TRUE, fill=BOTH)

        self.canvas_download = Canvas(self.downloadtab_frame)
        self.canvas_download.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.scroll_download = Scrollbar(self.downloadtab_frame, bd=0, command=self.canvas_download.yview)
        self.scroll_download.pack(side=RIGHT, fill=Y)

        self.canvas_download.configure(yscrollcommand=self.scroll_download.set)
        self.canvas_download.bind('<Configure>', lambda event: self.canvas_download.configure(scrollregion=self.canvas_download.bbox('all')))

        self.scroll_frame_download = Frame(self.canvas_download, padx=150)

        self.canvas_download.create_window((0, 0), window=self.scroll_frame_download, anchor='n')

        self.scroll_frame_download.bind("<Configure>", adjust_scrollregion)

        self.framee = Frame(self.scroll_frame_download)
        self.framee.pack(side=TOP)

        mycursor.execute(f"SELECT COUNT(*) FROM download.manga;")
        self.count = mycursor.fetchall()[0][0]

        for i in range(self.count):
            mycursor.execute(f"SELECT * FROM download.manga;")
            self.id = mycursor.fetchall()[i][0]
            t.Thread(target=lambda:self.add_result(self.id, self.framee, i)).start()

        #   Settings Tab
        self.settingstab_frame = Frame(self.settingstab)
        self.settingstab_frame.pack(expand=TRUE, fill=BOTH)

        self.canvas_settings = Canvas(self.settingstab_frame)
        self.canvas_settings.pack(side=LEFT, fill=BOTH, expand=TRUE)

        self.scroll_settings = Scrollbar(self.settingstab_frame, bd=0, command=self.canvas_settings.yview)
        self.scroll_settings.pack(side=RIGHT, fill=Y)

        self.canvas_settings.configure(yscrollcommand=self.scroll_settings.set)
        self.canvas_settings.bind('<Configure>', lambda event: self.canvas_settings.configure(scrollregion=self.canvas_settings.bbox('all')))

        self.scroll_frame_settings = Frame(self.canvas_settings, padx=150)

        self.canvas_settings.create_window((0, 0), window=self.scroll_frame_settings, anchor='n')

        self.scroll_frame_settings.bind("<Configure>", adjust_scrollregion)

        self.frameee = Frame(self.scroll_frame_settings)
        self.frameee.pack()

        #   Delete History
        self.delete_history_frame = Frame(self.frameee, width=1232, height=100)
        self.delete_history_frame.pack(side=TOP)
        self.delete_history_frame.pack_propagate(0)

        self.delete_history_text_frame = Frame(self.delete_history_frame)
        self.delete_history_text_frame.pack(side=LEFT)

        self.delete_history_title = Label(self.delete_history_text_frame, text='Clear History', font='Lato 12 bold', justify=LEFT, anchor=W)
        self.delete_history_title.pack(fill=X, ipady=5, padx=(18, 0))

        self.delete_history_desc = Label(self.delete_history_text_frame, text='Clears your reading history.', font='Lato 10', justify=LEFT, anchor=W)
        self.delete_history_desc.pack(fill=X, ipady=5, padx=(18, 0))

        self.delete_history_button_frame = Label(self.delete_history_frame)
        self.delete_history_button_frame.pack(side=RIGHT)

        self.delete_history_button = Button(self.delete_history_button_frame, text='DELETE', font='Lato 12 bold',  bg='#ed603d', fg='#fdfdfd', relief=FLAT, anchor=S, command=lambda: self.del_history())
        self.delete_history_button.pack(side=BOTTOM)

        self.sep1 = Separator(self.frameee, orient=HORIZONTAL)
        self.sep1.pack(fill=X)

        #   Delete Download
        self.delete_frame = Frame(self.frameee,  width=1232, height=100)
        self.delete_frame.pack(side=TOP)
        self.delete_frame.pack_propagate(0)

        self.delete_frame_inside = Frame(self.delete_frame, relief=FLAT)
        self.delete_frame_inside.pack(side=LEFT)

        self.delete_title = Label(self.delete_frame_inside, text='Clear Downloads', font='Lato 12 bold', justify=LEFT, anchor=W)
        self.delete_title.pack(fill=X, ipady=5, padx=(18, 0))

        self.delete_desc = Label(self.delete_frame_inside, text='Deletes all mangas from your downloads.', font='Lato 10', justify=LEFT, anchor=W)
        self.delete_desc.pack(fill=X, ipady=5, padx=(18, 0))

        self.delete_button_frame = Frame(self.delete_frame, )
        self.delete_button_frame.pack(side=RIGHT)

        self.delete_button = Button(self.delete_button_frame, text='DELETE', font='Lato 12 bold',  bg='#ed603d', fg='#fdfdfd', anchor=S, relief=FLAT, command=lambda: self.del_download())
        self.delete_button.pack(side=BOTTOM)

    def del_history(self):
        mycursor.execute(f'delete from histori.manga;')
        for widgets in self.frame.winfo_children():
            widgets.destroy()

    def del_download(self):
        mycursor.execute(f'delete from download.manga;')
        mycursor.execute(f'SET SESSION group_concat_max_len = 1000000;')
        mycursor.execute(f'SELECT GROUP_CONCAT(DISTINCT CONCAT("DROP DATABASE ", table_schema, ";") SEPARATOR "\n")'
                         f'FROM information_schema.tables WHERE table_schema'
                         f'NOT IN ("mysql", "information_schema", "performance_schema",  "download", "histori");')

        for i in str(mycursor.fetchall()[0][0]).splitlines():
            print(i)
            mycursor.execute(f'{i}')

        for widgets in self.framee.winfo_children():
            widgets.destroy()

        rootdir = os.path.abspath(os.curdir)
        path = f"{rootdir}\Downloads"

        for filename in os.listdir(path):
            shutil.rmtree(f'{path}\{filename}', ignore_errors=True)

    def result(self, text):
        if self.current_text == text:
            print('Same query')
            pass
        
        else:
            self.current_text = text
            print(len(self.result_frame.winfo_children()))
            if len(self.result_frame.winfo_children()) > 0:
                for widget in self.result_frame.winfo_children():
                    widget.destroy()
                    print('destroyed')

            self.list = api.get_manga_list(title=text.get("1.0", END))

            for i in range(len(self.list)):
                threading.Thread(target=lambda: self.add_result(self.list[i].manga_id, self.result_frame, i)).start()

    def add_result(self, id, frame, count):
        manga = (api.view_manga_by_id(manga_id=id))
        url = api.get_cover(coverId=manga.coverId).fetch_cover_image()
        r = requests.get(url)

        im = Image.open(BytesIO(r.content))
        width, height = im.size
        ratio = height/width
        new_width = 127
        new_height = int(ratio * new_width)
        pilImage = im.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(pilImage)

        desc = manga.description['en'].splitlines()
        del desc[1:]
        new_desc = "\n".join(str(line) for line in desc)
        newnew_desc = (new_desc[:105] + '...') if len(new_desc) > 75 else new_desc

        self.label = Button(frame,
                            text=f'       {manga.title["en"]}\n       {api.get_author_by_id(author_id=manga.authorId[0]).name}\n\n       {newnew_desc}',
                            image=photo,
                            font='lato 15',
                            compound=LEFT,
                            height=200,
                            justify=LEFT,
                            width=1232,
                            anchor=W,
                            wraplength='28c',
                            command=lambda: t.Thread(target=lambda:self.to_mangaview(manga, self.menu_frame)).start())

        # print(f'{manga.title["en"]}')
        # print(manga.description["en"].count("\n"))
        self.label.image = photo
        self.label.grid(column=1, row=count, pady=5)

    def to_mangaview(self, manga, widget):
        try:
            mycursor.execute(f'insert into histori.manga(mangaid, title, date_added)'
                             f'values("{manga.manga_id}", "{manga.title["en"]}", "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}");')
            pass
        except mysql.connector.errors.IntegrityError:
            mycursor.execute(f'delete from histori.manga where mangaid =  "{manga.manga_id}";')
            mycursor.execute(f'insert into histori.manga(mangaid, title, date_added)'
                             f'values("{manga.manga_id}", "{manga.title["en"]}", "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}");')
            pass
        widget.destroy()
        ViewManga(window, manga.manga_id)


class ViewManga:
    def __init__(self, window, mangaid, ):
        self.threads = []
        self.i = 0
        self.j = 2
        self.chapter_id_list = []
        self.allpages = []
        self.page_links = []
        self.page_count = 0
        self.chapter_name = ''
        self.current_chapter = ''
        self.current_page = 0
        self.pages_from_start = 0
        self.chapter_count = -1

        self.manga = api.view_manga_by_id(manga_id=mangaid)
        self.manga_list = api.get_manga_volumes_and_chapters(manga_id=mangaid, translatedLanguage='en')

        # self.schema = self.manga.title['en'].replace(' ', '_').lower()
        #
        # mycursor.execute(f'show databases like "{self.schema}";')
        # data = mycursor.fetchall()[0][0]
        #
        # if len(data) == 0:
        #     self.database()
        # else:
        #     pass

        self.manga_frame = Frame(window)
        self.manga_frame.pack(fill=BOTH, expand=True)

        window.bind('<Escape>', lambda event: self.to_menu(self.manga_frame))
        window.bind('<Right>', lambda event: self.next())
        window.bind('<Left>', lambda event: self.prev())

        #   MENU UI Frame
        self.menu_frame = Frame(self.manga_frame, bg="#18191b")
        self.menu_frame.pack(side=RIGHT, fill=BOTH, expand=FALSE)

        #   MAIN UI Frame
        self.page_frame = Frame(self.manga_frame, bg='#000000', bd=0, width=220, height=100)
        self.page_frame.pack(side=RIGHT, fill=BOTH, expand=TRUE)

        #   Buffer Frame
        self.buffer_frame = Frame(self.manga_frame, bg='#000000', width=220)
        self.buffer_frame.pack(side=LEFT, fill=BOTH, expand=FALSE)

        #   Sub Frames
        self.title_frame = Frame(self.menu_frame, bg='#18191b')
        self.title_frame.grid(column=0, row=0, pady=10)

        self.button_frame = Frame(self.menu_frame, bg='#18191b')
        self.button_frame.grid(column=0, row=1, pady=5)

        self.button_frame2 = Frame(self.menu_frame, bg='#18191b')
        self.button_frame2.grid(column=0, row=2, pady=5)

        self.button_frame3 = Frame(self.menu_frame, bg='#18191b')
        self.button_frame3.grid(column=0, row=3, pady=5)

        self.title = Label(self.title_frame, text=f'{self.manga.title["en"]}', font='Lato 12 bold', bg='#18191b',
                           fg='#ed603d', anchor='w', width=20, wraplength='4c', justify=LEFT)
        self.title.pack(fill=X, ipady=5, padx=(18, 0))

        self.chapter_title = Label(self.title_frame, text=f'{self.chapter_name}', font='Lato 12 bold', bg='#18191b',
                                   fg='#fdfdfd', anchor='w', width=20, wraplength='4c', justify=LEFT)
        self.chapter_title.pack(fill=X, ipady=5, padx=(18, 0))

        #   CHAPTER LIST
        self.chapter_button_frame = Frame(self.button_frame2, bg='#18191b')
        self.chapter_button_frame.pack()

        self.prev_chapter = Button(self.chapter_button_frame, text='<', font='Lato 10 bold', bd=0, bg='#4e4e4e',
                                   fg='#fdfdfd', height=3, width=2, command=lambda: self.prevChap())
        self.prev_chapter.grid(column=0, row=1, padx=3)

        self.next_chapter = Button(self.chapter_button_frame, text='>', font='Lato 10 bold', bd=0, bg='#4e4e4e',
                                   fg='#fdfdfd', height=3, width=2, command=lambda: self.nextChap())
        self.next_chapter.grid(column=2, row=1, padx=3)

        self.chapter_list = Button(self.chapter_button_frame, text='No Chapters', font='Lato 10 bold', height=3,
                                   width=15, bd=0, bg='#2b2b2b', fg='#fdfdfd',
                                   command=lambda: self.show_hide(self.list_chapter_frame, self.j))
        self.chapter_list.grid(column=1, row=1, padx=3)

        self.list_chapter_frame = Frame(self.button_frame2, bd=0)

        self.listbox_chapter = Listbox(self.list_chapter_frame, width=18, bd=0, highlightthickness=0, bg='#2b2b2b',
                                       fg='#fdfdfd')
        self.listbox_chapter.pack(side=LEFT)

        self.scroll_chapter = Scrollbar(self.list_chapter_frame, bd=0, troughcolor='#242426')
        self.scroll_chapter.pack(side=LEFT, fill=BOTH)

        # Adds the volume and chapter in the chapter listbox
        for key, value in self.manga_list.items():
            for i in value:
                if i == 'chapters':
                    for j, k in dict(value[i]).items():
                        if key == "none":
                            self.listbox_chapter.insert(END, f'   Ch. {j}')
                        else:
                            self.listbox_chapter.insert(END, f'   Vol. {key}, Ch. {j}')
                        for l in k:
                            if l == 'id':
                                self.chapter_id_list.append(k[l])
                            else:
                                continue

        # print(f'chapter id: {self.chapter_id_list}')
        self.listbox_chapter.config(yscrollcommand=self.scroll_chapter.set)
        self.listbox_chapter.yview_moveto('1.0')
        self.scroll_chapter.config(command=self.listbox_chapter.yview)

        self.listbox_chapter.bind('<Double-Button>', lambda event: self.skip_chapter(self.listbox_chapter, self.chapter_id_list))

        #   PAGE LIST
        self.first_chapter = api.get_chapter(self.chapter_id_list[-1])
        self.page_link = self.first_chapter.fetch_chapter_images()

        self.page_button_frame = Frame(self.button_frame, bg='#18191b')
        self.page_button_frame.pack()

        self.prev_page = Button(self.page_button_frame, text='<', font='Lato 10 bold', bd=0, bg='#4e4e4e', fg='#fdfdfd',
                                height=3, width=2, command=lambda: self.prev())
        self.prev_page.grid(column=0, row=0, padx=3)

        self.next_page = Button(self.page_button_frame, text='>', font='Lato 10 bold', bd=0, bg='#4e4e4e', fg='#fdfdfd',
                                height=3, width=2, command=lambda: self.next())
        self.next_page.grid(column=2, row=0, padx=3)

        self.page_list = Button(self.page_button_frame, text='No Pages', font='Lato 10 bold', height=3, width=15, bd=0,
                                bg='#2b2b2b', fg='#fdfdfd',
                                command=lambda: self.show_hide(self.list_page_frame, self.i))
        self.page_list.grid(column=1, row=0, padx=3)

        self.list_page_frame = Frame(self.button_frame, bd=0)

        self.listbox_page = Listbox(self.list_page_frame, width=18, bd=0, highlightthickness=0, bg='#2b2b2b',
                                    fg='#fdfdfd')
        self.listbox_page.pack(side=LEFT, fill=BOTH)

        self.scroll_page = Scrollbar(self.list_page_frame, bd=0, troughcolor='#242426')
        self.scroll_page.pack(side=LEFT, fill=BOTH)

        self.listbox_page.config(yscrollcommand=self.scroll_page.set)
        self.scroll_page.config(command=self.listbox_page.yview)

        self.listbox_page.bind('<Double-Button>', lambda event: self.skip_page(self.listbox_page))

        #   MENU BUTTON
        self.menu_button_frame = Frame(self.button_frame3, bg='#18191b')
        self.menu_button_frame.pack()

        self.menu = Button(self.menu_button_frame, text='Menu', font='Lato 12 bold',  bg='#ed603d', fg='#fdfdfd', width=11, padx=4, relief=FLAT, command=lambda: self.to_menu(self.manga_frame))
        self.menu.pack(pady=5)

        self.downloads = Button(self.menu_button_frame, text = 'Download', font='Lato 12 bold',  bg='#ed603d', fg='#fdfdfd', width=11, padx=4, relief=FLAT, command=lambda: t.Thread(target=lambda:self.download(self.manga)).start())
        self.downloads.pack(pady=5)

        #   IMAGE
        self.page = Label(self.page_frame, text='Loading...', bg='#000000', fg='#fdfdfd')
        self.page.pack(side=BOTTOM, fill=NONE, expand=TRUE)

        mycursor.execute(f'select exists(SELECT * FROM download.manga where mangaid = "{mangaid}");')
        self.in_download = mycursor.fetchall()[0][0]

        if self.in_download == 1:
            print('hi')

        elif self.in_download == 0:
            self.load_chapter_online(self.first_chapter.id, 'start')

    def database(self, schema):
        mycursor.execute(f'create database {schema};')
        mycursor.execute(f"create table {schema}.chapvol(link varchar(50) primary key, chapter varchar(10), volume varchar(5), pages bigint, location text(100));")
        mycursor.execute(f"create table {schema}.pages(chapter_link varchar(50), pages int, link varchar(300) primary key, location text(100), foreign key (chapter_link) references {schema}.chapvol(link));")

        for key, value in self.manga_list.items():
            for i in value:
                if i == 'chapters':
                    for j, k in dict(value[i]).items():
                        for l in k:
                            if l == 'id':
                                mycursor.execute(f'insert into {schema}.chapvol(link, chapter, volume) values ("{k[l]}", "{j}", "{key}");')

    def to_menu(self, widget):
        widget.destroy()
        ViewMenu(window)

    def show_hide(self, widget, var):
        # This will recover the widget from top level
        if var == 0:
            self.i += 1
            widget.pack()

        elif var == 1:
            self.i -= 1
            widget.pack_forget()

        elif var == 2:
            self.j += 2
            widget.pack()

        elif var == 4 and var == self.j:
            self.j -= 2
            widget.pack_forget()

    def skip_chapter(self, list, hidden_value):
        for index in list.curselection():
            self.chapter_count = index - list.index('end')
            print(self.chapter_count)

            self.value = hidden_value[index]

            if self.value != self.current_chapter:
                self.current_page = 0
                self.page.configure(image='')
                self.page.configure(text="loading...")
                self.page_links.clear()
                self.listbox_page.delete(0, 'end')

                t.Thread(target=lambda: self.load_chapter_online(self.value, 'start')).start()

            else:
                print('this is the same chapter')

    def skip_page(self, list):
        for index in list.curselection():
            if self.current_page != index:
                print('not the same page')
                self.current_page = index
                self.page_list.config(text=f'Pg. {self.current_page + 1} / {self.page_count}')
                self.page.configure(image=self.page_links[self.current_page])

    def download(self, manga):
        try:
            mycursor.execute(f'insert into download.manga(mangaid, title)'
                             f'values("{manga.manga_id}", "{manga.title["en"]}");')

        except mysql.connector.errors.IntegrityError:
            print('already in downloads')
            return

        self.database(str(manga.title["en"].replace(" ", "_").lower()))

        ey = 1

        rootdir = os.path.abspath(os.curdir)
        path = f"{rootdir}\Downloads"

        if os.path.exists(path) == False:
            os.makedirs(path)

        path = fr"{path}\\{self.manga.title['en']}"

        if os.path.exists(path) == False:
            os.makedirs(path)

        self.progress = Progressbar(self.menu_button_frame, orient=HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(side=BOTTOM)

        for chapters in reversed(self.chapter_id_list):
            eys = 1

            path = fr"{path}\\Chapter {ey}"

            mycursor.execute(f'update {str(manga.title["en"].replace(" ", "_").lower())}.chapvol set location = "{path}"'
                             f'where link = "{chapters}";')

            if os.path.exists(path) == False:
                os.makedirs(path)

            images = api.get_chapter(chapter_id=chapters).fetch_chapter_images()

            mycursor.execute(f'update {str(manga.title["en"].replace(" ", "_").lower())}.chapvol set pages = "{len(images)}"'
                             f'where link = "{chapters}";')

            for url in range(len(images)):
                mycursor.execute(f'insert into {str(manga.title["en"].replace(" ", "_").lower())}.pages(chapter_link, pages, link, location)'
                                 f'values("{chapters}", "{eys}", "{images[url]}", "{path}\\Page {eys}.png");')
                t = threading.Thread(target=self.download_image, args=(images, url, path, eys))
                self.threads.append(t)
                t.start()
                eys += 1

            for thread in self.threads:
                thread.join()

            self.progress['value']=(ey/len(self.chapter_id_list))*100
            self.menu_button_frame.update_idletasks()

            rootdir = os.path.abspath(os.curdir)
            path = f"{rootdir}\Downloads"
            path = fr"{path}\\{self.manga.title['en']}"
            ey += 1

        print('all chapters have finished loading')

    def download_image(self, images, url, path, eys):
        r = requests.get(images[url])
        pilImage = Image.open(BytesIO(r.content))
        pilImage.save(f'{path}\\Page {eys}.png')
        eys += 1
        print(f'page {eys} downloaded')

    def load_chapter_online(self, chapter, key):

        self.chapter_link = chapter

        self.current_chapter = self.chapter_link

        chapter = api.get_chapter(chapter_id=self.chapter_link)

        page = chapter.fetch_chapter_images()
        self.page_count = len(page)

        for i in range(self.page_count):
            self.listbox_page.insert(END, f'   {i + 1}')

        self.chapter_title.config(text=f'{chapter.title}')
        self.page_list.config(text=f'Pg. {self.current_page + 1} / {self.page_count}')
        self.chapter_list.config(text=f'{self.listbox_chapter.get(0, END)[self.chapter_count]}')

        print('loading different chapter')
        print('Pages loading...')
        for i in range(len(page)):
            t = threading.Thread(target=self.load_page, args=(page, i, key))
            self.threads.append(t)
            t.start()

        print('Pages finished loading.')
        print(f'Page Count:{self.page_count}')

    def load_page(self, page, i, key):
        self.page_links.append(i)
        # print(self.page_links)
        url = page[i]
        r = requests.get(url)

        pilImage = Image.open(BytesIO(r.content))
        width, height = pilImage.size
        ratio = width / height
        new_height = 780
        new_width = int(ratio * new_height)
        pilImage = pilImage.resize((new_width, new_height))
        image = ImageTk.PhotoImage(pilImage)

        self.page_links = [image if x == i else x for x in self.page_links]
        print(f'page {i} loaded')

        if key.lower() == 'start':
            if i == 0:
                self.page.configure(image=self.page_links[self.current_page])

        elif key.lower() == 'end':
            if i == self.page_count - 1:
                self.current_page = self.page_count - 1
                self.page.configure(image=self.page_links[self.current_page])

    def next(self):
        self.current_page += 1
        try:
            self.page_list.config(text=f'Pg. {self.current_page + 1} / {self.page_count}')
            try:
                self.page.configure(image=self.page_links[self.current_page])
                print(f'page {self.current_page + 1}')

            except TclError:
                print('oii')
                self.page.configure(image='')
                self.page.configure(text="HEY YOURE GOING TOO FAST")
                self.page.after(4000, lambda: self.page.configure(image=self.page_links[self.current_page]))

        except IndexError:
            if self.current_page > self.page_count - 1:
                print('Next Chapter')
                self.chapter_count -= 1
                self.current_page = 0

                self.page.configure(image='')
                self.page.configure(text="loading...")
                self.page_links.clear()
                self.listbox_page.delete(0, 'end')

                t.Thread(target=lambda: self.load_chapter_online(self.chapter_id_list[self.chapter_count], 'start')).start()

    def prev(self):
        if self.current_page > 0:
            self.current_page -= 1
            print(self.current_page)
            self.page_list.config(text=f'Pg. {self.current_page + 1} / {self.page_count}')

            try:
                self.page.configure(image=self.page_links[self.current_page])
                print(f'page {self.current_page + 1}')

            except TclError:
                self.page.configure(image='')
                self.page.configure(text="HEY YOURE GOING TOO FAST")

        else:
            if self.chapter_count < -1:
                self.chapter_count += 1
                self.current_page = 0
                print('Previous Chapter')

                self.page.configure(image='')
                self.page.configure(text="loading...")
                self.page_links.clear()

                t.Thread(target=lambda: self.load_chapter_online(self.chapter_id_list[self.chapter_count], 'end')).start()

    def nextChap(self):
        print('Next Chapter')
        self.chapter_count -= 1
        self.current_page = 0

        self.page.configure(image='')
        self.page.configure(text="loading...")
        self.page_links.clear()
        self.listbox_page.delete(0, 'end')

        t.Thread(target=lambda: self.load_chapter_online(self.chapter_id_list[self.chapter_count], 'start')).start()

    def prevChap(self):
        if self.chapter_count < -1:
            print('Previous Chapter')
            self.chapter_count += 1
            self.current_page = 0

            self.page.configure(image='')
            self.page.configure(text="loading...")
            self.page_links.clear()
            self.listbox_page.delete(0, 'end')

            t.Thread(target=lambda: self.load_chapter_online(self.chapter_id_list[self.chapter_count], 'start')).start()


ViewMenu(window)

window.title("Tagabasa ng Manga")
window.state('zoomed')

window.mainloop()
