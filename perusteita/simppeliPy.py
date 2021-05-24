print("Jotain simppeliä Pythonilla:")

try:
	age = input("Minkä ikäinen olet: ")
	intAge = int(age)
	yearOfBirth = 2021-intAge
	print("Olet siis syntynyt joko vuonna",yearOfBirth, "tai", yearOfBirth-1)
	
except:
	print("Et kirjoittanut numeroa.")



