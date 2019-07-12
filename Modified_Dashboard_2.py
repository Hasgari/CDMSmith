import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go

df_cpms = pd.read_csv("https://github.com/Hasgari/CDMSmith/blob/master/CPMS.csv")
df_CR = pd.read_csv("https://github.com/Hasgari/CDMSmith/blob/master/Cost%20ratio.csv")

def CPMS(key):
    if key in list(df_cpms["CPMS as percent of Median VOT"]):
        return df_cpms[df_cpms["CPMS as percent of Median VOT"] == key]["Percent Diversion"].values[0]
    elif key < 1:
        return 100
    else:
        return 0

CPMS(0.2)

def Cost_ratio(key):
    if key in df_CR["Cost Ratio"]:
        return df_CR[df_CR["Cost Ratio"] == key]["% Use Toll Path"].values[0]
    elif key < 0.02:
        return 100
    else:
        return 0


df_weights = pd.read_csv("https://github.com/Hasgari/CDMSmith/blob/master/Weights.csv")
scenarios = df_weights.columns[1:]
print (scenarios)
diff_miles = list(range(26))
print (diff_miles)


def weight(diff_mile,scenario): 
    if diff_mile > 25:
        diff_mile = 25
    return df_weights[df_weights["Difference_miles"] == str(diff_mile)][scenario].values[0]



def max_adjust(scenario):
    return df_weights[df_weights["Difference_miles"] == "Max. Adjust"][scenario].values[0]
type(max_adjust("F"))

df_toll = pd.read_csv("https://github.com/Hasgari/CDMSmith/blob/master/Toll%20rates.csv")
df_toll.columns

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='An Interactive Dashboard for toll diversion analysis'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),
    
    html.Div([html.Label("T_toll"), dcc.Input(id = "T_toll",
    placeholder='Travel time on toll road',
    type='number',
    value = 28
)  ,
    html.Label("T_alt"),
    dcc.Input(id = "T_alt",
    placeholder = 'Travel time on alternate road',
    type ='number',
    value = 45
) ,
    html.Label("Dist_toll"),
    dcc.Input(id = "Dist_toll",
    placeholder = 'Distance on toll road',
    type = 'number',
    value = 24.5
)  ,
    html.Label("Dist_alt"),
    dcc.Input(id = "Dist_alt",
    placeholder='Distance on alternate road',
    type = 'number',
    value = 33
)  ,
    dcc.RadioItems(id = "Roadtype",
    options=[
        {'label': 'Road', 'value': 'Road'},
        {'label': 'Bridge', 'value': 'Bridge'},
    ],
    value='Road'
)    ,
    html.Label("Tolled_length"),
    dcc.Input(id = "Tolled_length",
    placeholder = 'Tolled length',
    type = 'number',
    value = 18
)  , 
    html.Label("VOT_PC"),
    dcc.Input(id = "VOT_PC",
    placeholder = 'Passenger car value of time',
    type = 'number',
    value = 0.3
),
    html.Label("VOT_Truck"),
    dcc.Input(id = "VOT_Truck",
    placeholder = 'Truck Value of Time',
    type = 'number',
    value = 0.65
),
    html.Label("VOC_PC"),
    dcc.Input(id = "VOC_PC",
    placeholder = 'Passenger car operational cost',
    type = 'number',
    value = 0.24
),
    html.Label("VOC_Truck"),
    dcc.Input(id = "VOC_Truck",
    placeholder = 'Truck operational cost',
    type = 'number',
    value = 0.7
)],style = {'marginBottom' : '50'}),

html.Div([
html.Div([
    html.Div([dcc.Graph(
        id='graph_1'
        
    )],style = {'marginBottom' : '30'}),
    html.Div([ dcc.Graph(
        id='graph_2'
        
    )],style = {'marginBottom' : '30'}) ,
    html.Div([dcc.Graph(
        id='graph_3'
        
    )],style = {'marginBottom' : '30'})],className = "six columns") ,

    html.Div([
        html.Div([dcc.Graph(
        id='graph_4'
        
    )],style = {'marginBottom' : '30'}),
                   
    html.Div([dcc.Graph(
        id='graph_5'
        
    )],style = {'marginBottom' : '30'}),
            html.Div([dcc.Graph(
        id='graph_6'
        
    )],style = {'marginBottom' : '30'})], className = "six columns")
                        
],className = "row")
])


@app.callback(output=[Output('graph_1', 'figure'),Output('graph_2', 'figure'),Output('graph_3', 'figure'),Output('graph_4', 'figure'),Output('graph_5', 'figure'),Output('graph_6', 'figure')],
              inputs=[Input('T_toll', 'value'), Input('T_alt', 'value'), Input('Dist_toll', 'value'), Input('Dist_alt', 'value'), Input('Roadtype', 'value'), Input('Tolled_length', 'value'), Input('VOT_PC', 'value'), Input('VOT_Truck', 'value'), Input('VOC_PC', 'value'), Input('VOC_Truck', 'value') ])

def update_figures(T_toll,T_alt,Dist_toll,Dist_alt,Roadtype,tolled_length,VOT_PC,VOT_Truck,VOC_PC,VOC_Truck):
    
    scenarios = df_weights.columns[1:]
    print (scenarios)
    diff_miles = list(range(26))
    print (diff_miles)
    
    def weight(diff_mile,scenario): 
        if diff_mile > 25:
            diff_mile = 25
        return df_weights[df_weights["Difference_miles"] == str(diff_mile)][scenario].values[0]



    def max_adjust(scenario):
        return df_weights[df_weights["Difference_miles"] == "Max. Adjust"][scenario].values[0]
    type(max_adjust("F"))

    diff_mile = abs(Dist_toll - Dist_alt) 
    df_toll["toll_pc"] = [x * tolled_length for x in df_toll["Toll_PC_Road"]] if Roadtype == "Road" else df_toll["Toll_PC_Bridge"] 
    df_toll["toll_truck"] = [x * tolled_length for x in df_toll["Toll_Truck_Road"]] if Roadtype == "Road" else df_toll["Toll_Truck_Bridge"]    
    df_toll["toll_pc"] = df_toll["toll_pc"].astype("float64")
    df_toll["toll_truck"] = df_toll["toll_truck"].astype("float64")
    df_toll["CR_PC"] = [(T_toll * VOT_PC + Dist_toll * VOC_PC + x)/(T_alt * VOT_PC + Dist_alt * VOC_PC) for x in df_toll["toll_pc"]]  
    df_toll["CR_truck"] = [(T_toll * VOT_Truck + Dist_toll * VOC_Truck + x)/(T_alt * VOT_Truck + Dist_alt * VOC_Truck) for x in df_toll["toll_truck"]]
    df_toll["Div_Percent_CR_PC"] = [Cost_ratio(round(x,2)) for x in df_toll["CR_PC"]]
    df_toll["Div_Percent_CR_Truck"] = [Cost_ratio(round(x,2)) for x in df_toll["CR_truck"]]
    print(df_toll.head())

    result = 0

    def toll_adjust (toll,VOC,scenario):
        result = (Dist_toll - Dist_alt) * VOC * weight (int(abs(Dist_toll - Dist_alt)), scenario)
        if abs(result) > abs(max_adjust(scenario) * toll):
            result = max_adjust(scenario) * toll * np.sign(result)
        return result

    for scenario in scenarios:
        df_toll["PC_adjustment_" + scenario] = [toll_adjust(x,VOC_PC,scenario) for x in df_toll["toll_pc"]]
        df_toll["Truck_adjustment_" + scenario] = [toll_adjust(x,VOC_Truck,scenario) for x in df_toll["toll_truck"]]

    print(df_toll.head())
    
    for scenario in scenarios:
        df_toll["CPMS_PC_" + scenario] = (df_toll["toll_pc"] + df_toll["PC_adjustment_" + scenario])/(T_alt - T_toll) if (T_alt - T_toll) > 0 else 300
        df_toll["CPMS_Truck_" + scenario] = (df_toll["toll_truck"] + df_toll["Truck_adjustment_" + scenario])/(T_alt - T_toll) if (T_alt - T_toll) > 0 else 300
        df_toll["Div_Percent_PC_" + scenario] = [CPMS(int(x*100/VOT_PC)) for x in df_toll["CPMS_PC_" + scenario]]
        df_toll["Div_Percent_Truck_" + scenario] = [CPMS(int(x*100/VOT_Truck)) for x in df_toll["CPMS_Truck_" + scenario]] 
    df_toll.head()
    df_toll[["Toll_PC_Road","Div_Percent_PC_M"]].head(30)
    
    
    column_set_1 = ["Div_Percent_CR_PC","Div_Percent_PC_A","Div_Percent_PC_B","Div_Percent_PC_C"]
    column_set_2 = ["Div_Percent_CR_PC","Div_Percent_PC_D","Div_Percent_PC_F","Div_Percent_PC_H","Div_Percent_PC_J","Div_Percent_PC_L","Div_Percent_PC_N"]
    column_set_3 = ["Div_Percent_CR_PC","Div_Percent_PC_D","Div_Percent_PC_F","Div_Percent_PC_H","Div_Percent_PC_J","Div_Percent_PC_L","Div_Percent_PC_N"]
    
    column_set_4 = ["Div_Percent_CR_Truck","Div_Percent_Truck_A","Div_Percent_Truck_B","Div_Percent_Truck_C"]
    column_set_5 = ["Div_Percent_CR_Truck","Div_Percent_Truck_D","Div_Percent_Truck_F","Div_Percent_Truck_H","Div_Percent_Truck_J","Div_Percent_Truck_L","Div_Percent_Truck_N"]
    column_set_6 = ["Div_Percent_CR_Truck","Div_Percent_Truck_D","Div_Percent_Truck_F","Div_Percent_Truck_H","Div_Percent_Truck_J","Div_Percent_Truck_L","Div_Percent_Truck_N"]
    
    
    
    name_set_1 = ["Cost-Ratio","Scenario A","Scenario B","Scenario C"]
    name_set_2 = ["Cost-Ratio","Scenario D","Scenario F","Scenario H","Scenario J","Scenario L","Scenario N"]
    name_set_3 = ["Cost-Ratio","Scenario E","Scenario G","Scenario I","Scenario K","Scenario M","Scenario O"]
    
    if Roadtype == "Road":
        colors = ["blue","orange","yellow","red","olive","orchid", "silver","sandybrown"]
        
        traces_1 = []
        
        for i in range(len(column_set_1)):
            traces_1.append(go.Scatter(
                    x=df_toll["Toll_PC_Road"],
                    y=df_toll[column_set_1[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_1[i]
                    ))
        layout_1 = go.Layout(
            title = "Passenger cars-Zero and Full Scenarios",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_1 = go.Figure(data = traces_1,layout = layout_1)  
            
        
        
        traces_2 = []
        
        for i in range(len(column_set_2)):
            traces_2.append(go.Scatter(
                    x=df_toll["Toll_PC_Road"],
                    y=df_toll[column_set_2[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_2[i]
                    ))
        layout_2 = go.Layout(
            title = "Passenger cars-max adjustment ratio = 0.75",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_2 = go.Figure(data = traces_2,layout = layout_2)
    
    
        
        traces_3 = []
        
        for i in range(len(column_set_3)):
            traces_3.append(go.Scatter(
                    x=df_toll["Toll_PC_Road"],
                    y=df_toll[column_set_3[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_3[i]
                    ))
        layout_3 = go.Layout(
            title = "Passenger cars-max adjustment ratio = 0.5",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_3 = go.Figure(data = traces_3,layout = layout_3)
        
        
        
        traces_4 = []
        
        
        for i in range(len(column_set_4)):
            traces_4.append(go.Scatter(
                    x=df_toll["Toll_Truck_Road"],
                    y=df_toll[column_set_4[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_1[i]
                    ))
        layout_4 = go.Layout(
            title = "Trucks-Zero and Full Scenarios",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_4 = go.Figure(data = traces_4,layout = layout_4)  
            
        
        
        traces_5 = []
        
        for i in range(len(column_set_5)):
            traces_5.append(go.Scatter(
                    x=df_toll["Toll_Truck_Road"],
                    y=df_toll[column_set_5[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_2[i]
                    ))
        layout_5 = go.Layout(
            title = "Trucks-max adjustment ratio = 0.75",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_5 = go.Figure(data = traces_5,layout = layout_5)
    
    
        
        traces_6 = []
        for i in range(len(column_set_6)):
            traces_6.append(go.Scatter(
                    x=df_toll["Toll_Truck_Road"],
                    y=df_toll[column_set_6[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_3[i]
                    ))
        layout_6 = go.Layout(
            title = "Trucks-max adjustment ratio = 0.5",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_6 = go.Figure(data = traces_6,layout = layout_6)
        
    else:
        colors = ["blue","orange","yellow","red","olive","orchid", "silver","sandybrown"]
        
        traces_1 = []
        
        for i in range(len(column_set_1)):
            traces_1.append(go.Scatter(
                    x=df_toll["Toll_PC_Bridge"],
                    y=df_toll[column_set_1[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_1[i]
                    ))
        layout_1 = go.Layout(
            title = "Passenger cars-Zero and Full Scenarios",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_1 = go.Figure(data = traces_1,layout = layout_1)  
            
        
        
        traces_2 = []
        
        for i in range(len(column_set_2)):
            traces_2.append(go.Scatter(
                    x=df_toll["Toll_PC_Bridge"],
                    y=df_toll[column_set_2[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_2[i]
                    ))
        layout_2 = go.Layout(
            title = "Passenger cars-max adjustment ratio = 0.75",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_2 = go.Figure(data = traces_2,layout = layout_2)
    
    
        
        traces_3 = []
        
        for i in range(len(column_set_3)):
            traces_3.append(go.Scatter(
                    x=df_toll["Toll_PC_Bridge"],
                    y=df_toll[column_set_3[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_3[i]
                    ))
        layout_3 = go.Layout(
            title = "Passenger cars-max adjustment ratio = 0.5",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_3 = go.Figure(data = traces_3,layout = layout_3)
        
        
        
        traces_4 = []
        
        
        for i in range(len(column_set_4)):
            traces_4.append(go.Scatter(
                    x=df_toll["Toll_Truck_Bridge"],
                    y=df_toll[column_set_4[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_1[i]
                    ))
        layout_4 = go.Layout(
            title = "Trucks-Zero and Full Scenarios",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_4 = go.Figure(data = traces_4,layout = layout_4)  
            
        
        
        traces_5 = []
        
        for i in range(len(column_set_5)):
            traces_5.append(go.Scatter(
                    x=df_toll["Toll_Truck_Bridge"],
                    y=df_toll[column_set_5[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_2[i]
                    ))
        layout_5 = go.Layout(
            title = "Trucks-max adjustment ratio = 0.75",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_5 = go.Figure(data = traces_5,layout = layout_5)
    
    
        
        traces_6 = []
        for i in range(len(column_set_6)):
            traces_6.append(go.Scatter(
                    x=df_toll["Toll_Truck_Bridge"],
                    y=df_toll[column_set_6[i]],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                            'size': 5,
                            'line': {'width': 0.5, 'color': colors[i]}
                            },
                    name = name_set_3[i]
                    ))
        layout_6 = go.Layout(
            title = "Trucks-max adjustment ratio = 0.5",
            xaxis={'title': 'Toll rates'},
            yaxis={'title': 'Percentage of diversion', 'range': [0, 100]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 40},
            hovermode='closest'
        )
        figure_6 = go.Figure(data = traces_6,layout = layout_6)

    return figure_1,figure_2,figure_3,figure_4,figure_5,figure_6
    
if __name__ == '__main__':
    app.run_server(debug=True)

