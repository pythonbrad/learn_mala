"""
LearnGhomala GUI by PythonBrad
started 27/04/2018 at 19:41
stable version 29/04/2018
"""

from tkinter import *
from tkinter.ttk import *
from lgm import LGM
from data import *
from PIL import ImageTk
import webbrowser
try:
	import psound
except Exception as error:
	print('FATAL ERROR:',error)

app = LGM()
app.sound_dir = 'sound'

class GUI:
	"""Interface Graphic"""

	def __init__(self):
		self.win = Tk()
		self.win.iconphoto(self.win, PhotoImage(file="ico.gif"))
		self.win.title('Learn Ghomala')
		menu = Menu()
		menu.add_cascade(label='About', command=self.about)
		self.win.config(menu=menu)
		self.pad = {"padx":15, "pady":15}
		self._temp = []
		self.size_img = (600, 300)
		self.image_home = ImageTk.Image.open('img/'+'aller'+'.png')
		self.image_home = self.image_home.resize(self.size_img)
		self.image_home = ImageTk.PhotoImage(self.image_home)
		self.data_image = {}
		self.starter()
		self.win.mainloop()

	def clean(self):
		"""Module permettant de nettoyer la fenetre"""
		
		try:
			self.frame.destroy()
		except:
			pass

	def about(self):
		"""Module qui gere l'apercu des informations sur le programme"""

		fen = Toplevel(self.win)
		Label(fen, text="Developed by PythonBrad").pack(**self.pad)
		Label(fen, text="Version: 1.0").pack(**self.pad)
		frame1 = Frame(fen)
		label1 = Label(frame1, text="Email:")
		label1.pack(side=LEFT, **self.pad)
		label2 = Label(frame1, text="fomegnemeudje@outlook.com", foreground="blue")
		label2.config(cursor='hand2')
		label2.pack(side=RIGHT)
		frame1.pack()
		frame2 = Frame(fen)
		label3 = Label(frame2, text="SiteWeb:")
		label3.bind('<1>', lambda x:webbrowser.open("mailto:fomegnemeudje@outlook.com"))
		label3.pack(side=LEFT, **self.pad)
		label4 = Label(frame2, text="http://pythonbrad.pythonanywhere.com", foreground="blue")
		label4.config(cursor='hand2')
		label4.bind('<1>', lambda x:webbrowser.open("pythonbrad.pythonanywhere.com"))
		label4.pack(side=RIGHT)
		frame2.pack()
		Label(fen, text=app.source.upper()).pack(**self.pad)

	def load_image(self):
		"""Module permettant de charger les images en memoire"""

		self.win.config(cursor='wait')
		self.frame = Frame()
		label = Label(self.frame, text="Loading images")
		label.pack(**self.pad)
		pb_var = StringVar(self.frame)
		pb_var.set(0)
		pb = Progressbar(self.frame, variable=pb_var, max=len(app.word_no_translated))
		pb.pack(**self.pad)
		self.frame.pack()
		devine = ImageTk.Image.open('img/'+'devine'+'.png')
		devine = devine.resize(self.size_img)
		devine = ImageTk.PhotoImage(devine)

		for i in app.word_no_translated:
			pb_var.set(int(pb_var.get())+1)
			label.config(text="Loading %s.png ..."%app.word_no_translated[i])

			if not i in self.data_image:

				try:
					img = ImageTk.Image.open('img/'+app.word_no_translated[i].lower()+'.png')
					img = img.resize(self.size_img)
					img = ImageTk.PhotoImage(img)
				except:
					img = devine
				self.data_image[app.word_no_translated[i]] = img
				pb.update()
		self.win.config(cursor='')

	def set_level(self, x):
		"""Module permettant de choisir un niveau"""

		app.level = x
		self.play()

	def choose(self, word=None):
		"""Module qui gere le choix de l'utilisateur"""

		if app.level in [1,2,5]:
			self.button1.config(state='disable')
			self.button2.config(state='disable')
			app.word_choosed = word
			self.label_title.config(text=app.verify())
		elif app.level in [3,4]:
			self.entry.config(state='disable')
			self.button.config(state='disable')
			app.word_choosed = self.entry.get()
			self.label_title.config(text=app.verify())
		self.win.after(1000, self.play)

	def starter(self, dialect=None):
		"""Module qui gere le menu de choix de langue"""

		self.clean()
		if not dialect:
			self.frame = Frame()
			Label(self.frame, text="Tu veux apprendre quel langue?").pack(**self.pad)
			frame1 = Frame(self.frame)
			list_lang = Listbox(frame1)
			list_lang.pack(side=LEFT)

			for i in app.get_list_lang():
				list_lang.insert('end', i)

			list_lang.selection_set(0)
			s=Scrollbar(frame1, command=list_lang.yview)
			s.pack(side=RIGHT)
			list_lang.config(yscrollcommand=s.set)
			frame1.pack(**self.pad)
			Button(
				self.frame, text="Validez",
				command=lambda:self.starter(list_lang.selection_get())
				).pack(**self.pad)
			self.frame.pack(**self.pad)
		else:
			app.setting(dialect)
			self.load_image()
			self.main_menu()

	def main_menu(self):
		"""Module qui gere le menu principale"""

		self.clean()
		self.frame = Frame()
		title = app.tilm("Cour","Maison","La cour","La maison")+" "+app.tilm("Apprendre","Étudier","Enseigner","Eduquer")+" "+app.dialect
		subtitle = "(L'école du %s)"%app.dialect
		Button(self.frame, text="Changer de dialect", command=self.starter).pack(**self.pad)
		Label(self.frame, text="Apprendre %s (%s mots)"%(app.dialect,app.word_nb)).pack(**self.pad)
		Label(self.frame, text=title).pack(**self.pad)
		Label(self.frame, image=self.image_home).pack(**self.pad)
		Label(self.frame, text=subtitle).pack(**self.pad)
		Button(self.frame, text="Commencer", command=self.choose_level).pack(**self.pad)
		self.frame.pack(**self.pad)

	def choose_level(self):
		"""Module qui gere le menu de choix de niveau"""

		self.clean()
		self.frame = Frame()
		Button(self.frame, text="Main Menu", command=self.main_menu).pack(**self.pad)
		Label(
			self.frame,
			text='Choisissez un niveaux'
			).pack(side=TOP,**self.pad)
		Button(
			self.frame,
			text='Niveaux 0',
			command=lambda:self.set_level(0)
			).pack(**self.pad)
		Button(
			self.frame,
			text='Niveaux 1',
			command=lambda:self.set_level(1)
			).pack(**self.pad)
		Button(
			self.frame,
			text='Niveaux 2',
			command=lambda:self.set_level(2)
			).pack(**self.pad)
		Button(
			self.frame,
			text='Niveaux 3',
			command=lambda:self.set_level(3)
			).pack(**self.pad)
		Button(
			self.frame,
			text='Niveaux 4',
			command=lambda:self.set_level(4)
			).pack(**self.pad)
		self.frame.pack(**self.pad)
		if app.audio_word:
			Button(
				self.frame,
				text='PREPA Niveaux 5',
				command=lambda:self.set_level('prepa 5')
				).pack(**self.pad)
			self.frame.pack(**self.pad)
			Button(
				self.frame,
				text='Niveaux 5',
				command=lambda:self.set_level(5)
				).pack(**self.pad)
			self.frame.pack(**self.pad)

	def play(self, temp=None):
		"""Module qui gere le menu de jeux"""

		self.clean()
		self.frame = Frame()
		Button(self.frame, text="Main Menu", command=self.main_menu).pack(**self.pad)

		if app.level in [0]:
			id = app.whole(0)
			Label(self.frame, text="%s signifie en %s %s"%(
				app.word_no_translated[id],
				app.dialect,
				app.tilm(app.word_no_translated[id])
				)
			).pack(**self.pad)
			Button(self.frame, text='Next', command=lambda:self.play(app.whole(1))).pack(**self.pad)
			Button(self.frame, text='Before', command=lambda:self.play(app.whole(-1))).pack(**self.pad)
		elif app.level in [1,2,3,4,5]:
			self.score = Label(self.frame, text="Score: %s"%app.score)
			self.score.pack(**self.pad)
			self.label_title = Label(
				self.frame,
				text=app.ask(app.list_audio if app.level == 5 else None)
				)
			self.label_title.pack(side=TOP, **self.pad)

			if app.level in [1,2,5]:
				pos = app.get_position()
				Label(
					self.frame,
					image=self.data_image[app.word_correct] if app.level == 1 else None
					).pack(**self.pad)
				if app.level == 5:
					Button(self.frame,
						text="Repeat",
						command=lambda:self.play_audio_word(app.word_correct)
						).pack()
				self.button1 = Button(
					self.frame,
					text=app.word_correct,
					command=lambda:self.choose(app.word_correct)
					)
				self.button1.pack(
					side=pos,
					**self.pad
					)
				self.button2 = Button(
					self.frame,
					text=app.word_no_correct,
					command=lambda:self.choose(app.word_no_correct)
					)
				self.button2.pack(
					side=RIGHT if pos == LEFT else LEFT,
					**self.pad
					)
			elif app.level in [3,4]:
				if app.level == 3:
					Label(self.frame, text="Indice: "+app.word_pendu(app.word_correct)).pack(**self.pad)
				self.entry = Entry(self.frame)
				self.entry.pack(**self.pad)
				self.button = Button(
					self.frame,
				 	text="Validez", command=self.choose
				 	)
				self.button.pack(**self.pad)
		elif app.level == "prepa 5":
			id = app.whole_sound(0)
			self.play_audio_word(app.audio_to_play)
			Label(self.frame, text="<%s> en %s"%(
				app.list_audio[id],
				app.dialect)
			).pack(**self.pad)
			Button(self.frame, text='Repeat', command=lambda:self.play(app.whole_sound(0))).pack(**self.pad)
			Button(self.frame, text='Next', command=lambda:self.play(app.whole_sound(1))).pack(**self.pad)
			Button(self.frame, text='Before', command=lambda:self.play(app.whole_sound(-1))).pack(**self.pad)

		self.frame.pack(**self.pad)

	def play_audio_word(self, word):
		""""""
		psound.play(word, app.dialect)

GUI()
