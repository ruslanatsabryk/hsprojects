# Hardware layer (coffee machine)
class CoffeeMachine:
    def __init__(self):
        # Initial supply state
        self.water_av = 0
        self.milk_av = 0
        self.beans_av = 0
        self.cups_av = 0
        self.money_av = 550

    def _get_supply(self) -> str:
        return f"{self.water_av} {self.milk_av} {self.beans_av} {self.cups_av} {self.money_av}"

    def _change_supply(self, water: int, milk: int, beans: int, cups: int, money: int) -> str:
        # Change inner supply state
        self.water_av += water
        self.milk_av += milk
        self.beans_av += beans
        self.cups_av += cups
        self.money_av += money
        return '0'

    def execute_command(self, command: str) -> str:
        cp_s = command.split(" ")
        cp = [int(n) for n in cp_s]
        # buy: command '0, n, n, n, n, n', return success - '0' or unsufficient (error) - '1'
        if cp[0] == 0:
            return self._change_supply(-cp[1], -cp[2], -cp[3], -cp[4], cp[5])
        # fill: command '1, n, n, n, n', return success - '0'
        if cp[0] == 1:
            return self._change_supply(cp[1], cp[2], cp[3], cp[4], 0)
        # take: command '2', return sum of money - 'n'
        if cp[0] == 2:
            money_got = self.money_av
            self._change_supply(0, 0, 0, 0, -self.money_av)
            return str(money_got)
        # remaining: command '3', return remaining - 'n n n n n'
        if cp[0] == 3:
            return self._get_supply()


# User interface layer
class UserInterface:
    # User interface now is separated from "hardware" (hardware just receive a command, mix ingredients,
    # and return a result of operation (ok, error or state of supply of ingredients and money)
    def __init__(self, coffee_machine: CoffeeMachine):
        self.machine = coffee_machine

    @staticmethod
    def get_action():
        return input('Write action (buy, fill, take, remaining, exit)\n')

    def action_fill(self, ingr: list):
        if len(ingr) == 0:
            water_ = int(input('\nWrite how many ml of water do you want to add:\n'))
            milk_ = int(input('Write how many ml of milk do you want to add:\n'))
            beans_ = int(input('Write how many grams of coffee beans do you want to add:\n'))
            cups_ = int(input('Write how many disposable cups do you want to add:\n'))
            print()
            answer = self.machine.execute_command(f'1 {water_} {milk_} {beans_} {cups_}')
        else:
            answer = self.machine.execute_command(f'1 {ingr[0]} {ingr[1]} {ingr[2]} {ingr[3]}')
        return answer

    def display_supply(self):
        answer_str = self.machine.execute_command('3')
        answer = answer_str.split()
        print(f'\nThe coffee machine has:\n{answer[0]} of water\n{answer[1]} of milk\n'
              f'{answer[2]} of coffee beans\n{answer[3]} of disposable cups\n{answer[4]} of money\n')

    def action_take(self):
        answer_str = self.machine.execute_command('2')
        answer = answer_str.split()
        print(f'\nI gave you ${answer[0]}\n')

    def action_exit(self):
        _ = self.machine.execute_command('2')
        exit()

    def check_remains(self, water_need, milk_need, beans_need, cups_need):
        answer_str = self.machine.execute_command('3')
        answer = answer_str.split()
        error = ''
        error += 'not enough water, ' if int(answer[0]) < water_need else ''
        error += 'not enough milk, ' if int(answer[1]) < milk_need else ''
        error += 'not enough coffee beans, ' if int(answer[2]) < beans_need else ''
        error += 'not enough disposable cups, ' if int(answer[3]) < cups_need else ''
        return 'Ok!' if not error else 'Sorry, ' + error[:-2] + '!'

    def action_buy(self):
        coffee_type = self.get_coffee_type()
        error = 'Ok!'
        recipe = []
        # As coffee machine ("hardware") is separated from the user interface,
        # you can create another logic of UserInterface class or even new recipes without
        # reprogramming CoffeeMachine class:
        # for example recipe[0, 250, 0, 1, 2] will makes for you a pure milk,
        # and recipe[250, 0, 0, 1, 1] - is hot water.
        # You just need to send correct commands to CoffeMachine.execute_command('str') method.
        if coffee_type == '1':  # 1 - espresso
            recipe = [250, 0, 16, 1, 4]
            error = self.check_remains(*recipe[:-1])
        if coffee_type == '2':  # 2 - latte
            recipe = [350, 75, 20, 1, 7]
            error = self.check_remains(*recipe[:-1])
        if coffee_type == '3':  # 3 - cappuccino
            recipe = [200, 100, 12, 1, 6]
            error = self.check_remains(*recipe[:-1])
        if coffee_type == 'back':
            print()
            return
        if error == 'Ok!':
            recipe_ = [str(n) for n in recipe]
            _ = self.machine.execute_command(f'0 {" ".join(recipe_)}')
            print('I have enough resources, making your coffee!\n')
        else:
            print(f'{error}\n')

    @staticmethod
    def get_coffee_type():
        return input('\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu\n')

    def make_action(self):
        action = self.get_action()
        _ = self.action_buy() if action == 'buy' else self.action_fill([]) if action == 'fill' else \
            self.action_take() if action == 'take' else self.display_supply() if action == 'remaining' \
            else self.action_exit()


if __name__ == "__main__":
    # Create the coffee machine
    best_coffee_machine = UserInterface(CoffeeMachine())
    # Switch on machine and load the ingredients before use [water, milk, beans, cups]
    initial_supply = [400, 540, 120, 9]
    best_coffee_machine.action_fill(initial_supply)
    # Coffee Machine is ready for coffee lovers!
    while True:
        best_coffee_machine.make_action()
