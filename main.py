from tkinter import Tk, Frame, Label, Entry, Button, W, E, StringVar

class TextBtnFrame:
	def __init__(self, frame, label_text, func, format_dict, btn_text='check'):
		self.font_body_hanzi = format_dict['font_body_hanzi']
		self.entry_width = format_dict['entry_width']
		self.font_body_latin = format_dict['font_body_latin']

		self.frame      = frame
		self.label_text = label_text
		self.func       = func
		self.btn_text   = btn_text

		self.label = Label(self.frame, text=self.label_text, font=self.font_body_hanzi)
		self.input = Entry(self.frame, width=self.entry_width)
		self.btn   = Button(self.frame, text=self.btn_text, font=self.font_body_latin, command=self.btn_click_action)
		self.label_right_text = StringVar()
		self.label_right = Label(self.frame, textvariable=self.label_right_text, font=self.font_body_latin)

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


class FlashCardsGUI(TextBtnFrame):
	def __init__(self, master, format_dict, hsk_num=1):
		self.master = master
		self.master.title('Flash cards')

		self.format_dict = format_dict
		self.font_header_hanzi = format_dict['font_header_hanzi']
		self.font_header_latin = format_dict['font_header_latin']
		self.font_body_hanzi = format_dict['font_body_hanzi']
		self.font_body_latin = format_dict['font_body_latin']

		self.padx = 4
		self.pady = 4

		self.entry_width = format_dict['entry_width']

		self.hsk_num = hsk_num

		from utils import get_words
		self.words = get_words(test_num=self.hsk_num)

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
		# self.frame.columnconfigure(4, minsize=100)

		print(self.w_hanzi)

		row = 0

		hanzi_label = Label(self.frame, text=self.w_hanzi, font=self.font_header_hanzi)
		hanzi_label.grid(row=row, column=0, sticky=W, padx=self.padx)

		row = 1
		# First text button
		pinyin_frame = TextBtnFrame(self.frame, 'Pinyin:', self.pinyin_btn_clk, self.format_dict,)
		pinyin_frame.grid(row=row, padx=self.padx, pady=self.pady)

		self.frame.pack()

	def pinyin_btn_clk(self, user_input):
		self.reveal_pinyin()

		from difflib import SequenceMatcher
		score_1 = SequenceMatcher(None, user_input, self.w_pinyin).ratio()
		score_2 = SequenceMatcher(None, user_input, self.w_pinyin_num).ratio()

		score = max(score_1, score_2)

		return '{} %'.format(round(100 * score))

	def reveal_pinyin(self):
		self.pinyin_header = Label(self.frame, text=self.w_pinyin, font=self.font_header_latin)
		self.pinyin_header.grid(row=0, column=2, sticky=W, padx=self.padx)


	def pinyin_btn_click(self):
		row = 1
		self.score_pinyin = '{} %'.format(20)
		user_guess = self.in_pinyin.get()

		score = '{} %'.format(pinyin_score(user_guess, self.w_hanzi))

		self.pinyin_label_c3 = Label(self.frame, text=self.w_pinyin, font=self.font_header_latin)
		self.pinyin_label_c3.grid(row=0, column=2, sticky=W, padx=self.padx)

		self.pinyin_label_c4 = Label(self.frame, text=score, font=self.font_body_latin)
		self.pinyin_label_c4.grid(row=row, column=3, sticky=W, padx=self.padx)

		self.pinyin_btn.config(state="disabled")

format_dict = {
		'font_header_hanzi' : ("Times", 60),
		'font_header_latin' : ("", 60),
		'font_body_hanzi'   : ("Times", 24),
		'font_body_latin'   : ("", 16),
		'entry_width'       : 10,
}

root = Tk()
my_gui = FlashCardsGUI(root, format_dict)
root.mainloop()