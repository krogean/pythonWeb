#!/usr/bin/python3
import sys

# Perus input
if len(sys.argv)<2:
	sys.exit("Please tell me your name")

print(sys.argv)
name = sys.argv[1]
print(f"Hello, { name }")

# Perus if else
a=3
b=2

if a<b:
	print("a on pieni")
else:
	print("a on suuri")

# Perus looppi
for planet in ["merkurius", "venus", "maa", "mars"]:
	print(planet)

for i in range(0,10):
	print(i)

# Perus funktio
def square(x):
	return x*x

# Toinen perus funktio

def greet(name="Joku", greeting="No hei"):
	return f"{ greeting }, { name }"	

# Kutsutaan funktiota
print("Square of 2: ",square(2))
print(greet(name="Anna"))














