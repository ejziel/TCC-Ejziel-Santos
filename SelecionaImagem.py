import tkinter as tk
from tkinter import filedialog
import os
from tkinter import messagebox

class SelectImage: #classe para selecionar arquivo
	def __init__(self, app_window):
		self.app_window = app_window

	def select(self):
		#answer = messagebox.askyesno("Question","As imagens do usuário já foram capturadas?")
		
		#if answer == True:
			

			# Build a list of tuples for each file type the file dialog should display
			my_filetypes = [('images', '.jpg'), ('all files', '.*')]

			# Ask the user to select a folder.
			#answer = filedialog.askdirectory(parent=application_window,
			#								initialdir=os.getcwd(),
			#								title="Please select a folder:")

			# Ask the user to select a single file name.
			answer = filedialog.askopenfilename(parent=self.app_window,
												initialdir=os.getcwd(),
												title="Please select a file:",
												filetypes=my_filetypes)

			# Ask the user to select a one or more file names.
			#answer = filedialog.askopenfilenames(parent=application_window,
			#									initialdir=os.getcwd(),
			#									title="Please select one or more files:",
			#									filetypes=my_filetypes)
			
			return answer
			
		#else:
			
		#	return answer
			
