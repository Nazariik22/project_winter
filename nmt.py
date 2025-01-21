import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.dates as mdates

st.set_page_config(layout="wide")
data = pd.read_csv('Odata2024File.csv', sep=';')

def fourth():
    subjects = {
        'UkrBlockBall100': 'Українська мова',
        'HistBlockBall100': 'Історія',
        'MathBlockBall100': 'Математика',
        'PhysBlockBall100': 'Фізика',
        'ChemBlockBall100': 'Хімія',
        'BioBlockBall100': 'Біологія',
        'GeoBlockBall100': 'Географія',
        'EngBlockBall100': 'Англійська мова',
        'FraBlockBall100': 'Французька мова',
        'DeuBlockBall100': 'Німецька мова',
        'SpaBlockBall100': 'Іспанська мова',
        'UkrLitBlockBall100': 'Українська література'
    }
    data['TestDate'] = pd.to_datetime(data['TestDate'], errors='coerce')
    st.title("Графік середнього балу за датами")
    st.write("Це дослідження дозволяє відслідковувати динаміку результатів НМТ з різних предметів по датах і робити висновки щодо можливих змін або тенденцій в успішності учасників.")
    st.write("Оберіть предмети для відображення на графіку:")
    selected_subjects = st.multiselect(
        "Предмети",
        options=list(subjects.keys()),
        format_func=lambda x: subjects[x] 
    )

    if selected_subjects:
        filtered_data = data[['TestDate'] + selected_subjects].copy()
        for subject in selected_subjects:
            filtered_data[subject] = pd.to_numeric(filtered_data[subject].str.replace(',', '.'), errors='coerce')
        averages_by_date = (
            filtered_data.groupby('TestDate')[selected_subjects]
            .mean()
            .reset_index()
        )

        plt.figure(figsize=(10, 6))
        for subject in selected_subjects:
            plt.plot(
                averages_by_date['TestDate'], 
                averages_by_date[subject], 
                label=subjects[subject]
            )

        plt.title("Середній бал за датами")
        plt.xlabel("Дата проведення тесту")
        plt.ylabel("Середній бал")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.write("Оберіть хоча б один предмет для побудови графіку.")

def fifth():
    subjects = {
        'UkrBlockBall100': 'Українська мова',
        'HistBlockBall100': 'Історія',
        'MathBlockBall100': 'Математика',
        'PhysBlockBall100': 'Фізика',
        'ChemBlockBall100': 'Хімія',
        'BioBlockBall100': 'Біологія',
        'GeoBlockBall100': 'Географія',
        'EngBlockBall100': 'Англійська мова',
        'FraBlockBall100': 'Французька мова',
        'DeuBlockBall100': 'Німецька мова',
        'SpaBlockBall100': 'Іспанська мова',
        'UkrLitBlockBall100': 'Українська література'
    }
    data['TestDate'] = pd.to_datetime(data['TestDate'], errors='coerce')
    subject_names = []
    students_counts = []
    average_scores = []
    average_deviation = []
    for code, name in subjects.items():
        if code in data.columns:
            subject_data = pd.to_numeric(data[code].str.replace(',', '.'), errors='coerce').dropna()
            if not subject_data.empty:
                subject_names.append(name)
                students_counts.append(len(subject_data))
                average_scores.append(subject_data.mean())
                average_deviation.append((subject_data - subject_data.mean()).abs().mean())
    summary_table = pd.DataFrame({
        '№': range(1, len(subject_names) + 1), 
        'Назва предмету': subject_names,
        'Кількість учнів': students_counts,
        'Середній бал': average_scores,
        'Середнє відхилення': average_deviation
    })
    st.write("Підсумкова таблиця результатів (усі дані):")
    st.table(summary_table.set_index('№'))
    selected_date = st.date_input("Виберіть дату для фільтрації", min_value=data['TestDate'].min(), max_value=data['TestDate'].max())
    if selected_date:
        filtered_data = data[data['TestDate'] == pd.to_datetime(selected_date)]
        subject_names_filtered = []
        students_counts_filtered = []
        average_scores_filtered = []
        average_deviation_filtered = []
        for code, name in subjects.items():
            if code in filtered_data.columns:
                subject_data = pd.to_numeric(filtered_data[code].str.replace(',', '.'), errors='coerce').dropna()
                if not subject_data.empty:
                    subject_names_filtered.append(name)
                    students_counts_filtered.append(len(subject_data))
                    average_scores_filtered.append(subject_data.mean())
                    average_deviation_filtered.append((subject_data - subject_data.mean()).abs().mean())
        filtered_summary_table = pd.DataFrame({
            '№': range(1, len(subject_names_filtered) + 1), 
            'Назва предмету': subject_names_filtered,
            'Кількість учнів': students_counts_filtered,
            'Середній бал': average_scores_filtered,
            'Середнє відхилення': average_deviation_filtered
        })
        st.write(f"Підсумкова таблиця результатів за {selected_date.strftime('%d.%m.%Y')}:")
        st.table(filtered_summary_table.set_index('№'))

def geografy(df):
    st.title('Аналіз географічного розташування учасників НМТ')
    res = st.segmented_control("Оберіть тип відображення:", ["2D - режим","3D - режим"])
    city_to_coords = pd.read_excel("unique_cities.xlsx")
    required_columns = {'city', 'lon', 'lat'}
    city_to_coords['lat'] = pd.to_numeric(city_to_coords['lat'])
    city_to_coords['lon'] = pd.to_numeric(city_to_coords['lon'])
    city_to_coords = city_to_coords[
        (city_to_coords['lat'].between(-90, 90)) &
        (city_to_coords['lon'].between(-180, 180))
    ]
    if res =="2D - режим":
        st.map(city_to_coords[["lat", "lon"]])
    elif res =="3D - режим":
        participants_count = df['TerName'].value_counts().reset_index()
        participants_count.columns = ['city', 'count']
        merged_data = pd.merge(city_to_coords, participants_count, left_on='city', right_on='city', how='left').fillna(0)
        merged_data['count'] = merged_data['count'].astype(int)
        layer = pdk.Layer(
            "ColumnLayer",
            merged_data,
            get_position=["lon", "lat"],
            get_elevation="count",
            elevation_scale=100,
            radius=500,
            get_fill_color="[200, 30, 0, 160]",
            pickable=True,
        )
        view_state = pdk.ViewState(
            longitude=30,
            latitude=49,
            zoom=4,
            pitch=50,
        )
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

def pupils_by_school():
    REGNAME_COLUMN = 'RegName'
    EONAME_COLUMN = 'EOName'
    st.title('Список учнів по обраному закладу освіти')
    st.write('Оберіть Регіон, ввівши його назву повністю, або частково. Після правильно введеного регіону оберіть заклад/заклади освіти.') 
    region_options = data[REGNAME_COLUMN].unique()
    matching_regions = None
    entered_region = st.text_input("Регіон")
    selected_region = None
    if entered_region:
        matching_regions = [region for region in region_options if entered_region.lower() in region.lower()]
    else:
        matching_regions = region_options

    if len(matching_regions) == 1:
        selected_region = matching_regions[0]
        st.write("Ви обрали регіон:", selected_region)
    elif len(matching_regions) > 1:
        st.write("Згідно введеного паттерну знайдено більше одного регіону. Будь ласка, уточніть пошук")
        for region in matching_regions:
            st.write(region)
    else:
        st.write("Ой лишенько! Не знайдено жодного регіону... Будь ласка, спробуйте уважніше")
    filtered_df = data[data[REGNAME_COLUMN].isin(matching_regions)]
    schools = filtered_df[EONAME_COLUMN].unique()
    selected_schools = st.multiselect("Обреіть школи", options=schools)
    if st.button("Відобразити"):
        if selected_schools:
            st.write(f"Ви обрали щаклади освіти: {', '.join(selected_schools)}")
            
            result_df = filtered_df[filtered_df[EONAME_COLUMN].isin(selected_schools)]
            result_df = result_df[['Birth','SexTypeName',REGNAME_COLUMN,'TerName',EONAME_COLUMN,'Test','TestDate',
                                   'UkrBlockStatus','UkrBlockBall100','UkrBlockBall',
                                   'MathBlockStatus','MathBlockBall100','MathBlockBall',
                                   'HistBlockStatus','HistBlockBall100','HistBlockBall',
                                   'EngBlockStatus','EngBlockBall100','EngBlockBall',
                                   'GeoBlockStatus','GeoBlockBall100','GeoBlockBall',
                                   'BioBlockStatus','BioBlockBall100','BioBlockBall',
                                   'PhysBlockStatus','PhysBlockBall100','PhysBlockBall',
                                   'ChemBlockStatus','ChemBlockBall100','ChemBlockBall',
                                   'UkrLitBlockStatus','UkrLitBlockBall100','UkrLitBlockBall',
                                   'DeuBlockStatus','DeuBlockBall100','DeuBlockBall',
                                   'SpaBlockStatus','SpaBlockBall100','SpaBlockBall']]
            result_df = result_df.reset_index(drop=True)  
            result_df['RowNumber'] = result_df.index + 1
            column_order = ['RowNumber'] + [col for col in result_df.columns if col != 'RowNumber']
            result_df = result_df[column_order]
            result_df = result_df.set_index('RowNumber')

            result_df = result_df.rename(columns={
                'RowNumber' : '№',
                'Birth' : 'РН',
                'SexTypeName' : 'Стать',
                REGNAME_COLUMN: 'Регіон',
                'TerName' : 'Район/Місто',
                EONAME_COLUMN: 'Школа',
                'Test' : 'Назва тесту',
                'TestDate' : 'Дата тесту',
                'UkrBlockStatus' : 'Укр. статус',
                'UkrBlockBall100' : 'Укр. бал 100',
                'UkrBlockBall' : 'Укр. бал',
                'MathBlockStatus' : 'Матем. статус',
                'MathBlockBall100' : 'Матем. бал 100',
                'MathBlockBall' : 'Математ. бал',
                'HistBlockStatus' : 'Історія статус',
                'HistBlockBall100' : 'Історія бал 100',
                'HistBlockBall' : 'Історія бал',
                'EngBlockStatus' : 'Англ. статус',
                'EngBlockBall100' : 'Англ. бал 100',
                'EngBlockBall' : 'Англ. бал',
                'GeoBlockStatus' : 'Геогр. сатус',
                'GeoBlockBall100' : 'Геогр. бал 100',
                'GeoBlockBall' : 'Геогр. бал',
                'BioBlockStatus' : 'Біологія статус',
                'BioBlockBall100' : 'Біологія бал 100',
                'BioBlockBall' : 'Біологія бал',
                'PhysBlockStatus' : 'Фізика статус',
                'PhysBlockBall100' : 'Фізика бал 100',
                'PhysBlockBall' : 'Фізика бал',
                'ChemBlockStatus' : 'Хімія статус',
                'ChemBlockBall100' : 'Хімія бал 100',
                'ChemBlockBall' : 'Хімія бал',
                'UkrLitBlockStatus' : 'Укр.літ. статус',
                'UkrLitBlockBall100' : 'Укр.літ. бал 100',
                'UkrLitBlockBall' : 'Укр.літ. бал',
                'DeuBlockStatus' : 'Німец. статус',
                'DeuBlockBall100' : 'Німец. бал 100',
                'DeuBlockBall' : 'Німец. бал',
                'SpaBlockStatus' : 'Іспанс. статус',
                'SpaBlockBall100' : 'Іспанс. бал 100',
                'SpaBlockBall' : 'Іспанс. бал'
            })

            st.dataframe(result_df)

        else:
            st.write("No test centers selected.")


def get_values(subject: str, base_line: str):
    subject_column = subject + "Ball100"
    df_filtered = data.dropna(subset=[subject_column])
    values = df_filtered[df_filtered[subject_column].between(str(base_line), "200")]
    return values

def process_baseline_level():

    st.write("У цьому пункті буде відображатись інформація про те скільки учасників здали НМТ вище якогось рівня.")
    st.write("Рівень можна задати самостійно.")

    baseline = st.slider("Оберіть рівень", 100, 200, 100)

    subjects = ["UkrBlock", "HistBlock", "MathBlock", "EngBlock"]
    subjects_values = []
    for subject in subjects:
        subjects_values.append(len(get_values(subject, baseline)))

    data = {
        "names": ["Українська мова", "Історія України", "Математика", "Англійська мова"],
        "values": subjects_values
    }

    fig = px.histogram(
        data,
        x="names",
        y="values",
        barmode="overlay",
        nbins=50,
        opacity=0.5,
        color="names",
        labels={
            "names": "Назва предмету",
            "values": "Кількість"
        },
        title=f"Кількість учасників які здали предмети вище {str(baseline)} балів"
    )
    fig.update_yaxes(title='Кількість')

    st.plotly_chart(fig)

    


selection = None  
with st.sidebar:  
    st.image("logo.jpg", width=170)
    st.title("Аналіз даних НМТ")   
    st.write('За замовчуванням використовуються дані 2024 року')
    uploaded_file = st.file_uploader('За бажанням - завантажте файл з даними інших років', type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, sep=';') 
    selection = st.radio("Що будемо дивитися:", ["Рівень проходження","Учні закладу","Географічне дослідження","Успішність за датою",
                                                 "Відхилення з предмету"])  
if  selection =="Рівень проходження":
    process_baseline_level()
elif selection == "Учні закладу" :
    pupils_by_school()
elif selection == "Географічне дослідження":  
    geografy(data)
elif selection == "Успішність за датою":
    fourth()

elif selection == 'Відхилення з предмету':
    fifth()