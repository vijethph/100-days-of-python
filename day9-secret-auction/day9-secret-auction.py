"""Secret Auction"""
import os
from subprocess import call
from art import logo

def clear():
    # Clear function - source: https://www.geeksforgeeks.org/clear-screen-python/
    _ = call('clear' if os.name =='posix' else 'cls')


def find_highest_bidder(bidding_records):
    winner_amount = 0
    winner_name = ''
    for bidder in bidding_records:
        if bidding_records[bidder] > winner_amount:
            winner_amount = bidding_records[bidder]
            winner_name = bidder
    print(f'The winner is {winner_name} with ${winner_amount}')


print(logo)
print("Welcome to the secret auction program.")

# dictionary to store the name-bid pairs
bids = {}
# set condition to break out of the loop
bidding_over = False

while not bidding_over:
    # unclear whether multiple bids by the same person should be allowed
    # and whether it's possible for a subsequent bid by the same person to be LOWER than their previous one
    print("What's your name?")
    # so, just check if there's already a bid with that name (keep it case sensitive)
    while True:
        name = input("> ")
        # reject an empty input
        if name == "":
            print("Please enter a name.")
        # this should get evaluated as "truthy" (i.e. True) if there is a value assigned to it in the dictionary
        elif bids.get(name):
            print(f"There is already a bid by {name}. Please enter a different name.")
        else:
            break

    print("What is your bid?")
    # make sure it's a valid amount (no cents, to keep it simple)
    while True:
        bid_str = input("> $")
        if bid_str == "0":
            print("$0 is not a proper bid. Please try again.")
        elif not bid_str.isdigit():
            print("Please enter a valid amount.")
        else:
            bid_price = int(bid_str)
            break

    # add to the dictionary, already made sure it's a new key
    bids[name] = bid_price

    print("Are there any other bidders? Type \"yes\" or \"no\".")
    choice = input("> ").lower()
    clear()

    # skip checking the input, just keep going until "no" is entered
    if choice == "no":
        bidding_over = True
        find_highest_bidder(bids)

    

