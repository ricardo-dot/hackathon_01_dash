import pandas as pd


def catesian_format(dataframe, key):
    source_obj = {}
    for header in dataframe[key]:
        query = dataframe.query(f'{key} == "{header}"')
        fat_ven = query['fat_ven_faturamento'].to_list()
        source_obj[header] = fat_ven
    
    return pd.DataFrame.from_dict(source_obj)


def calculate_yoy(dataframe, query_string = None):
    if query_string:
        dataframe = dataframe.query(query_string)
        
    total = dataframe['fat_ven_faturamento'].sum()
    
    prior_current = (dataframe['dim_tem_ano']
                     .drop_duplicates()
                     .astype(int)
                     .nlargest(2)
                     .to_list()[-1])
    
    prior_current_total = (dataframe
                           .query(f"dim_tem_ano == '{prior_current}'")
                           .loc[:, 'fat_ven_faturamento']
                           .sum())
    yoy = ((total-prior_current_total)/prior_current_total) - 1
    return yoy