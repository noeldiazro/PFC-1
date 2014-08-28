"""
	COLOR UTILS
		Matplotlib supported colors:
			b: blue
			g: green
			r: red
			c: cyan
			m: magenta
			y: yellow
			k: black
			w: white
"""
def IntToCharColor(integer):
	if(integer==0):
		return 'b'
	elif(integer==1):
		return 'g'
	elif(integer==2):
		return 'r'
	elif(integer==3):
		return 'c'
	elif(integer==4):
		return 'm'
	elif(integer==5):
		return 'y'
	elif(integer==6):
		return 'k'
	elif(integer==7):
		return 'w'
	else:
		return 'z'

def IntToColor(integer):
	if(integer==0):
		return "Blue"
	elif(integer==1):
		return "Green"
	elif(integer==2):
		return "Red"
	elif(integer==3):
		return "Cyan"
	elif(integer==4):
		return "Magenta"
	elif(integer==5):
		return "Yellow"
	elif(integer==6):
		return "Black"
	elif(integer==7):
		return "White"
	else:
		return "None"
def GetColorList():
	return ["Blue","Green","Red","Cyan","Magenta","Yellow","Black","White","None"]
