'''Nguyễn Hoàng Thịnh - 17110372'''

from copy import deepcopy

import queue
import time


rows = "ABCDEFGHI"
cols = domains = "123456789"

def cross(rows,cols):
	return [row + col for row in rows for col in cols]


squares = cross(rows,cols)
'''
Hàm trên chạy thì biến squares sẽ có kết quả:
 ['A1','A2','A3','A4','A5','A6','A7','A8','A9'],
  'B1','B2','B3','B4','B5','B6','B7','B8','B9'],
  .............................................
  'I1','I2','I3','I4','I5','I6','I7','I8','I9'],
'''
class CSP:
	def __init__(self,grid = None):
		# Mô tả 3 thành phần của bài toán CSP
		self.X = squares # Tất cả các ô đều là biến
		self.D = self.getDomainForEachVariable(grid)

		# Lấy danh sách các unit (9 hàng, 9 cột và 9 vùng 3x3)
		self.unitList = ([cross(rows,col) for col in cols] +
						 [cross(row,cols) for row in rows] +
						 [cross(r,c) for r in ("ABC","DEF","GHI") for c in ("123","456","789")])
		# Kết quả:
		'''
		[['A1','B1','C1','D1','E1','F1','G1','H1','I1'],
		 ..............................................
		 ['A9','B9','C9','D9','E9','F9','G9','H9','I9'],

		 ['A1','A2','A3','A4','A5','A6','A7','A8','A9'],
		 ..............................................
		 ['I1','I2','I3','I4','I5','I6','I7','I8','I9'],

		 ['A1','A2','A3','B1','B2','B3','C1','C2','C3'],
		 ..............................................
		 ['G7','G8','G9','H7','H8','H9','I7','I8','I9']]
		'''

		'''
		Đối với mỗi biến V thuộc X. Ta gán cho biến V một danh sách chứa:
		- Danh sách các phần tử thuộc chung 1 hàng với V
		- Danh sách các phần tử thuộc chung 1 cột với V
		- Danh sách các phần tử thuộc chung 1 vùng 3x3 với V
		'''
		self.units = dict((Xi,[Xj for Xj in self.unitList if Xi in Xj]) for Xi in self.X)
		'''
		VD cho biến A1 ta có:
		{'A1': [['A1','B1','C1','D1','E1','F1','G1','H1','I1'],
				['A1','A2','A3','A4','A5','A6','A7','A8','A9'],
				['A1','A2','A3','B1','B2','B3','C1','C2','C3']]}
		'''

		# Đối với mỗi biến V thuộc X ta lấy ra danh sách các phần tử ràng buộc với biến đó
		self.neighbors = dict((Xi, set(sum(self.units[Xi],[])) - set([Xi])) for Xi in self.X)
		# Ví dụ các ô ràng buộc với A1 là:
		# {'A1': {'B1','C1',..'I1','A2','A3',...'A9','B2','B3','C2','C3'}}

		# Từ danh sách trên. Ta tạo ra tất cả các ràng buộc ( arc constraint ) của CSP
		self.C = {(variable,neighbor) for variable in self.X for neighbor in self.neighbors[variable]}

	# Hàm lấy domain cho mỗi ô (biến)
	def getDomainForEachVariable(self,grid):
		i = 0
		D = dict()
		for cell in self.X: # Duyệt qua tất cả các ô (biến)
			if grid[i] != '0': # Nếu ô đã có giá trị thì ta gán domain là giá trị hiện tại của ô đó
				D[cell] = grid[i]
			else:
				D[cell] = domains # Nếu ô đang trống thì ta gán domain là giá trị có thể nhận từ 1 đến 9
			i += 1

		return D

def printArray(grid):
	i = 0
	result = ""
	while i < len(grid):
		result += grid[i] +" "
		i += 1
		if i%9 == 0:
			result += "\n"
	print(result)

def printSolution(D):
	array = ""
	result = ""
	i = 0
	for v in squares:
		array+=D[v]
		result += D[v] + " "
		i += 1
		if i%9 == 0:
			result += "\n"
	print(result)
	return array