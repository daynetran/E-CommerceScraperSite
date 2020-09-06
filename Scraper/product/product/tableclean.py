import numpy as np # pip3 install numpy
import math
import csv
import pandas as pd
from datascience import * # pip3 install datascience


def clean_table(table_path):
    table = Table().read_table(table_path)
    for i in range(len(table[0])):
        # ranks
        # table.column('ranks')[i] += 1 # to account for rank starting at 0

        # brand
        brand_string = table.column('brand')[i]
        if 'Visit the' in brand_string:
            brand_string.replace('Visit the ', '')
        elif 'Brand:' in brand_string:
            brand_string.replace('Brand: ', '')
        table.column('brand')[i] = brand_string

        # price
        price_string = table.column('price')[i]
        if '$' not in price_string:
            table.column('price')[i] = None
        else:
            new_price = price_string.replace('$', '')
            if ',' in new_price:
                new_price = new_price.replace(',', '')
            elif '-' in new_price:
                first_price = new_price[:new_price.index('-') - 1]
                second_price = new_price[new_price.index('-') + 2:]
                new_price = (float(first_price) + float(second_price)) / 2
            table.column('price')[i] = float(new_price)

        # discounted price
        list_price_string = table.column('list_price')[i]
        if '$' not in list_price_string:
            table.column('list_price')[i] = None
        else:
            new_list_price = list_price_string.replace('$', '')
            if ',' in new_list_price:
                new_list_price = new_list_price.replace(',', '')
            elif '-' in new_list_price:
                first_list_price = new_list_price[:new_list_price.index('-') - 1]
                second_list_price = new_list_price[new_list_price.index('-') + 2:]
                new_list_price = (float(first_list_price) + float(second_list_price)) / 2
            table.column('list_price')[i] = float(new_list_price)

        # rating
        rating_string = table.column('rating')[i]
        if 'out of 5' in rating_string:
            new_rating = float(rating_string.replace(' out of 5', ''))
            table.column('rating')[i] = new_rating
        else:
            table.column('rating')[i] = None

        # num_reviews
        num_string = table.column('num_reviews')[i]
        if 'ratings' in num_string:
            new_num = num_string.replace(' ratings', '')
            table.column('num_reviews')[i] = new_num
        else:
            table.column('num_reviews')[i] = None

    return table.sort('rank', descending = False)


def create_csv(table, name):
    headers = ['Brand', 'Description', 'Link', 'List Price ($)', 'Product Name', '# Reviews', 'Price ($)', 'Rank', 'Rating']
    rows = []
    for i in range(len(table[0])):
        new_row = []
        for j in range(len(table)):
            new_row.append(table[j][i])
        rows.append(new_row)
    cleaned_table = pd.DataFrame(rows, columns=headers)
    cleaned_table = cleaned_table[['Rank', 'Product Name', 'Brand', 'Price ($)', 'Rating', '# Reviews', 'Link', 'Description', 'List Price ($)']]
    cleaned_table.to_csv("Cleaned_{}.csv".format(name), index=False)