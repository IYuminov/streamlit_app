import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
import streamlit as st 
st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Анализ отклика от клиентов на предложения банка')
st.write('Исследование данных начнем с рассмотрения целевой переменной')
df = pd.read_csv('application_data.csv').drop(['Unnamed: 0'], axis= 1)
def draw_pie(column_group: str, title_plot: str, data= df, target= 'TARGET', label_1= None, label_2= None): 
    fig, axs = plt.subplots(nrows= 1 , ncols= 2, figsize=(15, 15))
    label_data_1 = list(data[data[target] == 1].groupby(column_group)[column_group].count().index)
    value_data_1 = list(data[data[target] == 1].groupby(column_group)[column_group].count().values)
    label_data = list(data[data[target] == 0].groupby(column_group)[column_group].count().index)
    value_data = list(data[data[target] == 0].groupby(column_group)[column_group].count().values) 
    if len(label_data) == 2:
        label_data[0], label_data[1] = label_1, label_2
        label_data_1[0], label_data_1[1] = label_1, label_2
    axs[0].pie(value_data, labels= label_data, autopct='%1.1f%%')
    axs[1].pie(value_data_1, labels= label_data_1, autopct='%1.1f%%')
    axs[0].set_title(f'{title_plot} из НЕ воспользовавшихся ')
    axs[1].set_title(f'{title_plot} из воспользовавшихся ')
    st.pyplot(fig)
def draw_hist(column_group: str, title_plot: str, data= df, target= 'TARGET', label_1= 'Не воспользовались', label_2= 'Воспользовались'):
    fig, ax = plt.subplots()
    plt.hist(data[column_group], label= 'Всего')
    plt.hist(data[data[target] == 0][column_group], label= label_1)
    plt.hist(data[data[target] == 1][column_group], label= label_2)
    plt.xlabel(title_plot)
    plt.title(f'{title_plot} клиентов')
    plt.legend()
    st.pyplot(fig)
def draw_barh(column_group: str, title_plot: str, data= df, target= 'TARGET', label_1= "Не воспользовались", label_2= 'Воспользовались'):
    label_data_1 = list(data[data[target] == 1].groupby(column_group)[column_group].count().index)
    value_data_1 = list(data[data[target] == 1].groupby(column_group)[column_group].count().values)
    label_data = list(data[data[target] == 0].groupby(column_group)[column_group].count().index)
    value_data = list(data[data[target] == 0].groupby(column_group)[column_group].count().values)
    fig, ax = plt.subplots(figsize =(10, 5))
    plt.barh(label_data, value_data, label= label_1)
    plt.barh(label_data_1, value_data_1, label= label_2)
    if len(label_data) < 10:
        count = 0
        for i in ax.patches:
            if count < len(ax.patches)/2:
                plt.text(
                    i.get_width() + 100,
                    i.get_y() + 0.15, 
                    str(round((i.get_width()), 2)),
                    color= 'grey'
                    )
            else:
                plt.text(
                    i.get_width() + 100,
                    i.get_y() + 0.45, 
                    str(round((i.get_width()), 2)),
                    color= 'black'
                    )
            count += 1
    ax.set_title(f'{title_plot} клиентов',
                loc= 'left')            
    ax.legend(title= "Отклик клиентов")
    st.pyplot(fig)
label_target = list(df.groupby('TARGET')['TARGET'].count().index)
label_target[0] = 'Не воспользовались'
label_target[1] = 'Воспользовались'
value_target = list(df.groupby('TARGET')['TARGET'].count().values)
fig_pie, ax = plt.subplots()
plt.pie(value_target, labels=label_target, autopct='%1.1f%%')
plt.title("Распределение клиентов по таргету")
st.pyplot(fig_pie)
st.write('Наблюдаем сильный дисбаланс классов')
st.subheader('Матрица корреляции числовых признаков')
num_features_df = [i for i in df.columns if (df[i].dtype == 'int') | (df[i].dtype == 'float')]
num_features_df.remove('ID')
int_float_features = df[num_features_df]
corr_matrix_int_float = int_float_features.corr()
figure, ax = plt.subplots(figsize=(20, 10))
sns.heatmap(corr_matrix_int_float, annot=True, ax=ax)
st.pyplot(figure)
st.write('Из тепловой карты корреляции по числовым признакам данных сильных зависимостей у переменных с таргетом нет, но наблюдаются сильные линейные взаимосвязи между некоторыми признаками')
st.subheader('Возраст клиентов банка')
draw_hist(
    column_group= 'AGE',
    title_plot= 'Возраст'
    )
st.write('На графике изображены общее распределение клиентов банка по возрасту и в разрезе целевой переменной')
st.subheader('Разделение по полу клиентов банка')
draw_pie(
    column_group= 'GENDER',
    title_plot= 'Пол клиентов',
    label_1= 'Женщины',
    label_2= 'Мужчины'
    )
st.write('Видим преобладание мужского пола среди клиентов банка')
st.subheader('Полученное образоавние клиентами')
draw_barh(
    column_group= 'EDUCATION', 
    title_plot= 'Образование'
    )
st.write('Числами обозначены количество людей в каждом классе среде откликнувшихся и проигнорировавших предложение')
st.subheader('Семейное положение клиентов банка')
draw_pie(
    column_group= 'MARITAL_STATUS',
    title_plot= 'Семейное положение'
    )
st.write('Видим преобладание клиентов состоящих в браке. Также, хочется отметить что распределения по данному признаку схожи среди откликнувшихся и проигнорировавших.')
st.subheader('Количество детей в семьях клиентов')
draw_hist(
    column_group= 'CHILD_TOTAL',
    title_plot= 'Количество детей'
    )
st.write('Сохраняется тенденция к отклику на предложения на уровне остальных признаков.')
st.subheader('Количество несовершеннолетних детей в семьях клиентов')
draw_hist(
    column_group= 'DEPENDANTS',
    title_plot= 'Количество иждивенцев'
    )
st.subheader('Количество клиентов пенсионного возраста от непенсионного')
draw_pie(
    column_group= 'SOCSTATUS_PENS_FL',
    title_plot= 'Социальный статус',
    label_1= 'Не пенсионер',
    label_2= 'Пенсионер'
    )
st.write('Судя по данному графику люди пенсионного возраста менее активно берут заёмы')
st.subheader('Наличие работы у клиентов банка')
draw_pie(
    column_group= 'SOCSTATUS_WORK_FL',
    title_plot= 'Социальный статус',
    label_1= 'Не работает',
    label_2= 'Работает',
    )
st.subheader('Совпадает ли адрес места пребывания с местом регистрации клиента?')
draw_pie(
    column_group= 'MATCH_ADDRESS',
    title_plot= 'Совпадение адреса',
    label_1= 'Не совпадает',
    label_2= 'Совпадает',
    )
st.write('Видим что клиенты у которых адрес несовпадает отвечают на предложения банка чаще.')
st.subheader('Наличие жилья у клиентов банка')
draw_pie(
    column_group= 'FL_PRESENCE_FL',
    title_plot= 'Наличие жилья в собственности',
    label_1= 'Нет',
    label_2= 'Есть',
    )
st.write('По данному признаку видим, что в целом сохраняется распределение откликнувшися и проигнорировавших')
st.subheader('Количество автомобилей в собственности клиентов')
draw_pie(
    column_group= 'OWN_AUTO',
    title_plot= 'Количество авто в собственности'
    )
st.subheader('Количество клиентов по индуйстриям в разрезе таргета')
draw_barh(
    column_group= 'GEN_INDUSTRY', 
    title_plot= 'Отрасль работы'
    )
st.subheader('Всего кредитов у клиента')
draw_barh(
    column_group= 'GEN_TITLE', 
    title_plot= 'Отрасль работы'
    )
st.subheader('Количество закрытых кредитов у клиента ')
draw_barh(
    column_group= 'COUNT_CLOSED_LOAN', 
    title_plot= 'Количество закрытых кредитов'
    )
