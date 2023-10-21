from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
# current_inventory = []
# current_quantity_items = []
# current_price = []
# current_balance = 0
# history_data = []
purchases = []
sales_history = []
balance = float(0)


@app.route('/', methods=['GET', 'POST'])
def purchase_form():
    if request.method == 'POST':
        product_name = request.form['product_name']
        unit_price = float(request.form['unit_price'])
        quantity = int(request.form['quantity'])
        total_cost = unit_price * quantity

        purchase = \
            {
                'product_name': product_name,
                'unit_price': unit_price,
                'quantity': quantity,
                'total_cost': total_cost
            }
        purchases.append(purchase)
        # history_data.append(purchase)
        # current_inventory.append(product_name)
        # current_quantity_items.append(quantity)
        # current_price.append(unit_price)

        return render_template('home_page.html', product_name=product_name, unit_price=unit_price,
                               quantity=quantity)

    return render_template('home_page.html', purchases=purchases)


@app.route('/add_sale', methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        product_name = request.form['product_name']
        unit_price = float(request.form['unit_price'])
        quantity = int(request.form['quantity'])
        total_price = unit_price * quantity

        sales = \
            {
                'product_name': product_name,
                'unit_price': unit_price,
                'quantity': quantity,
                'total_price': total_price
            }
        sales_history.append(sales)
        # purchases.remove(sales)

        return render_template('add_sale.html', product_name=product_name, unit_price=unit_price,
                               quantity=quantity)

    return render_template('add_sale.html', purchases=purchases, sales_history=sales_history)


@app.route('/change_balance', methods=['GET', 'POST'])
def change_balance():
    global balance
    balance = float(0)

    if request.method == 'POST':
        comment = request.form['comment']
        value = request.form['value']
        try:
            if comment == 'add' or comment == 'Add':
                value = float(value)
                balance += value
                return f'Balance changed by {value} in PLN.'
            elif comment == 'substract' or comment == 'Substract':
                value = float(value)
                balance -= value
                return f'Balance changed by {value} in PLN.'
        except ValueError:
            return 'Error: Value must be a number.'

        return render_template('change_balance.html', comment=comment, balance=balance, value=value)

    return render_template('change_balance.html', balance=balance)


@app.route('/history/')
@app.route('/history/<int:start>/')
@app.route('/history/<int:start>/<int:end>/')
def history(start=0, end=len(sales_history)):
    return render_template('history.html', purchases=purchases, sales_history=sales_history[start:end])


if __name__ == '__main__':
    app.run(debug=True)
