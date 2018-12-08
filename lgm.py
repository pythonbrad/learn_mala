# -*- coding: utf-8 -*-
"""
LearnGhomala by PythonBrad
started 27/04/2018 at 19:41
first stable version 29/04/2018
"""
import random
import unicodedata
from data_lang.word import dict_word
import glob
import os

class LGM:
	"""docstring for LGM"""

	def __init__(self):
		self.source="Source: Resulam, LE B-A BA DE LA PENSéE BAMILEKé editon afrédit."
		self.word_no_translated = []
		self.word_translated = []
		self.dialect = None
		self.score = 0
		self.word_choosed = None
		self.word_correct = None
		self.word_no_correct = None
		self.id_word = 0
		self.level = 0
		self.audio_word = False
		self.list_audio = None
		self.audio_to_play = None
		self.sound_dir = None

	def word_pendu(self, word):
		"""Module qui transforme un mot en mot de pendu"""

		count = int(len(word)/2)

		for i in range(count):
			e = random.choice(word)
			if e != " ":
				word = word.replace(e, '*', 1)

		return word

	def shuffle(self, data, no_double=False):
		data_shuffled = []
		while data:
			_ = random.choice(data)
			data.remove(_)
			if not no_double or (no_double and not _ in data_shuffled):
				data_shuffled.append(_)
		return data_shuffled

	def get_list_lang(self):
		"""Module qui renvoie la liste des dialects"""

		result = []

		for i in dict_word:
			result.append(i)

		return result

	def setting(self, dialect):
		"""Module qui charge les donnees du dialect choisi"""

		self.word_no_translated = dict_word[dialect]['lang']
		self.word_translated = dict_word[dialect]['mlang']
		self.word_nb = len(dict_word[dialect]['lang'])
		self.dialect = dialect
		try:
			_ = os.getcwd()
			os.chdir(self.sound_dir+'/'+self.dialect)
			self.list_audio = [i.split('.')[0].capitalize() for i in glob.glob('*.wav')]
			os.chdir(_)
			self.audio_word = True
		except Exception as error:
			print(error)
			self.audio_word = False

	def tilm(self, *words):
		"""Module qui traduit des mots au dialect choisi"""

		for word in words:

			for id in self.word_no_translated:
				if unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode().lower() == unicodedata.normalize('NFKD', self.word_no_translated[id].lower()).encode('ascii', 'ignore').decode().lower():
					return self.word_translated[id]

		return word

	def whole(self, x):
		"""Module qui renvoie un mot, tout en parcourant la liste"""

		self.id_word += x

		if self.id_word >= len(self.word_no_translated) or self.id_word < 0:
			self.id_word = 0

		return self.id_word

	def whole_sound(self, x):
		"""Module qui joue un son, tout en parcourant la liste"""

		self.id_word += x

		if self.id_word >= len(self.list_audio) or self.id_word < 0:
			self.id_word = 0

		self.audio_to_play = self.list_audio[self.id_word]
		return self.id_word

	def random_word(self, list_word=None):
		"""Module qui donne un mot a trouver"""

		if not list_word:
			list_word = self.word_no_translated
		id = random.randint(0, len(list_word)-1)
		self.word_correct = list_word[id]

		while 1:
			id = random.randint(0, len(list_word)-1)
			self.word_no_correct = list_word[id]

			if self.word_no_correct != self.word_correct:
				break

	def incr_score(self, x):
		"""Module qui incremente le score"""
		
		self.score += x

		if self.score < 0:
			self.score = 0

	def verify(self):
		"""Module qui verifie si l'utilisateur a trouver le mot correct"""

		word_choosed = unicodedata.normalize('NFKD', self.word_choosed).encode('ascii', 'ignore').decode()
		word_correct = unicodedata.normalize('NFKD', self.word_correct).encode('ascii', 'ignore').decode()

		if word_choosed.capitalize() == word_correct.capitalize():
			self.incr_score(1)
			return "Vous avez trouver!"
		else:
			self.incr_score(-1)
			return "Vous avez rater!, C'est %s"%self.word_correct

	def ask(self, list_word=None):
		"""Module qui renvoie une question"""

		self.random_word(list_word)
		return "Que signifie %s en %s ?"%(self.tilm(self.word_correct), self.dialect) if self.level != 5 else "Ca signifie quoi?"

	def get_position(self):
		"""Module qui renvoie une position"""

		return random.choice(["left", "right"])
