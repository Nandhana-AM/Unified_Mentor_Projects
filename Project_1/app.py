import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Assuming 'data' is your pandas DataFrame

# Function to create all figures
def create_figures(data):
    figures = {}

    # Plot attrition by department
    figures['department_attrition_fig'] = px.histogram(data, x='Department', color='Attrition', barmode='group', 
                                                       title='Attrition Rate by Department')
    
    # Plot attrition by job role
    figures['job_role_attrition_fig'] = px.histogram(data, x='JobRole', color='Attrition', barmode='group', 
                                                     title='Attrition Rate by Job Role')
    
    # Plot monthly income distribution by attrition
    figures['income_attrition_fig'] = px.box(data, x='Attrition', y='MonthlyIncome', color='Attrition', 
                                             title='Monthly Income Distribution by Attrition')
    
    # Plot attrition by overtime 
    if 'OverTime' in data.columns:
        figures['overtime_attrition_fig'] = px.histogram(data, x='OverTime', color='Attrition', barmode='group', 
                                                         title='Attrition by Overtime')
    
    # Plot attrition by business travel
    figures['travel_attrition_fig'] = px.histogram(data, x='BusinessTravel', color='Attrition', barmode='group', 
                                                   title='Attrition by Business Travel')
    
    # Plot years at company vs. attrition
    figures['tenure_attrition_fig'] = px.histogram(data, x='YearsAtCompany', color='Attrition', barmode='group', 
                                                   title='Years at Company vs. Attrition')
    
    # Plot the correlation heatmap
    numeric_data = data.select_dtypes(include=['float64', 'int64'])
    correlation_matrix = numeric_data.corr()
    figures['correlation_heatmap'] = px.imshow(correlation_matrix, text_auto=True, 
                                               title='Correlation Heatmap', aspect='auto', 
                                               color_continuous_scale='Viridis')  # Using a valid colorscale
    
    return figures

# Create the figures dictionary
figures = create_figures(data)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
layout_children = [
    dbc.Row([
        dbc.Col(html.H1('Employee Attrition Dashboard'), className='mb-2')
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=figures['department_attrition_fig']), className='mb-4')
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=figures['job_role_attrition_fig']), className='mb-4')
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=figures['income_attrition_fig']), className='mb-4')
    ]),
]

# Check if 'overtime_attrition_fig' exists in figures
if 'overtime_attrition_fig' in figures:
    layout_children.append(
        dbc.Row([
            dbc.Col(dcc.Graph(figure=figures['overtime_attrition_fig']), className='mb-4')
        ])
    )

layout_children.extend([
    dbc.Row([
        dbc.Col(dcc.Graph(figure=figures['travel_attrition_fig']), className='mb-4')
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=figures['tenure_attrition_fig']), className='mb-4')
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=figures['correlation_heatmap']), className='mb-4')
    ]),
])

# Set the layout of the app
app.layout = dbc.Container(layout_children)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
