"""
File: weather_master.py
-----------------------
This program should implement a console program
that asks weather data from user to compute the
average, highest, lowest, cold days among the inputs.
Output format should match what is shown in the sample
run in the Assignment Handout.

"""
EXIT = -1
COLD = 18


def main():
	"""
	TODO:
	"""
	print("stanCode \"Weather Master 4.0\"!")
	# print("Next Temperature: (or "+str(EXIT)+" to quit)?")
	n = int(input("Next Temperature: (or "+str(EXIT)+" to quit)?"))
	t = list()
	if n != EXIT:
		while n != EXIT:
			t.append(n)
			print("Next Temperature: (or "+str(EXIT)+" to quit)?")
			n = int(input())
			avg = 0
			s = list()
		for i in t:
			avg += i
			if i < COLD:
				s.append(i)
		print("Highest Temperature = " + str(max(t)))
		print("Lowest Temperature = " + str(min(t)))
		print("Average = " + str(avg / len(t)))
		print(str(len(s)) + " cold days")
	else:
		print("No temperatures were entered")





###### DO NOT EDIT CODE BELOW THIS LINE ######

if __name__ == "__main__":
	main()
