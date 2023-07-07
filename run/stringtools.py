

def formattobashready(f=""):
    f = f.replace(" ", "\ ")
    f = f.replace("(", "\(")
    f = f.replace(")", "\)")
    f = f.replace("'", "\\'")
    return f


def RemoveSpaces(string):
	title_no_spaces = string.split(' ')
	res = ''
	for word in title_no_spaces:
		res = res+word
	return res
