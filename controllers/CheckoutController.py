from flask import request, render_template
from models import Item, Check, db


class CheckoutController:

    @staticmethod
    def checkout(item_id):
        chekoutItem = Item.query.get(item_id)
        if request.method == 'POST':
            x = "So far, no discount for this code"
            total = chekoutItem.total
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            address = request.form.get('address')
            discount = request.form.get('discount')
            if discount == "11111":
                x = "12% discount"
                total = chekoutItem.total * 0.88
            check1 = Check(name, email, phone, address, chekoutItem.id, discount, total)
            db.session.add(check1)
            db.session.commit()
            return render_template('checkout.html', item=chekoutItem, check=check1,
                                   response="information has been saved successfully", percentage=x)

        return render_template('checkout.html', item=chekoutItem)
