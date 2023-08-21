from flask import Flask, request, jsonify
import re
import datetime
import math
import uuid

app = Flask(__name__)

# A global cache to store output id key-value pairs (id, score) based on the instruction
cache = {}


# Add key, value to global cache
def add_to_cache(key, value):
    global cache
    cache[key] = value


# Get key from global cache
def get_from_cache(key):
    global cache
    return cache.get(key)


# Validate purchase date
def validate_purchase_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except Exception:
        return False


# Validate purchase time
def validate_purchase_time(time_string):
    try:
        datetime.datetime.strptime(time_string, '%H:%M')
        return True
    except Exception:
        return False


# Count retailer valid characters
def count_characters(text):
    pattern = r'[^a-zA-Z0-9]'
    cleaned_text = re.sub(pattern, '', text)
    num_characters = len(cleaned_text)
    return num_characters


# Check if total is a round dollar
def is_round_dollar(total):
    total_split = total.split('.')
    return int(total_split[1]) == 0


# Check if total is a multiple of 0.25
def is_multiple_of_025(total):
    try:
        num = float(total)
        remainder = num % 0.25
        return remainder == 0
    except ValueError:
        return False


# Check if purchaseDate is an odd day
def is_odd_day(date_string):
    try:
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        day = date.day
        return day % 2 != 0
    except ValueError:
        return False


# Check if time is between 14:00 -16:00
def is_between_time(time_string):
    try:
        time = datetime.datetime.strptime(time_string, "%H:%M").time()
        start_time = datetime.time(14, 0)
        end_time = datetime.time(16, 0)
        return start_time <= time <= end_time
    except ValueError:
        return False


# Validate POST parameters
def validate_post_param(data):
    required_params = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
    # Check if all the required parameters are included
    for param in required_params:
        if param not in data:
            print(f"{param} is required")
            return False

    # Validate retailer parameters
    # Regex rule: Matches strings that do not contain whitespace characters
    # Match: 'hello', '123', 'ThisIsAString'
    # Do not match: 'hello world', '123 ',' This is a string '
    # if not re.match("^[^\s]+$", data['retailer']):
    #     print(f"retailer is invalid. value: {data['retailer']}")
    #     return False

    # Validate purchaseDate parameter in format yyyy-mm-dd
    if not validate_purchase_date(data['purchaseDate']):
        print(f"purchaseDate is invalid. value: {data['purchaseDate']}")
        return False

    # Validate purchaseTime parameter in 24-hour system and format hh:mm
    if not validate_purchase_time(data['purchaseTime']):
        print(f"purchaseTime is invalid. value: {data['purchaseTime']}")
        return False

    # Validate items parameter (should be an array type)
    if len(data['items']) < 1 or type(data['items']) != list:
        print(f"items is invalid. value: {data['items']}")
        return False

    # Validate items contents
    for item in data['items']:
        if "shortDescription" not in item or "price" not in item:
            print(f"item is invalid. value: {item}")
            return False

        # Validate hortDescription in item
        # Regex rule: Check if a string contains only letters, numbers,
        # underscores, Spaces, and hyphens (minus), and no other special characters
        # Match: 'hello_world', 'a1-2', 'foo bar'
        # Do not match: 'hello!', 'a@2', 'foo.bar'
        if not re.match("^[\\w\\s\\-]+$",item['shortDescription']):
            print(f"item.shortDescription is invalid. value: {item['shortDescription']}")
            return False

        # Validate price in item
        # Regex rule: Matches a numerical string of exactly two decimal places
        # Match: '123.45', '0.99', '9.00'
        # Do not match: 'abc', '1.234', '12.3'
        if not re.match("^\\d+\\.\\d{2}$",item['price']):
            print(f"item.price is invalid. value: {item['price']}")
            return False

    # Validate total parameter
    # Regex rule: Matches a numerical string of exactly two decimal places
    # Match: '123.45', '0.99', '9.00'
    # Do not match: 'abc', '1.234', '12.3'
    if not re.match("^\\d+\\.\\d{2}$", data['total']):
        print(f"total is invalid. value: {data['total']}")
        return False

    return True


# Calculate score based on rules
def calculate_score(data):
    """
    rules
    1、 One point for every alphanumeric character in the retailer name.
    2、 50 points if the total is a round dollar amount with no cents.
    3、 25 points if the total is a multiple of 0.25.
    4、 5 points for every two items on the receipt.
    5、 If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2
    and round up to the nearest integer. The result is the number of points earned.
    6、 6 points if the day in the purchase date is odd.
    7、 10 points if the time of purchase is after 2:00pm and before 4:00pm.

    """
    # Define initial score
    score = 0

    # 1、 One point for every alphanumeric character in the retailer name.
    score += count_characters(data['retailer'])

    # 2、 50 points if the total is a round dollar amount with no cents.
    if is_round_dollar(data['total']):
        score += 50

    # 3、 25 points if the total is a multiple of 0.25.
    if is_multiple_of_025(data['total']):
        score += 25

    # 4、 5 points for every two items on the receipt.
    score += int(len(data['items']) / 2) * 5

    # 5、 If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2
    # and round up to the nearest integer. The result is the number of points earned.
    for item in data['items']:
        if len(item['shortDescription'].strip()) % 3 == 0:
            score += math.ceil(float(item['price']) * 0.2)

    # 6、 6 points if the day in the purchase date is odd.
    if is_odd_day(data["purchaseDate"]):
        score += 6

    # 7、 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    if is_between_time(data["purchaseTime"]):
        score += 10

    # Generate an id and cache the id
    id = str(uuid.uuid4())
    add_to_cache(id, score)
    return id


# Output id from POST API
@app.route('/receipts/process', methods=['POST'])
def post_data():
    data = request.get_json()
    if not validate_post_param(data):
        return jsonify({"msg": "The receipt is invalid"}), 400

    id = calculate_score(data)

    return jsonify({"id": id}), 200


# Output score based on id from cache
@app.route('/receipts/<string:id>/points', methods=['GET'])
def get_receipt_points(id):
    # add_to_cache("1111aa",100)
    if re.match("^\\S+$", id):
        score = get_from_cache(id)
        if score is not None:
            data = jsonify({"points": score}), 200 # Assume we return JSON data with id and points
        else:
            data = jsonify({"msg": "No receipt found for that id"}), 404
        return data
    else:
        return {"msg": "The receipt is invalid"}, 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11111)