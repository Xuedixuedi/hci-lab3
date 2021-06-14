import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import random

app = dash.Dash()

# 数据集本身
df = pd.read_csv("./lab3-datasets/google-play-store-apps/googleplaystore.csv")

# 先读取一些unique信息
categories = df['Category'].unique()
types = df['Type'].unique()
content_rating = df['Content Rating'].unique()
genres = df['Genres'].unique()
rating = df['Rating'].unique()

# 版本信息
android_ver_all = df['Android Ver']
android_ver_all = [i for i in android_ver_all if i is not np.nan]
android_ver_all = np.array(android_ver_all)
version_category = [
    'Android 1+', 'Android 2+', 'Android 3+', 'Android 4+', 'Android 5+',
    'Android 6+', 'Android 7+', 'Android 8+', 'Varies with device'
]
version_category_number = [0] * len(version_category)

for item in android_ver_all:
    if item[0] == 'V':
        version_category_number[8] += 1
    else:
        version_category_number[int(item[0]) - 1] += 1

# 把rating里面不是数字和nan的删除掉
rating = np.delete(rating, np.where(rating == 'Free'))
float_rating = rating.astype(np.float64)
float_rating = float_rating[~np.isnan(float_rating)]

# 把category和type里面的nan删除
categories = [i for i in categories if i is not np.nan]
categories = np.array(categories)
types = [i for i in types if i is not np.nan]
types = np.array(types)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id="categories",
            options=[{'label': i, 'value': i} for i in categories],
            value='Choose a category'
        )
    ]),

    html.Div([
        dcc.RadioItems(
            id="types",
            options=[{'label': i, 'value': i} for i in types],
            value='Choose a type'
        )
    ]),
    html.Div([
        # scatter chart
        dcc.Graph(id='scatter-chart', animate=True)
    ]),
    # 评分Slider
    html.Div([
        dcc.Slider(
            id="rating",
            min=float_rating.min(),
            max=float_rating.max(),
            value=random.choice(float_rating),
            step=None,
            marks={str(rate): str(rate) for rate in df['Rating'].unique()}
        )
    ]),
    html.Div([
        # pie chart
        dcc.Graph(id='pie-chart', animate=True)
    ]),
    html.Div([
        # bar chart
        dcc.Graph(id='bar-chart', animate=True)
    ])

])


# scatter chart
# scatter point hover name:APP
# x axis: Reviews
# y axis: Install
# filter: Type
# select drop down: Category
@app.callback(
    dash.dependencies.Output('scatter-chart', 'figure'),
    [
        dash.dependencies.Input('categories', 'value'),
        dash.dependencies.Input('types', 'value')
    ]
)
def update_scatter_chart(category, type_name):
    df_scatter = df[df['Type'] == type_name]
    return {
        'data': [
            go.Scatter(
                x=df_scatter[df_scatter['Category'] == category]['Reviews'],
                y=df_scatter[df_scatter['Category'] == category]['Installs'],
                text=df_scatter[df_scatter['Category'] == category]['App'],
                customdata=df_scatter[df_scatter['Category'] == category]['App'],
                mode='markers',
                marker={
                    'size': 15,
                    'opacity': 0.5,
                    'line': {
                        'width': 0.5,
                        'color': 'white'
                    }
                }
            )
        ],
        'layout': go.Layout(
            xaxis={
                'title': 'Reviews',
            },
            yaxis={
                'title': 'Installs',
            },
            margin={
                'l': 40,
                'b': 30,
                't': 10,
                'r': 0
            },
            height=450,
            hovermode='closest')
    }


# Pie chart
# input:Rating
# 根据你选定的评分来看这个评分的电影Content Rating分布
@app.callback(
    dash.dependencies.Output('pie-chart', 'figure'),
    [
        dash.dependencies.Input('rating', 'value')
    ]
)
def update_pie_chart(rating):
    df_pie = df[df['Rating'] == rating]

    # filter Content Rating by Rating
    content_rating = df_pie['Content Rating'].value_counts()
    content_rating = pd.DataFrame(
        {'Content_Rating_Name': content_rating.index, 'Number': content_rating.values})  # 把series转化成dataframe
    content_rating_list = content_rating['Content_Rating_Name']
    content_rating_number = content_rating['Number']
    print(content_rating_number)
    return {
        'data': [
            go.Pie(
                labels=content_rating_list,
                values=content_rating_number,
            )
        ],
        'layout':
            go.Layout(
                margin={
                    'l': 130,
                    'b': 30,
                    't': 50,
                    'r': 0
                },
                height=300,
                hovermode='closest')
    }


@app.callback(
    dash.dependencies.Output('bar-chart', 'figure'),
    [
        dash.dependencies.Input('rating', 'value')
    ]
)
def update_bar_chart(rating):
    return {
        'data': [
            {
                'x': version_category,
                'y': version_category_number,
                'type': 'Scatter'
            }
        ],
        'layout':
            go.Layout(
                margin={
                    'l': 40,
                    'b': 50,
                    't': 20,
                    'r': 20
                },
                legend={
                    'x': 0,
                    'y': 1
                },
                height=280,
                hovermode='closest')
    }


# if __name__ == '__main__':


if __name__ == '__main__':
    print(version_category_number)
    app.run_server(debug=True, host='localhost')
