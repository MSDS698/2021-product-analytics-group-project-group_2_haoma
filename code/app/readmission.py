import plotly.graph_objects as go
import plotly.express as px
import plotly
import pandas as pd

def load_data_():
    df = pd.read_excel('code/backend/readmission_1.xlsx')
    df_sample = df.sample(frac=0.65)
    df_male = df_sample.loc[df_sample['Gender'] == 'M']
    df_female = df_sample.loc[df_sample['Gender'] == 'F']
    return df_sample, df_male, df_female

def gender_hist():
    _, df_male, df_female = load_data_()

    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count",
        x=df_male['Date'],
        name='Male', # name used in legend and hov
        marker_color='#3378cc',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(histfunc="count",
        x=df_female['Date'],
        name='Female', # name used in legend and hov
        marker_color='#d82057',
        opacity=0.75
    ))

    fig.update_layout(
        xaxis_title_text='Time', # xaxis label
        bargap=0.1, # gap between bars of adjacent location coordinates
        bargroupgap=0.03 # gap between bars of the same location coordinates
    )
    output = plotly.offline.plot(fig, include_plotlyjs=True, output_type='div')
    return output

def service_pie():
    df_sample, _, _ = load_data_()
    data = df_sample.groupby(by='Service')['Date'].count().reset_index()
    fig = px.pie(data, values=data['Date'], names=data['Service'], color_discrete_sequence=px.colors.qualitative.T10)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    output = plotly.offline.plot(fig, include_plotlyjs=True, output_type='div')
    return output

def age_hist():
    df_sample, _, _ = load_data_()
    fig = px.histogram(df_sample, x="Age", color_discrete_sequence=['#40a1e5'], opacity=0.75)
    fig.update_layout(
        xaxis_title_text='Age', # xaxis label
        bargap=0.1, # gap between bars of adjacent location coordinates
        bargroupgap=0.03 # gap between bars of the same location coordinates
    )
    output = plotly.offline.plot(fig, include_plotlyjs=True, output_type='div')
    return output

