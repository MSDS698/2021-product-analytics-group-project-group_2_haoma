import plotly.graph_objects as go
import plotly.express as px
import plotly
import pandas as pd
import numpy as np


def load_data_():
    df = pd.read_excel('code/backend/readmission_1.xlsx')
    df['percentage_admission'] = np.round((1 /
                                           (np.random.choice(np.arange(5, 25),
                                                             df.shape[0]))), 2)

    # for CA data
    df_CA = pd.DataFrame(np.round((1 /
                                   (np.random.choice(np.arange(8, 15),
                                                     df.shape[0]))), 2),
                         columns=['percentage_admission'])
    df_CA['Date'] = df['Date']

    # For National data
    df_nation = pd.DataFrame(np.round((1 /
                                       (np.random.choice(np.arange(6, 13),
                                                         df.shape[0]))), 2),
                             columns=['percentage_admission'])
    df_nation['Date'] = df['Date']

    df_sample = df.sample(frac=0.75)
    df_male = df_sample.loc[df_sample['Gender'] == 'M']
    df_female = df_sample.loc[df_sample['Gender'] == 'F']

    return df_sample, df_male, df_female, df_CA, df_nation


def get_monthly_sum_readmission_(df):
    output = df.groupby(by=[df['Date'].dt.month])['Patient ID'] \
        .count().reset_index()
    return output


def gender_line():
    _, df_male, df_female, _, _ = load_data_()
    df_male_monthly_sum = get_monthly_sum_readmission_(df_male)
    df_female_monthly_sum = get_monthly_sum_readmission_(df_female)

    # Plotting
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
             'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_male_monthly_sum['Date'],
                             y=df_male_monthly_sum['Patient ID'],
                             mode='lines',
                             name='Male',
                             line=dict(color='#08519c', width=2)))
    fig.add_trace(go.Scatter(x=df_female_monthly_sum['Date'],
                             y=df_female_monthly_sum['Patient ID'],
                             mode='lines',
                             name='Female',
                             line=dict(color='#cc3d33', width=3.3)))
    fig.update_layout(title=dict(text='Re-admission Rates in 2025',
                                 x=0.5,
                                 xanchor='center',
                                 font=dict(size=22)),
                      xaxis=dict(range=[0, 13],
                                 showgrid=False,
                                 tickmode='array',
                                 tickvals=df_male_monthly_sum['Date'],
                                 ticktext=month),
                      yaxis=dict(range=[0, 20],
                                 showgrid=True,
                                 zeroline=False,
                                 showline=False,
                                 showticklabels=True,
                                 gridcolor='#e5e5e5'),
                      showlegend=True,
                      plot_bgcolor='white',
                      legend=dict(orientation="h",
                                  yanchor="bottom",
                                  y=1.02,
                                  xanchor="right",
                                  x=1))

    output = plotly.offline.plot(fig, include_plotlyjs=True, output_type='div')
    return output


def get_monthly_avg_admission_(df):
    output = df.groupby(by=[df['Date'].dt.month])['percentage_admission'] \
        .mean().reset_index()
    return output


def readmission_compare_line():
    df_sample, _, _, df_CA, df_nation = load_data_()
    df_sample_monthly_avg = get_monthly_avg_admission_(df_sample)
    df_CA_monthly_avg = get_monthly_avg_admission_(df_CA)
    df_nation_monthly_avg = get_monthly_avg_admission_(df_nation)

    # Plotting
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
             'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    df_list = [df_sample_monthly_avg, df_CA_monthly_avg, df_nation_monthly_avg]
    df_names = ['Agency', 'CA', 'Nation']
    colors = ['#cc3d33', '#999999', '#999999']
    dash = [None, None, 'dash']
    width = [3.3, 1.9, 1.5]

    fig = go.Figure()
    for ind, df in enumerate(df_list):
        fig.add_trace(go.Scatter(x=df['Date'],
                                 y=df['percentage_admission'],
                                 mode='lines',
                                 name=df_names[ind],
                                 line=dict(color=colors[ind],
                                           dash=dash[ind],
                                           width=width[ind])))

    fig.update_layout(title=dict(
        text='Comparision to National and State Rates',
        x=0.5,
        xanchor='center',
        font=dict(size=22)),
        xaxis=dict(range=[0, 13],
                   showgrid=False,
                   tickmode='array',
                   tickvals=df_sample_monthly_avg['Date'],
                   ticktext=month,),
        yaxis=dict(range=[0.05, 0.15],
                   tickformat='.1%',
                   showgrid=True,
                   zeroline=False,
                   showline=False,
                   showticklabels=True
                   ),
        showlegend=True,
        plot_bgcolor='#e5e5e5',
        legend=dict(orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1))
    output = plotly.offline.plot(fig, include_plotlyjs=True, output_type='div')
    return output


def service_pie():
    df_sample, _, _, _, _ = load_data_()
    data = df_sample.groupby(by='Service')['Date'].count().reset_index() \
        .rename(columns={'Date': 'Count'})

    # Plotting
    colors = ['#eff3ff', '#cc3d33', '#f7fbff', '#c6dbef', '#9ecae1', '#deebf7']
    fig = go.Figure()
    fig.add_trace(go.Pie(labels=data['Service'], values=data['Count'],
                         pull=[0, 0.13, 0, 0, 0, 0]))

    fig.update_traces(textposition='inside',
                      textinfo='percent+label',
                      textfont_size=16,
                      marker=dict(colors=colors,
                                  line=dict(color='#e5e5e5', width=0.9)))

    fig.update_layout(
        title=dict(text='Re-admissions by Service',
                   x=0.45,
                   xanchor='center',
                   font=dict(size=22)))

    output = plotly.offline.plot(fig, include_plotlyjs=True, output_type='div')
    return output


def age_hist():
    df_sample, _, _, _, _ = load_data_()

    # Plotting
    colors = ['#08519c', ] * 13
    colors[4] = '#cc3d33'

    fig = go.Figure()

    fig.add_trace(go.Histogram(histfunc="count",
                  x=df_sample['Age'],
                  name='Age',  # name used in legend and hov
                  marker_color=colors,
                  opacity=0.8))

    fig.update_layout(
        title=dict(text='Re-admissions by Age',
                   x=0.5,
                   xanchor='center', font=dict(size=22)),
        xaxis=dict(),
        xaxis_title_text='Age',  # xaxis label
        bargap=0.1,  # gap between bars of adjacent location coordinates
        bargroupgap=0.03,  # gap between bars of the same location coordinates
        plot_bgcolor='#e5e5e5'
    )

    output = plotly.offline.plot(fig, include_plotlyjs=True, output_type='div')
    return output
