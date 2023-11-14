from flask import Flask, request, jsonify
from tinydb import TinyDB, Query


app = Flask(__name__)
db = TinyDB('forms_db.json')

db.insert({"name": "MyForm", "field_name_1": "email", "field_name_2": "phone"})
db.insert({"name": "OrderForm", "field_name_1": "order_date", "field_name_2": "lead_email"})


@app.route('/get_form', methods=['POST'])
def get_form():
    data = request.form.to_dict()
    form_templates = db.all()
    matching_fields = []
    for template in form_templates:
        match = True
        for key, value in template.items():
            if key != "name" and key in data:
                if value == "email" and not validate_email(data[key]):
                    match = False
                    break
                elif value == "phone" and not validate_phone(data[key]):
                    match = False
                    break
                elif value == "date" and not validate_date(data[key]):
                    match = False
                    break
                elif value == "text":
                    continue
                elif value != data[key]:
                    match = False
                    break
        if match:
            return template["name"]
        else:
            matching_fields.append({key: infer_field_type(data[key])})

    return jsonify(matching_fields)


def validate_email(email):
    return True


def validate_phone(phone):
    return True


def validate_date(date):
    return True


def infer_field_type(value):
    if validate_date(value):
        return "date"
    elif validate_phone(value):
        return "phone"
    elif validate_email(value):
        return "email"
    else:
        return "text"
    
if __name__ == '__main__':
    app.run()
