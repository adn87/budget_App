class Category:
    def __init__(self, description):
        self.description = description
        self.ledger = []
        self.__balance = 0.0

    def __str__(self):
        top = self.description.center(30, "*") + "\n"
        ledger = ""
        for i in self.ledger:
           
            description_format = "{:<23}".format(i["description"])
            line_format = "{:>7.2f}".format(i["amount"])
            
            ledger += "{}{}\n".format(description_format[:23], line_format[:7])
        total = "Total: {:.2f}".format(self.__balance)
        return top + ledger + total

    def deposit(self, amount, description=""):
        self.ledger.append({"amount":amount,"description":description})
        self.__balance += amount

    def withdraw(self, amount, description=""):
        if(self.check_funds(amount)):
          self.ledger.append({"amount":-amount,"description":description})
          self.__balance -= amount
          return True
        return False

    def get_balance(self):
        total_balance = 0
        total_balance = self.__balance
        return total_balance

    def transfer(self, amount, category):
        if(self.withdraw(amount, "Transfer to {}".format(category.description))):
          category.deposit(amount, "Transfer from {}".format(self.description))
          return True
        return False

    def check_funds(self, amount):
        if (self.get_balance() >= amount):
          return True
        return False


def create_spend_chart(categories):
    spent_amounts = []
    
    for category in categories:
        spent = 0
        for i in category.ledger:
            if i["amount"] < 0:
                spent += abs(i["amount"])
        spent_amounts.append(round(spent, 2))

    
    total = round(sum(spent_amounts), 2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent_amounts))

    
    header = "Percentage spent by category\n"

    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + '|'
        for percent in spent_percentage:
            if percent >= value:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"

    footer = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    descriptions = list(map(lambda category: category.description, categories))
    max_length = max(map(lambda description: len(description), descriptions))
    descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
    for x in zip(*descriptions):
        footer += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (header + chart + footer).rstrip("\n")