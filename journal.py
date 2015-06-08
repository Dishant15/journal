from Tkinter import *
import tkMessageBox
from PIL import Image
import os, datetime

dirpath = os.path.dirname(__file__)
data_folder = 'journal_data'
datapath = dirpath + data_folder + '/'

class JournalReader(object):
	"""
	Class responsible to create a reader window to read old journal entries
	This window will have 3 text box to get a date input which can point journal Entry
	of that day. Will have Next and Previouse buttons to read entries on fly.
	"""
	def __init__(self):
		self.file_list = []
		for (dirpath, dirnames, filenames) in os.walk(datapath):
			for filename in filenames:
				if filename.isdigit():
					self.file_list.append(filename)
		self.file_list.sort()

		self.reading_window = Tk()
		self.reading_window.title("Daily Journal Reader")

		self.first_column = Frame(self.reading_window)
		self.first_column.pack()

		"""
		WORK IN PROGRESS ABOUT LIST BOX TO SELECT FILE
		"""
		# self.second_column = Frame(self.reading_window)
		# self.second_column.pack()

		# # Second Column construction
		# self.list = Listbox(self.second_column, selectmode=SINGLE)
		# self.list.pack(fill=BOTH, expand=1)
		# for files in self.file_list:
		# 	self.list.insert(END, files)
		


		# First Column Construction
		self.input_frame = Frame(self.first_column)
		self.input_frame.pack()

		self.previouse_button = Button(self.input_frame, text='Previouse', command = self.get_previous_entry )
		self.previouse_button.pack(side='left')

		self.day_label = Label(self.input_frame, text='Day : ')
		self.day_label.pack(side='left')
		self.day = Entry(self.input_frame, width = 10 )
		self.day.pack(side='left')

		self.month_label = Label(self.input_frame, text='Month : ')
		self.month_label.pack(side='left')
		self.month = Entry(self.input_frame, width = 10 )
		self.month.pack(side='left')

		self.year_label = Label(self.input_frame, text='Year : ')
		self.year_label.pack(side='left')
		self.year = Entry(self.input_frame, width = 10 )
		self.year.pack(side='left')

		self.next_button = Button(self.input_frame, text='Next', command = self.get_next_entry )
		self.next_button.pack(side='left')



		self.go_frame = Frame(self.first_column)
		self.go_frame.pack()
		self.go_button = Button( self.go_frame, text = "Go To Date", command = self.go_to_date )
		self.go_button.pack()


		self.show_frame = Frame(self.first_column)
		self.show_frame.pack()

		self.text_box = Text( self.show_frame, width=500, height=500, wrap = "word" )
		self.text_box.pack()

		self.current_file = self.file_list[0]
		self.current_file_index = 0
		self.open_file( self.current_file )

		self.reading_window.geometry("900x500")

		self.reading_window.mainloop()


	def go_to_date( self ):
		day = self.day.get()
		if not day.isdigit() or len(day) > 2 :
			tkMessageBox.showerror("Input error", "Day value must be between 00 - 31")
			return None
		if len(day) < 2 : day = "0" + day

		month = self.month.get()
		if not month.isdigit() or len(month) > 2 :
			tkMessageBox.showerror("Input error", "Month value must be between 00 - 12")
			return None
		if len(month) < 2 : month = "0" + month

		year = self.year.get()
		if len(year) < 4 : year = "20" + year

		self.open_file( year + month + day )


	def get_previous_entry( self ):
		"""
		Function used to turn page while reading the Journal
		"""
		try:
			self.open_file( self.file_list[ self.current_file_index - 1 ] )
		except Exception, e:
			self.open_file( self.file_list[ -1 ] )
		

	def get_next_entry( self ):
		"""
		Function used to turn page while reading the Journal
		"""
		# current = datetime.date( date[0], date[1], date[2] )
		# tommorow = current + datetime.timedelta(days=1)
		# get_page_from_date()
		try:
			self.open_file( self.file_list[ self.current_file_index + 1 ] )
		except Exception, e:
			self.open_file( self.file_list[ 0 ] )

	def open_file( self, filename ):
		"""
		Opens a file if that filename entry exists in data_folder
		shows an error box if file do not exists
		"""
		try:
			file_op = open( datapath + filename, 'r' )
		except Exception, e:
			tkMessageBox.showerror("File does not exist", e)
			return None

		ans_str = file_op.read()
		file_op.close()
		# insert File data into Text Box
		self.text_box.delete(0.0, END)
		self.text_box.insert( END, ans_str)
		# Fill default values in Input Text Boxes
		self.year.delete(0, END)
		self.year.insert(0, filename[:4] )
		self.month.delete(0, END)
		self.month.insert(0, filename[4:6] )
		self.day.delete(0, END)
		self.day.insert(0, filename[6:] )

		self.current_file = filename
		self.current_file_index = self.file_list.index( filename )




class JournalWriter(object):
	"""
	Class responsible to create main window of the application
	Contains the text box and primary buttons for text input and journal writting
	"""
	def __init__(self):
		self.writting_window = Tk()
		self.writting_window.title("Daily Journal Writter")

		self.button_frame = Frame(self.writting_window)
		self.button_frame.pack()

		self.save_button = Button(self.button_frame, text="Save", command = self.save_file )
		self.save_button.pack(side='left')
		self.read_button = Button(self.button_frame, text="Read Old Journal", command = self.start_reader )
		self.read_button.pack(side='left')

		# self.image_button = Button(self.button_frame, text="Upload Image", command = self.image_test )
		# self.image_button.pack(side='left')

		self.text_frame = Frame(self.writting_window)
		self.text_frame.pack()

		self.text_box = Text( self.text_frame, width=500, height=500, wrap = "word" )
		self.text_box.pack()

		self.writting_window.geometry("900x500")

		self.writting_window.mainloop()


	def save_file(self):
		today = datetime.datetime.now()
		input_str = today.strftime('%d/%m/%Y    %I:%M %p     %A') + "\n\n" + self.text_box.get(0.0, END) + "\n\n"
		# Files are saved with date label
		file_name = today.strftime('%Y%m%d')
		new_file = open( datapath + file_name, 'a' )
		new_file.write(input_str)
		new_file.close()
		self.text_box.delete(0.0, END)

	def start_reader(self):
		self.reading_window = JournalReader()


if __name__ == '__main__':
	app_starter = JournalWriter()


