class Category():
    def __init__(self, description):
        self.description = description
        self.ledger = []
        self.balance = 0.0
    
    def __repr__(self):
        header = self.description.center(30, "*") + '\n'
        ledger = ''
        for item in self.ledger:
            line_description = '{:23}'.format(item['description'])
            line_amount = '{:>7.2f}'.format(item['amount'])
            ledger += '{}{}\n'.format(line_description[:23], line_amount[:7])
        total = 'Total: {:.2f}'.format(self.balance)
        return header + ledger + total

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})
        self.balance += amount

    def withdraw(self, amount, description=''):
        if self.balance >= amount:
            self.ledger.append({"amount": -1 * amount, "description": description})
            self.balance -= amount
            return True
        else:
            return False
    
    def get_balance(self):
        return self.balance

    def transfer(self, amount, category_instance):
        if self.withdraw(amount, "Transfer to {}".format(category_instance.description)):
            category_instance.deposit(amount, "Transfer from {}".format(self.description))
            return True
        else:
            return False
    
    def check_funds(self, amount):
        return self.balance >= amount
    
def create_spend_chart(categories):
    # Menghitung jumlah pengeluaran di setiap kategori
    spend_amounts = []
    for category in categories:
        spent = 0
        for item in category.ledger:
            if item['amount'] < 0:
                spent += abs(item['amount'])
        spend_amounts.append(round(spent, 2))

    # Menghitung persentase pengeluaran
    total_spent = sum(spend_amounts)
    spent_percentage = list(map(lambda amount: int((amount / total_spent) * 100 // 10) * 10, spend_amounts))

    # Membuat header
    header = "Percentage spent by category\n"

    # Membuat chart
    chart = ""
    for value in reversed(range(0, 101, 10)):
        chart += str(value).rjust(3) + "|"
        for percent in spent_percentage:
            chart += " o " if percent >= value else "   "
        chart += " \n"

    # Membuat garis horizontal
    chart += "    " + "-" * (3 * len(categories) + 1) + "\n"

    # Membuat footer dengan nama kategori
    descriptions = [category.description for category in categories]
    max_length = max(len(description) for description in descriptions)
    descriptions = [description.ljust(max_length) for description in descriptions]

    footer = ""
    for row in zip(*descriptions):  # Menyusun nama kategori secara vertikal
        footer += "     " + "  ".join(name for name in row) + "  \n"

    return (header + chart + footer).rstrip("\n")


# Pengujian
food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(105.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')

clothing = Category('Clothing')
clothing.deposit(500, 'deposit')
clothing.withdraw(50.75, 'clothes')

auto = Category('Auto')
auto.deposit(1000, 'deposit')
auto.withdraw(200, 'car maintenance')

# Cetak hasil kategori
print(food)
print(clothing)
print(auto)

# Cetak chart
print(create_spend_chart([food, clothing, auto]))
