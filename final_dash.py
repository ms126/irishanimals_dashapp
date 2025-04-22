import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Initialize Dash app with Bootstrap for styling
app = dash.Dash(__name__, external_stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css"])

# Read in data and clean column names
df = pd.read_csv("/Users/misha/Downloads/Data Viz/Final Project/irish_animals.csv")
df.columns = df.columns.str.replace(r"[()]", "", regex=True).str.replace(" ", "_")

# Custom color scheme and font setup
app.layout = html.Div(
    style={"backgroundColor": "#382d22", "padding": "20px", "fontFamily": "Arial, sans-serif"},
    children=[
        html.H1("🍀 Irish Wildlife Dashboard 🐾", 
                className="text-center mt-4", 
                style={"color": "#c2adff", "fontSize": "40px", "fontWeight": "bold", "letterSpacing": "2px"}),

        # Dropdown for selecting animal
        dcc.Dropdown(
            id="animal-dropdown",
            options=[{"label": name, "value": name} for name in df.Name],
            value=df.Name[0],
            className="m-3",
            style={"width": "50%", "backgroundColor": "#c2adff", "borderColor": "#2c3e50", "fontSize": "16px"}
        ),
        
        # Animal info card with rounded corners and shadow effect
        html.Div(id="animal-info", className="container p-3 shadow-lg rounded", style={"backgroundColor": "#c2adff"}),

        # Graphs container with improved spacing and styling
        html.Div([
            dcc.Graph(id="population-chart", className="col-md-6", config={"displayModeBar": False}),
            dcc.Graph(id="size-weight-chart", className="col-md-6", config={"displayModeBar": False}),
        ], className="row g-4"),

        # Additional interactive graphs
        dcc.Graph(id="lifespan-chart", className="mt-4", config={"displayModeBar": False}),
        dcc.Graph(id="animal-pie-chart", className="mt-4", config={"displayModeBar": False}),
        dcc.Graph(id="correlation-heatmap", className="mt-4", config={"displayModeBar": False}),
    ]
)

# Callback to update the charts based on selected animal
@app.callback(
    [Output("animal-info", "children"),
     Output("population-chart", "figure"),
     Output("size-weight-chart", "figure"),
     Output("lifespan-chart", "figure"),
     Output("animal-pie-chart", "figure"),
     Output("correlation-heatmap", "figure")],
    [Input("animal-dropdown", "value")]
)
def update_charts(selected_animal):
    animal_data = df[df.Name == selected_animal]

    # Info card with rounded corners and smooth transitions
    info_card = html.Div([
        html.H3(f"{selected_animal}", style={"color": "#2980B9", "fontSize": "24px", "fontWeight": "bold"}),
        html.P(f"🌍 Population: {animal_data.Population.values[0]:,}", style={"fontSize": "16px", "color": "#34495e"}),
        html.P(f"📏 Size: {animal_data.Size_min_cm.values[0]} - {animal_data.Size_max_cm.values[0]} cm", style={"fontSize": "16px", "color": "#34495e"}),
        html.P(f"⚖️ Weight: {animal_data.Weight_min_kg.values[0]} - {animal_data.Weight_max_kg.values[0]} kg", style={"fontSize": "16px", "color": "#34495e"}),
        html.P(f"⌛ Lifespan: {animal_data.Lifespan_min_years.values[0]} - {animal_data.Lifespan_max_years.values[0]} years", style={"fontSize": "16px", "color": "#34495e"})
    ], className="p-3 rounded shadow-sm", style={"backgroundColor": "#ECF0F1"})
    
    # Population Bar Chart with custom colors and smooth transition
    pop_fig = px.bar(df, x="Name", y="Population", title="Population of Irish Animals",
                     color="Population", height=400, 
                     color_continuous_scale="Viridis", labels={"Population": "Population (in millions)"})
    pop_fig.update_layout(
        title_font={"size": 22, "family": "Arial", "color": "#2980B9"},
        plot_bgcolor="#f8f8f8",
        paper_bgcolor="#f8f8f8",
        margin={"l": 50, "r": 50, "t": 50, "b": 50},
        transition_duration=500
    )
    
    # Size vs Weight Scatter Plot with custom hover effects
    size_weight_fig = px.scatter(df, x="Size_max_cm", y="Weight_max_kg", size="Population", color="Name",
                                 title="Size vs. Weight of Animals", height=400, 
                                 hover_data=["Name", "Population", "Size_max_cm", "Weight_max_kg"])
    size_weight_fig.update_layout(
        title_font={"size": 22, "family": "Arial", "color": "#2980B9"},
        plot_bgcolor="#f8f8f8",
        paper_bgcolor="#f8f8f8",
        margin={"l": 50, "r": 50, "t": 50, "b": 50},
        transition_duration=500
    )

    # Lifespan Range Bar Chart with color changes for lifespans
    lifespan_fig = px.bar(df, x="Name", y=["Lifespan_min_years", "Lifespan_max_years"],
                          title="Lifespan Range of Animals", barmode="group", height=400)
    lifespan_fig.update_layout(
        title_font={"size": 22, "family": "Arial", "color": "#2980B9"},
        plot_bgcolor="#f8f8f8",
        paper_bgcolor="#f8f8f8",
        margin={"l": 50, "r": 50, "t": 50, "b": 50},
        transition_duration=500
    )

    # Pie Chart: Population Distribution by Animal Type with gradient colors
    pop_pie_fig = px.pie(df, names="Name", values="Population", title="Population Distribution of Animals",
                         height=400, color_discrete_sequence=px.colors.sequential.RdBu)
    pop_pie_fig.update_layout(
        title_font={"size": 22, "family": "Arial", "color": "#2980B9"},
        plot_bgcolor="#f8f8f8",
        paper_bgcolor="#f8f8f8",
        margin={"l": 50, "r": 50, "t": 50, "b": 50},
        transition_duration=500
    )

    # Correlation Heatmap with smooth color scale and annotations
    correlation_df = df[['Size_max_cm', 'Weight_max_kg', 'Lifespan_min_years', 'Lifespan_max_years']]
    correlation_matrix = correlation_df.corr()
    heatmap_fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='YlGnBu', 
        colorbar=dict(title="Correlation"),
        showscale=True,
        hoverongaps=False
    ))
    heatmap_fig.update_layout(
        title="Correlation Heatmap (Size, Weight, Lifespan)", 
        title_font={"size": 22, "family": "Arial", "color": "#2980B9"},
        plot_bgcolor="#f8f8f8",
        paper_bgcolor="#f8f8f8",
        margin={"l": 50, "r": 50, "t": 50, "b": 50},
        transition_duration=500
    )

    return info_card, pop_fig, size_weight_fig, lifespan_fig, pop_pie_fig, heatmap_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

