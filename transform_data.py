import pandas as pd
import os
from numpy import where


list_name_datasets = list()
for file_name in sorted(os.listdir('datasets/')):
    if (file_name[0] != '.') and (file_name[-4:] == '.csv') and (file_name[:2] == 'D_'):
        locals()[f"df_{file_name[:-4]}"] = pd.read_csv('datasets/{}'.format(file_name))
        list_name_datasets.append(f"df_{file_name[:-4]}")


df = df_D_clients.merge(df_D_target, left_on= 'ID', right_on= 'ID_CLIENT', how= 'left').drop(['ID_CLIENT'], axis=1)
df = df.merge(df_D_job, left_on= 'ID', right_on= 'ID_CLIENT', how= 'left').drop(['ID_CLIENT'], axis=1)
df = df.merge(df_D_salary, left_on= 'ID', right_on= 'ID_CLIENT', how= 'left').drop_duplicates().drop(['ID_CLIENT'], axis=1)
df = df.merge(df_D_last_credit, left_on= 'ID', right_on= 'ID_CLIENT', how= 'left').drop(['ID_CLIENT'], axis=1)


# количество всего кредитов у клиента
count_all_credis = pd.DataFrame(df_D_loan.merge(df_D_close_loan, left_on= 'ID_LOAN', right_on= 'ID_LOAN', how= 'left')\
    .groupby('ID_CLIENT')['ID_LOAN'].count()).reset_index()\
        .rename(columns={'ID_LOAN': 'COUNT_LOAN'})

# количество закрытых кредитов у клиента
count_closed_credis = pd.DataFrame(df_D_loan.merge(df_D_close_loan, left_on= 'ID_LOAN', right_on= 'ID_LOAN', how= 'left')\
    .groupby('ID_CLIENT')['CLOSED_FL'].sum()).reset_index()\
        .rename(columns={'CLOSED_FL': 'COUNT_CLOSED_LOAN'})


df = df.merge(count_all_credis, left_on= 'ID', right_on= 'ID_CLIENT', how= 'left').drop(['ID_CLIENT'], axis=1)
# df['COUNT_LOAN'] = df['COUNT_LOAN'].fillna(0)
df = df.merge(count_closed_credis, left_on= 'ID', right_on= 'ID_CLIENT', how= 'left').drop(['ID_CLIENT'], axis=1)
# df['COUNT_CLOSED_LOAN'] = df['COUNT_CLOSED_LOAN'].fillna(0)

# если адрес проживания совпадает с адресом регистрации - 1, иначе - 0
df['MATCH_ADDRESS'] = where(df['REG_ADDRESS_PROVINCE'] != df['FACT_ADDRESS_PROVINCE'], 0, 1)


df.to_csv('application_data.csv')
