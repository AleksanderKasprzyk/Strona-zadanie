from flask import Flask, render_template, request, redirect, url_for
import json

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

        with open('purchase_form.json', mode='a+') as file:
            file.write(json.dumps(purchase, indent=4))

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

        with open('purchase_form.json', mode='a+') as file:
            file.write(json.dumps(sales, indent=4))

        return render_template('add_sale.html', product_name=product_name, unit_price=unit_price,
                               quantity=quantity)

    return render_template('add_sale.html', purchases=purchases, sales_history=sales_history)


@app.route('/change_balance', methods=['GET', 'POST'])
def change_balance():
    global balance
    balance = float(0)

    if request.method == 'POST':
        comment = request.form.get('comment')
        value = request.form.get('value')
        try:
            if comment == 'add' or comment == 'Add':
                value = float(value)
                balance += value
                answer_add = f'Balance changed on plus by {value} in PLN.'

                added_balance = \
                    {
                        "Added": balance,
                        "Comment": answer_add
                    }

                with open('save_balance.json', mode='a+') as file:
                    file.write(json.dumps(added_balance, indent=4))

                return render_template('change_balance.html', answer_add=answer_add, balance=balance)

            elif comment == 'substract' or comment == 'Substract':
                value = float(value)
                balance -= value
                answer_substract = f'Balance changed on minus by {value} in PLN.'

                minus_balance = \
                    {
                        "Added": balance,
                        "Comment": answer_substract
                    }

                with open('save_balance.json', mode='a+') as file:
                    file.write(json.dumps(minus_balance, indent=4))

                return render_template('change_balance.html', answer_substract=answer_substract, balance=balance)

        except ValueError:
            error = 'Error: Value must be a number.'

            error_json = \
                {
                    "Error": error
                }

            with open('save_balance.json', mode='a+') as file:
                file.write(json.dumps(error_json, indent=4))

            return render_template('change_balance.html', error=error)

        return render_template('change_balance.html', comment=comment, balance=balance, value=value)

    return render_template('change_balance.html', balance=balance)


@app.route('/history/')
@app.route('/history/<int:start>/')
@app.route('/history/<int:start>/<int:end>/')
def history(start=0, end=len(sales_history)):
    return render_template('history.html', purchases=purchases, sales_history=sales_history[start:end])


if __name__ == '__main__':
    app.run(debug=True)
