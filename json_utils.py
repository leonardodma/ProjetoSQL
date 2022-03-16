import json


def create_data(new_data, field_name):
    with open('data.json', 'r+', encoding='utf-8') as file:
        file_data = json.load(file)
        file_data[field_name].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=2)


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
        file.seek(0)
        json.dump(file_data, file, indent=4)


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
        file.seek(0)
        json.dump(file_data, file, indent=4)


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

data_to_insert = {
    "fk_id_carrinho": 1,
    "fk_id_produto": 4
}

# Case where there are only one param of search
""" update_data("carrinho_produto", ["fk_id_carrinho"], [1], data_to_insert) """

# Case where there are two params of search
""" update_data("carrinho_produto", ["fk_id_carrinho", "fk_id_produto"], [1, 1], data_to_insert) """

# Delete
# Case where there are only one param of search
""" delete_data("carrinho_produto", ["fk_id_carrinho"], [1]) """
# Case where there are two params of search
""" delete_data("carrinho_produto", ["fk_id_carrinho", "fk_id_produto"], [1, 1]) """
