import pandas as pd
from dash import Dash, dash_table, html, dcc, Input, Output, callback
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
r = urllib.request.urlopen('https://raw.githubusercontent.com/alexmagno6m/render/main/BD_PRIMARIA_2025.csv')
df = pd.read_csv(r, sep=';')
#Para convertir la columna cedula de numero a string
df['CEDULA']=df['CEDULA'].astype(str)
df = df[['CEDULA', 'PROFESOR_O_CURSO', 'DIA','FRANJA', '1', '2', '3', '4', '5', '6', '7', '8']]
app = Dash(__name__)
server = app.server

''' For input field
                     id='professor_drop',
                     type="text",
                     autoComplete=False,
                     placeholder="Seleccione un curso o profesor"
'''
app.layout = html.Div([
    html.H2('Horario General Primaria 2025'),
    html.H2('Colegio Antonio Baraya IED'),
    html.Div([
        "Consulte su horario individual "
        "digite su numero de cedula sin puntos ni comas",
        html.Br(),
        "Si no visualiza su horario Verifique que no tiene ningun curso seleccionado en la",
        " lista desplegable de cursos",
        html.Br(),
        dcc.Input( id='professor_drop',
                   type="text",
                   autoComplete=False,
                   step=0,
                   placeholder="Cedula")
    ],
        style={'width': '40%'}
    ),
    html.Br(),
    html.Div([
        "Para consultar horario de un curso seleccionelo de la lista desplegable: ",
        "Importante. El campo cédula de arriba debe estar vacio",
        dcc.Dropdown(['101', '102', '103',
                      '201', '202', '203',
                      '301', '302', '303',
                      '401', '402', '403',
                      '501', '502', '503'],
                     id='dia_drop',
                     searchable=False,
                     placeholder="Seleccionar Curso")
    ],
        style={'width': '40%'}
    ),
    html.Div(
        ["Las franjas mayoritarias A y B, no son aplicables en primaria"]
    ),
    dash_table.DataTable(
        data=df.to_dict('records'),
        page_size=18,
        columns=[{'name': i, 'id': i} for i in df.columns],
        style_data_conditional=(
                [
                    {
                        'if': {
                            'filter_query': '{{{}}} is blank'.format(col),
                            'column_id': col
                        },
                        'backgroundColor': 'gray',
                        'color': 'white'
                    } for col in df.columns
                ]
                +
                [
                    {
                        'if': {
                            'filter_query': '{{{}}} contains "TP"'.format(col),
                            'column_id': col
                        },
                        'backgroundColor': '#b8e0d2',
                        'color': 'black'
                    } for col in df.columns
                ]
                +
                [
                    {
                        'if': {
                            'filter_query': '{{{}}} = "RA"'.format(col),
                            'column_id': col
                        },
                        'backgroundColor': '#c1fba4',
                        'color': 'black'
                    } for col in df.columns
                ]
                +
                [
                    {
                        'if': {
                            'filter_query': '{{{}}} = "RC"'.format(col),
                            'column_id': col
                        },
                        'backgroundColor': '#c1fba4',
                        'color': 'black'
                    } for col in df.columns
                ]
        ),
        style_cell_conditional=[
            {'if': {'column_id': 'PROFESOR_O_CURSO'},
             'width': '15%'},
            {'if': {'column_id': 'DIA'},
             'width': '10%'},

        ],
        id='my_table'

    ),
    html.Div([
        html.H3('Powered by Dash - Created by BitSmart | Alexander Acevedo (2016-2025)')
    ])

])


@callback(
    Output('my_table', 'data'),
    Input('professor_drop', 'value'),
    Input('dia_drop', 'value')
)
def update_dropdown(proff_v, day_v):
    dff = df.copy()
    if proff_v:
        dff = dff[dff.CEDULA == proff_v]
        return dff.to_dict('records')
    if day_v:
        dff = dff[dff.PROFESOR_O_CURSO == day_v]
        return dff.to_dict('records')


# un solo return al mismo nivel del if muestra toda la tabla
if __name__ == '__main__':
    app.run_server(debug=False)