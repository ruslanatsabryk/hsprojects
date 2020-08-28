import random
import sqlite3


def last_digit_luhn(s):
    start = 1 if len(s) % 2 else 0
    dx2 = [int(d) * 2 if i % 2 else int(d) for i, d in enumerate(s, start)]
    result = 10 - sum(n - 9 if n > 9 else n for n in dx2) % 10
    return result if result < 10 else 0


def get_next_id():
    cur.execute("SELECT max(id) FROM card;")
    result = cur.fetchone()[0]
    return result + 1 if result is not None else 0


def save_account(values):
    sql_query = "INSERT INTO card (id, number, pin) VALUES (?, ?, ?);"
    cur.execute(sql_query, values)
    connection.commit()


def get_balance(number, pin):
    sql_query = "SELECT balance FROM card WHERE NUMBER=:num and pin=:pin;"
    cur.execute(sql_query, {"num": number, "pin": pin})
    result = cur.fetchone()
    return result[0] if result else result


def add_income(number, income):
    sql_query = "UPDATE card SET balance = balance + :inc WHERE number = :num;"
    cur.execute(sql_query, {"inc": income, "num": number})
    connection.commit()


def close_account(number):
    cur.execute("DELETE FROM card WHERE number = ?", (number,))
    connection.commit()


def check_account(number):
    cur.execute("SELECT COUNT(number) FROM card WHERE number = ?", (number,))
    return bool(cur.fetchone()[0])


def transfer_money(number_sen, number_rec, amount):
    cur.execute("UPDATE card SET balance = balance - ? WHERE number = ?", (amount, number_sen))
    cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (amount, number_rec))
    connection.commit()


BIN = '400000'
connection = sqlite3.connect('card.s3db')
cur = connection.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS card "
            "(id INTEGER UNIQUE, "
            "number TEXT UNIQUE, "
            "pin TEXT, "
            "balance INTEGER DEFAULT 0)")
connection.commit()

while True:
    menu = input('1. Create an account\n2. Log into account\n0. Exit\n')
    if int(menu) == 1:
        next_id = get_next_id()
        acc_id = ('0' * 8 + str(next_id))[-9:]
        card_number = BIN + acc_id + str(last_digit_luhn(BIN + acc_id))
        pin_code = ('0' * 4 + str(random.randrange(10000)))[-4:]
        save_account((next_id, card_number, pin_code))
        print(f'\nYour card has been created\nYour card number:\n'
              f'{card_number}\nYour card PIN:\n{pin_code}\n')
    elif int(menu) == 2:
        card_number = input('\nEnter your card number:\n')
        pin_entered = input('Enter your PIN:\n')
        balance = get_balance(card_number, pin_entered)
        if balance is not None:
            print('\nYou have successfully logged in!\n')
            while True:
                menu2 = input('1. Balance\n2. Add income\n3. Do transfer\n'
                              '4. Close account\n5. Log out\n0. Exit\n')
                if menu2 == '1':
                    print(f'\nbalance: {get_balance(card_number, pin_entered)}\n')
                elif menu2 == '2':
                    acc_income = int(input('\nEnter income:\n'))
                    add_income(card_number, acc_income)
                    print('Income was added!\n')
                elif menu2 == '3':
                    rec_number = input("\nTransfer\nEnter card number:\n").strip()
                    if rec_number == card_number:
                        print("You can't transfer money to the same account!\n")
                        continue
                    if rec_number[-1] != str(last_digit_luhn(rec_number[:-1])):
                        print("Probably you made mistake in the card number. Please try again!\n")
                        continue
                    if not check_account(rec_number):
                        print("Such a card does not exist.\n")
                        continue
                    transfer_amount = int(input("Enter how much money you want to transfer:\n"))
                    if transfer_amount > get_balance(card_number, pin_entered):
                        print("Not enough money!\n")
                        continue
                    transfer_money(card_number, rec_number, transfer_amount)
                    print("Success!\n")
                elif menu2 == '4':
                    close_account(card_number)
                    print('\nThe account has been closed!\n')
                    break
                elif menu2 == '5':
                    print('\nYou have successfully logged out!\n')
                    break
                else:
                    print('\nBye!')
                    exit()
        else:
            print('\nWrong card number or PIN\n')
    else:
        print('\nBye!')
        exit()
