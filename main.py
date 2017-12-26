from tkinter import Tk, Frame, Label, Entry, Button, W, E, StringVar

class conf:
	font_header_hanzi   = ("Times", 60)
	font_header_latin   = ("", 60)
	font_body_hanzi     = ("Times", 24)
	font_body_latin     = ("", 16)
	entry_width         = 10
	padx                = 4
	pady                = 4


class TextBtnFrame(conf):
	def __init__(self, frame, label_text, func, btn_text='check'):
		self.frame      = frame
		self.label_text = label_text
		self.func       = func
		self.btn_text   = btn_text

		self.label = Label(self.frame, text=self.label_text, font=conf.font_body_hanzi)
		self.input = Entry(self.frame, width=conf.entry_width)
		self.btn   = Button(self.frame, text=self.btn_text, font=conf.font_body_latin, command=self.btn_click_action)
		self.label_right_text = StringVar()
		self.label_right = Label(self.frame, textvariable=self.label_right_text, font=conf.font_body_latin)

	def btn_click_action(self):
		user_input = self.input.get()
		label_text_right = self.func(user_input)

		self.label_right_text.set(label_text_right)

		# self.btn.config(state="disabled")

	def grid(self, row, padx, pady):
		self.label.grid(row=row, sticky=W, padx=padx)
		self.input.grid(row=row, column=1, sticky=E, pady=pady)
		self.btn.grid(row=row, column=2)
		self.label_right.grid(row=row, column=3, sticky=W, padx=padx)

	def clear(self):
		self.label_right_text.set(' ')
		self.input.delete(0, 'end')

class FlashCardsGUI(TextBtnFrame, conf):
	def __init__(self, master, words):
		self.master = master
		self.master.title('Flash cards')

		self.words = words

		self.word = self.words.sample(n=1)

		self.w_hanzi = self.word.iat[0, 0]
		self.w_pinyin = self.word.iat[0, 3]
		self.w_pinyin_num = self.word.iat[0, 2]
		self.w_english = self.word.iat[0, 4]

		self.make_mainframe()

	def make_mainframe(self):
		self.frame = Frame(self.master, padx=20, pady=20)

		self.frame.columnconfigure(0, minsize=200)
		self.frame.columnconfigure(1, minsize=100)
		self.frame.columnconfigure(2, minsize=200)
		self.frame.columnconfigure(3, minsize=100)

		row = 0

		self.w_hanzi_sv = StringVar().set(self.w_hanzi)
		hanzi_label = Label(self.frame, text=self.w_hanzi_sv, font=conf.font_header_hanzi)
		hanzi_label.grid(row=row, column=0, sticky=W, padx=conf.padx)

		self.w_pinyin_sv = StringVar().set(' ')
		pinyin_header = Label(self.frame, textvariable=self.w_pinyin_sv, font=conf.font_header_latin)
		pinyin_header.grid(row=0, column=2, sticky=W, padx=conf.padx)

		row = 1
		# First text button
		self.pinyin_frame = TextBtnFrame(self.frame, '拼音:', self.pinyin_btn_clk)
		self.pinyin_frame.grid(row=row, padx=conf.padx, pady=conf.pady)

		row = 2

		self.en_frame = TextBtnFrame(self.frame, '英语:', self.en_btn_clk)
		self.en_frame.grid(row=row, padx=conf.padx, pady=conf.pady)


		self.frame.pack()

	def pinyin_btn_clk(self, user_input):
		self.reveal_pinyin()

		from difflib import SequenceMatcher
		score_1 = SequenceMatcher(None, user_input, self.w_pinyin).ratio()
		score_2 = SequenceMatcher(None, user_input, self.w_pinyin_num).ratio()

		score = max(score_1, score_2)

		return '{} %'.format(round(100 * score))

	def en_btn_clk(self, user_input):
		if user_input.lower() in [x.lower() for x in self.w_english.split('; ')]:
			return 'Correct'

		return 'Incorrect'

	def reveal_pinyin(self):
		self.w_pinyin_sv.set(self.w_pinyin)

	def clear(self):
		self.w_pinyin_sv.set(' ')
		self.pinyin_frame.clear()
		self.en_frame.clear()

from utils import get_words
words = get_words(test_num=1)

root = Tk()
my_gui = FlashCardsGUI(root, words)
root.mainloop()