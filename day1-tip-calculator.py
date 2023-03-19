print("Welcome to the tip calculator!")
bill_amount = float(input("What was the total bill? $"))
tip_amount = int(input("How much tip would you like to give? 10, 12, or 15? "))
num_people = int(input("How many people should split the bill?"))

tip_as_percent = tip_amount / 100
total_tip_amount = bill_amount * tip_as_percent
total_bill = bill_amount + total_tip_amount
bill_per_person = total_bill / num_people
final_amount = "{:.2f}".format(bill_per_person)

print(f"Each person should pay: ${final_amount}")