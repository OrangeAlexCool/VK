import pandas as pd

def find_best_days(file_name):
    # Загрузка данных из файла
    df = pd.read_csv(file_name, sep='\t')

    # Преобразование timestamp в формат даты
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    _year = df['timestamp'].dt.year.unique()

    # Определение первого и последнего месяца за все время
    first_year = df['year'].min()
    last_year = df['year'].max()
    first_month = df[df['year'] == first_year]['month'].min()
    last_month = df[df['year'] == last_year]['month'].max()

    months_for_each_year = {}
    for year in sorted(df['year'].unique()):
        months_for_each_year[year] = sorted(df[df['year'] == year]['month'].unique())

    months_for_each_year[first_year].remove(first_month)
    months_for_each_year[last_year].remove(last_month)

    # Фильтрация данных по первому визиту пользователя
    df = df.sort_values(by='timestamp').drop_duplicates('userid')

    best_days = pd.Series()

    # Нахождение лучшего дня для каждого месяца
    for year in _year:
        for month in months_for_each_year[year]:
            month_data = df[(df['year'] == year) & (df['month'] == month)]
            if not month_data.empty:
                best_day = month_data.loc[month_data['value'].idxmax()]['timestamp']
                best_days = best_days.append(pd.Series(best_day, index=[(year, month)]))

    # Сохранение итоговых данных в CSV файл
    result_data = pd.DataFrame(columns=['timestamp', 'value'])

    for (year, month), best_day in best_days.items():
        month_data = df[(df['year'] == year) & (df['month'] == month) & (df['timestamp'].dt.date == best_day.date())]
        total_value = month_data['value'].sum()
        if total_value != 0:
            result_data = result_data.append({'timestamp': best_day, 'value': total_value}, ignore_index=True)
    result_data.to_csv('output.csv', sep="\t" ,index=False)