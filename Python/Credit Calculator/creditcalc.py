import math
import sys
# sys.argv parsing:
ptype, periods, payment, interest, principal, i = None, None, None, None, None, None
for arg in sys.argv[1:]:
    value = arg.split(sep="=")
    if "--type=" in arg and len(value) == 2 and value[1] == "diff" or value[1] == "annuity":
        ptype = value[1]
    if "--periods=" in arg and len(value) == 2 and int(value[1]) > 0:
        periods = int(value[1])
    if "--payment=" in arg and len(value) == 2 and float(value[1]) > 0:
        payment = float(value[1])
    if "--interest=" in arg and len(value) == 2 and float(value[1]) > 0:
        interest = float(value[1])
    if "--principal=" in arg and len(value) == 2 and int(value[1]) > 0:
        principal = int(value[1])
# What to count
parameter = "e" if ptype and principal and payment and interest and periods else \
            "n" if ptype and principal and payment and interest else \
            "a" if ptype and principal and periods and interest else \
            "p" if ptype and payment and periods and interest else "e"
# Period calculations:
if parameter == "e":
    print("Incorrect parameters")
else:
    i = interest / (12 * 100)
if parameter == "n":
    periods = math.ceil(math.log(payment / (payment - i * principal), 1 + i))
    overpayment = payment * periods - principal
    months, years = periods % 12, periods // 12
    if years > 0 and months > 0:
        print(f"You need {years} years and {months} {'months' if months > 1 else 'month'} "
              f"to repay this credit!")
    elif years > 0:
        print(f"You need {years} years to repay this credit!")
    else:
        print(f"You need {months} {'months' if months > 1 else 'month'} to repay this credit!")
    print(f"Overpayment = {overpayment}")
# Payments calculations:
elif parameter == "a":
    if ptype == "annuity":
        payment = math.ceil(principal * i * (1 + i) ** periods / ((1 + i) ** periods - 1))
        overpayment = payment * periods - principal
        print(f"Your annuity payment = {payment}!\nOverpayment = {overpayment}")
    else:
        sum_payment = 0
        for m in range(1, periods + 1):
            payment = math.ceil(principal / periods + i * (principal - principal * (m - 1) / periods))
            sum_payment += payment
            print(f"Month {m}: paid out {payment}")
        overpayment = sum_payment - principal
        print(f"\nOverpayment = {overpayment}")
# Credit principal calculations:
elif parameter == "p":
    principal = round(payment / (i * (1 + i) ** periods / ((1 + i) ** periods - 1)))
    overpayment = payment * periods - principal
    print(f"Your credit principal = {principal}!\nOverpayment = {overpayment}")
