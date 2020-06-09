'''Nguyễn Hoàng Thịnh - 17110372'''

from tkinter import Frame, Menu, Tk, Label, Button, PhotoImage
from tkinter.filedialog import Open

import ac3algorithm as ac3 
import backtracksearch as bks

'''Tạo một class kế thừa từ Frame, nên nó sẽ có kiểu là frame và đại diện cho một cửa sổ trong chương trình'''
class App(Frame):

	def __init__(self,parent):
		super().__init__(parent)
		self.parent = parent
		self.squares = []
		self.initUI()


	def initUI(self):
		# Tạo tiêu đề cho cửa sổ
		self.parent.title("Sudoku problem")

		# Cấu hình layout cho cửa sổ này. Trong đó tham số:
		# side = left : cho biết layout sẽ căn chỉnh cố định với cạnh trái
		# fill = both : kích thước của layout sẽ đổ đầy 2 bên
		# expand = True : cho phép cửa sổ mở rộng
		self.pack(side = "left", fill ="both", expand = True)

		# Tạo menu cho cửa sổ
		menuBar = Menu(self)
		self.parent.config(menu = menuBar)

		fileMenu = Menu(menuBar)
		fileMenu.add_command(label = "Import Sudoku", command = self.importSudoku)
		menuBar.add_cascade(label = "File",menu = fileMenu)

		# Tạo một frame, frame này sẽ chứa 81 ô. Trong đó:
		# self: cho biết widget sẽ chứa nó
		# width: cho biết chiều rộng của frame
		# height: cho biết chiều cao của frame
		self.map = Frame(self,width = 600, height = 600)
		self.map.pack(side = "left", fill="both",expand = True)

		# Lấy ra thông tin chiều dài và rộng tính theo pixel của map
		self.map.update()
		self.x = int(self.map.winfo_width() - 10)
		self.y = int(self.map.winfo_height() - 10)

		# Tạo frame thứ 2, frame này chứa button sử dụng để tìm lời giải và chứa label
		# hiển thị thời gian tìm lời giải
		self.frameWidget = Frame(self, width = 200)
		self.frameWidget.pack(side = "left", fill = "both",expand = True)

		# Tạo button để chạy tìm lời giải
		# Tham số command = self.resolvingUsingAc3 để tạo sự kiện khi nhấn button
		self.btnAc3 = Button(self.frameWidget, text = "AC3 algorithm", command = self.resolvingUsingAc3)
		# Tham số pady = 50 để label cách trục y 25px
		self.btnAc3.pack(pady = 50)

		self.btnBks = Button(self.frameWidget, text = "Backtrack algorithm", command = self.resolvingUsingBacktrack)
		self.btnBks.pack(pady = 50)

		# Tạo label hiển thị thời gian tìm lời giải
		self.lbTime = Label(self.frameWidget,text = "0.0s")
		self.lbTime.pack(pady = 25)

	
	'''Hàm lấy dữ liệu từ file txt'''
	def importSudoku(self):
		# List lưu các định dạng file khác nhau để đọc
		ftypes = [('All files','*')]
		# Hiển thị hộp thoại chọn đường dẫn file
		dialog = Open(self,filetypes = ftypes)
		path = dialog.show()

		# Đọc file
		intput_ = ""
		with open(path,"r") as ins:
			for line in ins:
				intput_ += line
		self.input = intput_

		self.createSquares(9)
		self.setNumbers(9,intput_)

	'''
	Hàm gọi thuật toán AC3 algorithm để tìm lời giải, sau đó nó sẽ đặt các con số lên map
	'''
	def resolvingUsingAc3(self):
		# Khi thuật toán bắt đầu chạy, ta sẽ khóa button này lại tránh trường hợp click nhiều
		# lần từ người dùng
		self.btnAc3['state'] = 'disabled'
		self.btnBks['state'] = 'disabled'

		solution, ti = ac3.getResults(self.input)

		self.createSquares(9)
		self.setNumbers(9,solution)
		self.lbTime.config(text = str(ti)+"s")

		# Thuật toán chạy xong, các số đã được đặt ta mở khóa lại button
		self.btnAc3['state'] = 'active'
		self.btnBks['state'] = 'active'

	'''
	Hàm gọi thuật toán Backtrack algorithm để tìm lời giải, sau đó nó sẽ đặt các con số lên map
	'''
	def resolvingUsingBacktrack(self):
		# Khi thuật toán bắt đầu chạy, ta sẽ khóa button này lại tránh trường hợp click nhiều
		# lần từ người dùng
		self.btnAc3['state'] = 'disabled'
		self.btnBks['state'] = 'disabled'

		solution, ti = bks.getResults(self.input)

		self.createSquares(9)
		self.setNumbers(9,solution)
		self.lbTime.config(text = str(ti)+"s")

		# Thuật toán chạy xong, các số đã được đặt ta mở khóa lại button
		self.btnAc3['state'] = 'active'
		self.btnBks['state'] = 'active'



	'''Hàm tạo 81 ô trên map'''
	def createSquares(self, numOfSquares):
		for widget in self.map.winfo_children():
			widget.destroy()

		self.map.update()
		self.squares.clear()

		# Lấy chiều rộng và chiều dài  của 1 ô theo pixel
		w = int(self.x/numOfSquares)
		h = int(self.y/numOfSquares)

		# Cấu hình cột, hàng cho map
		for k in range(numOfSquares):
			self.map.columnconfigure(k,pad = 1)
			self.map.rowconfigure(k,pad = 1)

		# Tạo các label, mỗi ô trên map sẽ chứa một label, dùng để hiển thị số
		for i in range(numOfSquares):
			self.squares.append([])
			for j in range(numOfSquares):
				# Tạo một ảnh pixel, để khi ta set width và height cho label thì nó sẽ lấy
				# kích thước theo pixel chứ không phải mm

				pixelVirtual = PhotoImage(width = 1, height = 1)
				lb = Label(self.map, text = 0, image = pixelVirtual, compound = 'center', borderwidth = 1,
					relief = "groove",width = w, height = h, bg = "white")
				lb.config(font =("Courier", 35))
				lb.grid(row = i, column = j)
				self.squares[i].append(lb)

	'''Hàm đặt các con số lên map dựa vào solution tìm được'''
	def setNumbers(self,numOfSquares,solution):
		for i in range(numOfSquares):
			for j in range(numOfSquares):
				lb = self.squares[i][j]
				pixelVirtual = PhotoImage(width = 1, height = 1)
				lb.config(image = pixelVirtual, text = str(solution[i*numOfSquares+j]))



#Tạo một cửa sổ
tk = Tk()
app = App(tk)
#Lệnh gọi hiển cửa sổ
tk.mainloop()