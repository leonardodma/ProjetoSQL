import json


def create_data(new_data, field_name):
    with open('data.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        file_data[field_name].append(new_data)
        file.truncate(0)
        file.seek(0)
        json.dump(file_data, file, indent=4)


def read_data(field_name=None):
    with open('data.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)

        if field_name == None:
            return file_data
        else:
            return file_data[field_name]


def update_data(field_name, column_name, value, data_to_insert):
    data = read_data(field_name)
    new_data = []

    if len(column_name) == 1:
        for i in range(len(data)):
            d = data[i]
            if d[column_name[0]] == value[0]:
                new_data.append(data_to_insert)
            else:
                new_data.append(d)
    else:
        for i in range(len(data)):
            d = data[i]
            if d[column_name[0]] == value[0] and d[column_name[1]] == value[1]:
                new_data.append(data_to_insert)
            else:
                new_data.append(d)
    

    with open('data.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        del file_data[field_name]
        file_data[field_name] = new_data
        file.truncate(0)
        file.seek(0)
        json.dump(file_data, file, ensure_ascii=False, indent=4)


def delete_data(field_name, column_name, value):
    data = read_data(field_name)
    new_data = []

    if len(column_name) == 1:
        new_data = list(filter(lambda x: x[column_name[0]] != value[0], data))
    else:
        for i in range(len(data)):
            d = data[i]
            if d[column_name[0]] == value[0] and d[column_name[1]] == value[1]:
                pass
            else:
                new_data.append(d)

    with open('data.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        del file_data[field_name]
        file_data[field_name] = new_data
        file.truncate(0)
        file.seek(0)
        json.dump(file_data, file, indent=4)


def get_next_id(field_name, column_name):
    data = read_data(field_name)
    max_id = 0
    for d in data:
        if d[column_name] > max_id:
            max_id = d[column_name]
    
    return max_id + 1


def check_id(field_name, column_name, id):
    data = read_data(field_name)

    id_found = False
    for d in data:
        if d[column_name] == id:
            id_found = True
    
    return id_found

# CRUD WITH JSON TESTS

# Create
""" entry = {
    "fk_id_carrinho": 4,
    "fk_id_produto": 3
}
create_data(entry, "carrinho_produto") """

# Read
""" print(get_data("carrinho_produto")) """

# Update

""" data_to_insert = {
    "fk_id_carrinho": 1,
    "fk_id_produto": 4
} """

# Case where there are only one param of search
""" update_data("carrinho_produto", ["fk_id_carrinho"], [1], data_to_insert) """

# Case where there are two params of search
""" update_data("carrinho_produto", ["fk_id_carrinho", "fk_id_produto"], [1, 1], data_to_insert) """

# Delete
# Case where there are only one param of search
""" delete_data("carrinho_produto", ["fk_id_carrinho"], [1]) """
# Case where there are two params of search
""" delete_data("carrinho_produto", ["fk_id_carrinho", "fk_id_produto"], [1, 1]) """


# Get next id
""" print(get_next_id("produto", "id_produto"))  """

# Check if id exists
""" print(check_id("produto", "id_produto", 4)) """
