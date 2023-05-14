# Exercise 1
number = int(input("Which number do you want to check?"))

if number % 2 == 0:
  print("This is an even number.")
else:
  print("This is an odd number.")


# Exercise 2
year = int(input("Which year do you want to check?"))

if year % 4 == 0:
  if year % 100 == 0:
    if year % 400 == 0:
      print("Leap year.")
    else:
      print("Not leap year.")
  else:
    print("Leap year.")
else:
  print("Not leap year.")

# Exercise 3
for fizzbuzznumber in range(1, 101):
  if fizzbuzznumber % 3 == 0 and fizzbuzznumber % 5 == 0:
    print("FizzBuzz")
  if fizzbuzznumber % 3 == 0:
    print("Fizz")
  if fizzbuzznumber % 5 == 0:
    print("Buzz")
  else:
    print(fizzbuzznumber)