'''Nguyễn Hoàng Thịnh - 17110372'''

from copy import deepcopy
from csp import *
'''
Hàm Backtracking_Search khởi tạo một assignment rỗng và gọi hàm backtrack. Trong đó:
assignment: là tập hợp các biến có đúng 1 giá trị. Khi đó Complete assignment là
tập hợp của tất cả các biến được gán giá trị.
csp: Định nghĩa 3 thành phần variables, domains, constraints
Hàm trả về Complete Assignment nếu ta tìm thấy solution. Ngược lại trả về Failure
'''
def Backtracking_Search(csp):
	return Backtrack({},csp)

'''
Hàm backtrack nơi đăng kí một giá trị sử dụng backtracking
'''
def Backtrack(assignment,csp):
	if isComplete(assignment):
		return assignment

	var = Select_Unasssigned_Variable(assignment,csp) # Chọn một biến chưa được gán giá trị
	domain = deepcopy(csp.D) # Sao chép domain hiện tại vào một biến khác. Biến này để dùng backtrack

	for value in Order_Domain_Values(var,assignment,csp):
		if isConsistent(var,value,assignment,csp):
			assignment[var] = value # assignment consistent với value của biến var. Ta thêm value ứng với biến var vào assignment

			# Tiến hành đi thu hẹp domain của các biến còn lại
			inferences = {}
			inferences = Inference(assignment,inferences,csp,var,value)
			# Hàm Inference không trả về failure tức là domain của các biến được 
			# thu hẹp
			if inferences != "FAILURE":
				result = Backtrack(assignment,csp)# Ta gọi hàm backtrack để tiếp tục
				# chọn biến tiếp theo và xét
				if result != "FAILURE":
					return result
		del assignment[var] # Ngược lại, đây là bước backtrack, ta xóa value ứng với 
		# biến var ra khổi assignment. Ta tiếp tục chọn một giá trị khác để xét
		csp.D.update(domain) # Ta thực hiện việc xóa value ứng với biến var ra khỏi
		# assignment thì trước đó là nó đã được thêm vào assignment hay là hàm Inference
		# được chạy để giảm domain của các neighbor. Vì vậy khi xóa đi var thì domain cũng
		# phải được backtrack
	return "FAILURE"


'''
Hàm kiểm tra xem assignment có complete hay không
'''
def isComplete(assignment):
	'''
	Ý tưởng: ta kiểm tra tập tất cả các biến được gán trong assignment
	Nếu tập các biến của assignment trùng với tập X của CSP thì return True. Ngược lại False
	'''
	return set(assignment.keys()) == set(squares)


'''
Ta chọn một biến chưa được gán giá trị sử dụng Minimum remaining-values (Chọn biến
có domain nhỏ nhất)
'''
def Select_Unasssigned_Variable(assignment,csp):
	'''
	Lấy ra tất cả các ô (biến) trong 81 ô, nếu ô đó chưa nằm trong assignmennt
	thì ta lấy ra ô đó cùng với domain của nó. Đưa nó vào trong một dictionary với
	key: biến đó, value = độ dài domain của biến đó
	Sau đó ta đi tìm key có độ dài nhỏ nhất
	'''
	unasssigned_variable = dict((squares,len(csp.D[squares])) for squares in csp.D 
		if squares not in assignment.keys())
	mrv = min(unasssigned_variable,key = unasssigned_variable.get)
	return mrv

'''
Hàm lấy domain của biến var
'''
def Order_Domain_Values(var,assignment,csp):
	return csp.D[var]

'''
Hàm kiểm tra giá trị của value ứng với biến var có làm cho assignment consisten hay không
'''
def isConsistent(var,value,assignment,csp):
	'''
	Ta đi xét các neighbor của biến var. Nếu neighbor nằm trong assignment và giá trị
	của neighbor là value, thì khi đó value làm cho assignment inconsistent
	'''
	for neighbor in csp.neighbors[var]:
		if neighbor in assignment.keys() and assignment[neighbor] == value:
			return False
	return True

'''
Hàm thu hẹp domain của các biến sử dụng forward checking
'''
def Inference(assignment, inferences, csp, var, value):
	inferences[var] = value # Thêm value của biến var vào inferences

	for neighbor in csp.neighbors[var]: # Kiểm tra các neighbor của biến var
		if neighbor not in assignment and value in csp.D[neighbor]: # Nếu neighbor không nằm trong assignment
		# và value nằm trong domain của neighbor thì ta cần loại value này ra khỏi domain của neighbor (thu hẹp domain của neighbor)
			
			if len(csp.D[neighbor])==1: # Trước khi thu hẹp domain của neighbor ta kiểm tra
			# nếu domain của neighbor hiện tại là 1 thì sau khi thu hẹp domain của nó sẽ rỗng, khi đó ta không
			# tìm được solution. Hay ta nói rằng cách chọn value cho biến var hiện tại sẽ dẫn tới viên không tìm
			# được solution. Ta return failure
				return "FAILURE"

			# Ngược lại domain của neighbor > 1, ta sẽ loại bỏ value ra khỏi neighbor
			remaining = csp.D[neighbor] = csp.D[neighbor].replace(value, "")

			# Tiếp tục kiểm tra, nếu domain của neighbor sau khi loại bỏ value chỉ còn 1 giá trị, ta thực hiện tiếp
			# constraint propagation cho các neighbor của neighbor đang xét
			if len(remaining)==1:
				flag = Inference(assignment, inferences, csp, neighbor, remaining)
				if flag == "FAILURE":
					return "FAILURE"

	return inferences

def getResults(input):
	start = time.time()
	sudoku = CSP(input)
	solved = Backtracking_Search(sudoku)
	if solved != "FAILURE":
		return printSolution(sudoku.D), time.time() - start

if __name__ == "__main__":

	# Đọc dữ liệu từ file txt
	# Sudoku được biểu diễn dưới file txt, trong đó tất cả các phần tử
	# được ghi trên 1 dòng từ trái qua phải, từ trên xuống dưới. Ô nào trống
	# ta sẽ điền vào số 0

	array = []
	with open('input2.txt','r') as ins:
		for line in ins:
			array.append(line)
	print("Input:")
	printArray(array[0])
	
	# Chạy thuật toán giải quyết đầu vào
	start = time.time()
	sudoku = CSP(array[0])
	solved = Backtracking_Search(sudoku)
	if solved != "FAILURE":
		print("Output:")
		printSolution(solved)
		print("Time excute:",time.time() - start)

