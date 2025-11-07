"""
Happiness Prediction Analysis Dashboard
ETL Workshop 3 - Happiness Prediction Analysis

Enhancements included:
- KPI MBE (prediction bias).
- Histogram with reference line at global MAE.
- Geographic map (choropleth) by country according to mean error.
- Dynamic textual 'insights' block.
- Robust handling when filter leaves DataFrame empty.
- In regional visuals, negative R² is truncated to 0 for clarity.
"""

import os
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================================

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', 'happiness_db')
}

def get_database_connection():
    """Crea y retorna una conexión a la base de datos usando SQLAlchemy."""
    connection_string = (
        f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(connection_string)

# ============================================================================
# CARGA Y UTILIDADES
# ============================================================================

def load_data():
    """Carga los datos de predicciones desde la base de datos."""
    engine = get_database_connection()
    query = "SELECT * FROM predictions ORDER BY created_at DESC"
    df = pd.read_sql(query, engine)
    engine.dispose()
    return df

def _safe_len(x): 
    try:
        return len(x)
    except Exception:
        return 0

def _fmt(x, nd=4, na="N/A"):
    try:
        if x is None or (isinstance(x, float) and (np.isnan(x) or np.isinf(x))):
            return na
        return f"{x:.{nd}f}"
    except Exception:
        return na

def calculate_metrics(df, data_split=None):
    """
    Calculates performance metrics.
    Returns dict with MAE, RMSE, R², MBE (bias) and count.
    Returns NaN/N/A-friendly if df is empty.
    """
    if data_split:
        df = df[df['data_split'] == data_split]

    n = _safe_len(df)
    if n == 0:
        return {'mae': np.nan, 'rmse': np.nan, 'r2': np.nan, 'mbe': np.nan, 'count': 0}

    y_true = df['actual_happiness_score'].astype(float)
    y_pred = df['predicted_happiness_score'].astype(float)

    mae = mean_absolute_error(y_true, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    # If only one value, can't calculate R²; we return NaN
    r2 = r2_score(y_true, y_pred) if n > 1 else np.nan
    mbe = float((y_pred - y_true).mean())  # bias: positive = overpredicts

    return {'mae': mae, 'rmse': rmse, 'r2': r2, 'mbe': mbe, 'count': n}

# ============================================================================
# COLORES Y ESTILOS
# ============================================================================

COLORS = {
    'train': '#1f77b4',      # Blue for train
    'test': '#ff7f0e',       # Orange for test
    'all': '#2ca02c',        # Green for all
    'background': '#f8f9fa',
    'card': '#ffffff',
    'text': '#212529',
    'border': '#dee2e6',
    'accent': '#007bff'
}

CARD_STYLE = {
    'backgroundColor': COLORS['card'],
    'padding': '20px',
    'borderRadius': '10px',
    'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
    'marginBottom': '20px'
}

# ============================================================================
# APP
# ============================================================================

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Happiness Prediction Dashboard"

# Cargar datos inicial
df_global = load_data()

# ============================================================================
# LAYOUT
# ============================================================================

app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🌍 Happiness Prediction Analysis Dashboard",
                style={'color': COLORS['text'], 'marginBottom': '10px'}),
        html.P("Complete analysis of linear regression model | ETL Workshop 3",
               style={'color': '#6c757d', 'fontSize': '16px'})
    ], style={
        'backgroundColor': COLORS['card'],
        'padding': '30px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'marginBottom': '30px',
        'textAlign': 'center'
    }),

    # Filtros
    html.Div([
        html.H3("🔍 Filters", style={'marginBottom': '20px', 'color': COLORS['text']}),
        html.Div([
            html.Div([
                html.Label("Dataset:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.RadioItems(
                    id='dataset-filter',
                    options=[
                        {'label': ' All', 'value': 'all'},
                        {'label': ' Training', 'value': 'train'},
                        {'label': ' Test', 'value': 'test'}
                    ],
                    value='all',
                    inline=True,
                    style={'marginTop': '5px'}
                )
            ], style={'flex': '1', 'marginRight': '20px'}),

            html.Div([
                html.Label("Region:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='region-filter',
                    options=[{'label': 'All regions', 'value': 'all'}] +
                            [{'label': region, 'value': region} for region in sorted(df_global['region'].unique())],
                    value='all',
                    multi=False,
                    style={'minWidth': '250px'}
                )
            ], style={'flex': '1', 'marginRight': '20px'}),

            html.Div([
                html.Label("Year:", style={'fontWeight': 'bold', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    id='year-filter',
                    options=[{'label': 'All years', 'value': 'all'}] +
                            [{'label': str(year), 'value': year} for year in sorted(df_global['year'].unique())],
                    value='all',
                    multi=False,
                    style={'minWidth': '150px'}
                )
            ], style={'flex': '1'})
        ], style={'display': 'flex', 'alignItems': 'flex-end', 'flexWrap': 'wrap'})
    ], style=CARD_STYLE),

    # KPIs
    html.Div([
        html.H3("📊 Performance Metrics", style={'marginBottom': '20px', 'color': COLORS['text']}),
        html.Div(id='kpi-cards', style={'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'})
    ], style=CARD_STYLE),

    # Scatter Real vs Predicho
    html.Div([
        html.H3("📈 Predicted vs Actual Values",
                style={'marginBottom': '20px', 'color': COLORS['text']}),
        dcc.Graph(id='scatter-predicted-actual')
    ], style=CARD_STYLE),

    # Distribución de Errores
    html.Div([
        html.H3("📉 Prediction Error Distribution",
                style={'marginBottom': '20px', 'color': COLORS['text']}),
        dcc.Graph(id='error-distribution')
    ], style=CARD_STYLE),

    # Comparación y Top errores
    html.Div([
        html.Div([
            html.H3("⚖️ Train vs Test Comparison",
                    style={'marginBottom': '20px', 'color': COLORS['text']}),
            dcc.Graph(id='train-test-comparison')
        ], style={'flex': '1', 'marginRight': '10px'}),

        html.Div([
            html.H3("🔝 Top 10 Largest Errors",
                    style={'marginBottom': '20px', 'color': COLORS['text']}),
            dcc.Graph(id='top-errors')
        ], style={'flex': '1', 'marginLeft': '10px'})
    ], style={**CARD_STYLE, 'display': 'flex', 'gap': '20px', 'flexWrap': 'wrap'}),

    # Rendimiento por Región
    html.Div([
        html.H3("🌎 Performance by Region",
                style={'marginBottom': '20px', 'color': COLORS['text']}),
        dcc.Graph(id='regional-performance')
    ], style=CARD_STYLE),

    # Mapa geográfico
    html.Div([
        html.H3("🗺️ Performance Map by Country (MAE per country)",
                style={'marginBottom': '20px', 'color': COLORS['text']}),
        dcc.Graph(id='map-performance')
    ], style=CARD_STYLE),

    # Evolución temporal
    html.Div([
        html.H3("📅 Temporal Evolution (2015-2019)",
                style={'marginBottom': '20px', 'color': COLORS['text']}),
        dcc.Graph(id='temporal-evolution')
    ], style=CARD_STYLE),

    # Insights
    html.Div([
        html.H3("🧠 Automatic Insights",
                style={'marginBottom': '12px', 'color': COLORS['text']}),
        html.Div(id='insights-block', style={
            'backgroundColor': '#fcfcfd',
            'border': f'1px solid {COLORS["border"]}',
            'borderRadius': '10px',
            'padding': '16px',
            'lineHeight': '1.6',
            'color': COLORS['text']
        })
    ], style=CARD_STYLE),

    # Footer
    html.Div([
        html.P("Dashboard created for ETL Workshop 3 | Data: World Happiness Report 2015-2019",
               style={'textAlign': 'center', 'color': '#6c757d', 'margin': '0'})
    ], style={'padding': '20px', 'marginTop': '30px'})

], style={
    'fontFamily': 'Arial, sans-serif',
    'padding': '30px',
    'backgroundColor': COLORS['background'],
    'minHeight': '100vh'
})

# ============================================================================
# CALLBACK
# ============================================================================

@app.callback(
    [Output('kpi-cards', 'children'),
     Output('scatter-predicted-actual', 'figure'),
     Output('error-distribution', 'figure'),
     Output('train-test-comparison', 'figure'),
     Output('top-errors', 'figure'),
     Output('regional-performance', 'figure'),
     Output('map-performance', 'figure'),
     Output('temporal-evolution', 'figure'),
     Output('insights-block', 'children')],
    [Input('dataset-filter', 'value'),
     Input('region-filter', 'value'),
     Input('year-filter', 'value')]
)
def update_dashboard(dataset, region, year):
    # Aplicar filtros
    df = df_global.copy()

    if dataset != 'all':
        df = df[df['data_split'] == dataset]
    if region != 'all':
        df = df[df['region'] == region]
    if year != 'all':
        df = df[df['year'] == year]

    # Si no hay datos tras los filtros: devolver placeholders
    if _safe_len(df) == 0:
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No data for selected filters",
                                 xref="paper", yref="paper", x=0.5, y=0.5,
                                 showarrow=False, font=dict(size=16))
        empty_fig.update_layout(height=360, template='plotly_white')
        return ([],) + (empty_fig,)*7 + ("No data to generate insights with current filters.",)

    # ================= KPI CARDS =================
    all_m = calculate_metrics(df)
    train_m = calculate_metrics(df, 'train') if 'train' in df['data_split'].values else None
    test_m  = calculate_metrics(df, 'test')  if 'test'  in df['data_split'].values else None

    def card(title, main_value, foot_left=None, foot_right=None):
        return html.Div([
            html.Div(title, style={'fontSize': '14px', 'color': '#6c757d', 'marginBottom': '10px'}),
            html.Div(main_value, style={'fontSize': '36px', 'fontWeight': 'bold', 'color': COLORS['accent']}),
            html.Div([
                html.Span(foot_left or "", style={'fontSize': '12px', 'color': COLORS['train'], 'marginRight': '10px'}),
                html.Span(foot_right or "", style={'fontSize': '12px', 'color': COLORS['test']})
            ], style={'marginTop': '10px'})
        ], style={
            'backgroundColor': COLORS['card'],
            'padding': '20px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'flex': '1', 'minWidth': '220px',
            'textAlign': 'center'
        })

    kpi_cards = [
        card("📝 Total Records",
             f"{all_m['count']}",
             f"Train: {train_m['count'] if train_m else 0}",
             f"Test: {test_m['count'] if test_m else 0}"),

        card("📊 MAE (Mean Absolute Error)",
             _fmt(all_m['mae']),
             f"Train: {_fmt(train_m['mae'])}" if train_m else "Train: N/A",
             f"Test: {_fmt(test_m['mae'])}" if test_m else "Test: N/A"),

        card("📉 RMSE (Root Mean Squared Error)",
             _fmt(all_m['rmse']),
             f"Train: {_fmt(train_m['rmse'])}" if train_m else "Train: N/A",
             f"Test: {_fmt(test_m['rmse'])}" if test_m else "Test: N/A"),

        card("🎯 R²",
             _fmt(all_m['r2']),
             f"Train: {_fmt(train_m['r2'])}" if train_m else "Train: N/A",
             f"Test: {_fmt(test_m['r2'])}" if test_m else "Test: N/A"),
    ]

    # ================= Scatter Real vs Predicho =================
    fig_scatter = go.Figure()
    min_val = float(min(df['actual_happiness_score'].min(), df['predicted_happiness_score'].min()))
    max_val = float(max(df['actual_happiness_score'].max(), df['predicted_happiness_score'].max()))
    fig_scatter.add_trace(go.Scatter(
        x=[min_val, max_val], y=[min_val, max_val],
        mode='lines', name='Perfect Prediction',
        line=dict(color='red', dash='dash', width=2)
    ))
    if dataset == 'all':
        for split, color in [('train', COLORS['train']), ('test', COLORS['test'])]:
            df_split = df[df['data_split'] == split]
            if _safe_len(df_split) > 0:
                fig_scatter.add_trace(go.Scatter(
                    x=df_split['actual_happiness_score'],
                    y=df_split['predicted_happiness_score'],
                    mode='markers', name=f'{split.capitalize()}',
                    marker=dict(size=8, color=color, opacity=0.6),
                    text=df_split['country'],
                    hovertemplate='<b>%{text}</b><br>Actual: %{x:.3f}<br>Predicted: %{y:.3f}<br>Error: %{customdata:.3f}<extra></extra>',
                    customdata=df_split['prediction_error']
                ))
    else:
        color = COLORS['train'] if dataset == 'train' else COLORS['test']
        fig_scatter.add_trace(go.Scatter(
            x=df['actual_happiness_score'], y=df['predicted_happiness_score'],
            mode='markers', name=dataset.capitalize(),
            marker=dict(size=8, color=color, opacity=0.6),
            text=df['country'],
            hovertemplate='<b>%{text}</b><br>Actual: %{x:.3f}<br>Predicted: %{y:.3f}<br>Error: %{customdata:.3f}<extra></extra>',
            customdata=df['prediction_error']
        ))
    fig_scatter.update_layout(
        xaxis_title='Actual Happiness', yaxis_title='Predicted Happiness',
        template='plotly_white', hovermode='closest', height=500,
        showlegend=True, legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)')
    )

    # ================= Histograma de Errores (con línea MAE) =================
    fig_error = go.Figure()
    if dataset == 'all':
        for split, color in [('train', COLORS['train']), ('test', COLORS['test'])]:
            df_split = df[df['data_split'] == split]
            if _safe_len(df_split) > 0:
                fig_error.add_trace(go.Histogram(
                    x=df_split['prediction_error'],
                    name=split.capitalize(),
                    marker_color=color, opacity=0.7, nbinsx=30
                ))
    else:
        color = COLORS['train'] if dataset == 'train' else COLORS['test']
        fig_error.add_trace(go.Histogram(
            x=df['prediction_error'], name=dataset.capitalize(),
            marker_color=color, opacity=0.7, nbinsx=30
        ))
    # Línea vertical en el MAE global del df filtrado
    mae_here = calculate_metrics(df)['mae']
    if mae_here is not None and not np.isnan(mae_here):
        fig_error.add_vline(x=mae_here, line_dash="dot", line_color="red",
                            annotation_text=f"MAE={mae_here:.2f}", annotation_position="top right")
    fig_error.update_layout(
        xaxis_title='Prediction Error (absolute)', yaxis_title='Frequency',
        template='plotly_white', barmode='overlay', height=400, showlegend=True
    )

    # ================= Comparación Train vs Test =================
    comparison_data = []
    if 'train' in df['data_split'].values:
        m = calculate_metrics(df[df['data_split'] == 'train'])
        comparison_data.append({'Dataset': 'Train', 'MAE': m['mae'], 'RMSE': m['rmse'], 'R²': m['r2']})
    if 'test' in df['data_split'].values:
        m = calculate_metrics(df[df['data_split'] == 'test'])
        comparison_data.append({'Dataset': 'Test', 'MAE': m['mae'], 'RMSE': m['rmse'], 'R²': m['r2']})

    if comparison_data:
        df_comparison = pd.DataFrame(comparison_data)
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(
            name='MAE', x=df_comparison['Dataset'], y=df_comparison['MAE'],
            marker_color='lightblue', text=df_comparison['MAE'].round(4), textposition='auto'
        ))
        fig_comparison.add_trace(go.Bar(
            name='RMSE', x=df_comparison['Dataset'], y=df_comparison['RMSE'],
            marker_color='lightcoral', text=df_comparison['RMSE'].round(4), textposition='auto'
        ))
        fig_comparison.update_layout(
            yaxis_title='Metric Value', template='plotly_white',
            barmode='group', height=400, showlegend=True
        )
    else:
        fig_comparison = go.Figure()
        fig_comparison.add_annotation(
            text="Not enough data to compare",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=16)
        )
        fig_comparison.update_layout(height=400, template='plotly_white')

    # ================= Top 10 errores =================
    df_top_errors = df.nlargest(10, 'prediction_error')[['country', 'year', 'prediction_error', 'data_split']].copy()
    colors_top = [COLORS['train'] if s == 'train' else COLORS['test'] for s in df_top_errors['data_split']]
    fig_top_errors = go.Figure(go.Bar(
        x=df_top_errors['prediction_error'],
        y=df_top_errors['country'] + ' (' + df_top_errors['year'].astype(str) + ')',
        orientation='h', marker_color=colors_top,
        text=df_top_errors['prediction_error'].round(3), textposition='auto',
        hovertemplate='<b>%{y}</b><br>Error: %{x:.3f}<extra></extra>'
    ))
    fig_top_errors.update_layout(
        xaxis_title='Prediction Error', yaxis_title='',
        template='plotly_white', height=400, yaxis={'categoryorder': 'total ascending'}
    )

    # ================= Rendimiento por Región (clamp R²>=0) =================
    regional_metrics = []
    for region_name in df['region'].unique():
        df_region = df[df['region'] == region_name]
        m = calculate_metrics(df_region)
        r2_clamped = max(0.0, 0.0 if (m['r2'] is None or np.isnan(m['r2'])) else float(m['r2']))
        regional_metrics.append({
            'Region': region_name,
            'MAE': m['mae'],
            'RMSE': m['rmse'],
            'R²': r2_clamped,
            'Records': m['count']
        })
    df_regional = pd.DataFrame(regional_metrics).sort_values('MAE')
    fig_regional = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Error by Region (MAE)', 'R² by Region'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    fig_regional.add_trace(
        go.Bar(x=df_regional['MAE'], y=df_regional['Region'], orientation='h',
               marker_color=COLORS['accent'], text=df_regional['MAE'].round(3),
               textposition='auto', showlegend=False),
        row=1, col=1
    )
    fig_regional.add_trace(
        go.Bar(x=df_regional['R²'], y=df_regional['Region'], orientation='h',
               marker_color=COLORS['all'], text=df_regional['R²'].round(3),
               textposition='auto', showlegend=False),
        row=1, col=2
    )
    fig_regional.update_xaxes(title_text="MAE", row=1, col=1)
    fig_regional.update_xaxes(title_text="R²", row=1, col=2)
    fig_regional.update_yaxes(categoryorder='total ascending', row=1, col=1)
    fig_regional.update_yaxes(categoryorder='total descending', row=1, col=2)
    fig_regional.update_layout(template='plotly_white', height=500, showlegend=False)

    # ================= Mapa geográfico (error medio por país) =================
    # Agrupamos por país (opcionalmente podrías agrupar por país+año)
    df_country = (df.groupby('country', as_index=False)
                    .agg(mae=('prediction_error', 'mean'),
                         actual_mean=('actual_happiness_score', 'mean'),
                         pred_mean=('predicted_happiness_score', 'mean'),
                         count=('prediction_error', 'size')))
    fig_map = px.choropleth(
        df_country, locations='country', locationmode='country names',
        color='mae', color_continuous_scale='Reds',
        hover_name='country',
        hover_data={'mae': ':.3f', 'actual_mean': ':.3f', 'pred_mean': ':.3f', 'count': True},
        labels={'mae': 'MAE'}
    )
    fig_map.update_layout(
        template='plotly_white', height=520,
        coloraxis_colorbar=dict(title="MAE"),
        margin=dict(l=30, r=30, t=20, b=20)
    )

    # ================= Evolución temporal =================
    temporal_metrics = []
    for year_val in sorted(df['year'].unique()):
        df_year = df[df['year'] == year_val]
        m_all = calculate_metrics(df_year)
        temporal_metrics.append({
            'Year': year_val, 'Dataset': 'All',
            'MAE': m_all['mae'],
            'Actual Average': df_year['actual_happiness_score'].mean(),
            'Predicted Average': df_year['predicted_happiness_score'].mean()
        })
        for split in ['train', 'test']:
            df_split = df_year[df_year['data_split'] == split]
            if _safe_len(df_split) > 0:
                m_split = calculate_metrics(df_split)
                temporal_metrics.append({
                    'Year': year_val, 'Dataset': split.capitalize(),
                    'MAE': m_split['mae'],
                    'Actual Average': df_split['actual_happiness_score'].mean(),
                    'Predicted Average': df_split['predicted_happiness_score'].mean()
                })
    df_temporal = pd.DataFrame(temporal_metrics)

    fig_temporal = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Error Evolution (MAE)', 'Happiness Averages Evolution'),
        vertical_spacing=0.15,
        specs=[[{"type": "scatter"}], [{"type": "scatter"}]]
    )
    for dataset_name in df_temporal['Dataset'].unique():
        df_dataset = df_temporal[df_temporal['Dataset'] == dataset_name]
        color = COLORS['all'] if dataset_name == 'All' else (COLORS['train'] if dataset_name == 'Train' else COLORS['test'])
        fig_temporal.add_trace(
            go.Scatter(x=df_dataset['Year'], y=df_dataset['MAE'],
                       mode='lines+markers', name=f'{dataset_name} - MAE',
                       line=dict(color=color, width=2), marker=dict(size=8)),
            row=1, col=1
        )
    df_all_temporal = df_temporal[df_temporal['Dataset'] == 'All']
    fig_temporal.add_trace(
        go.Scatter(x=df_all_temporal['Year'], y=df_all_temporal['Actual Average'],
                   mode='lines+markers', name='Actual Average',
                   line=dict(color='green', width=2), marker=dict(size=8)),
        row=2, col=1
    )
    fig_temporal.add_trace(
        go.Scatter(x=df_all_temporal['Year'], y=df_all_temporal['Predicted Average'],
                   mode='lines+markers', name='Predicted Average',
                   line=dict(color='orange', width=2, dash='dash'), marker=dict(size=8)),
        row=2, col=1
    )
    fig_temporal.update_xaxes(title_text="Year", row=2, col=1)
    fig_temporal.update_yaxes(title_text="MAE", row=1, col=1)
    fig_temporal.update_yaxes(title_text="Average Happiness", row=2, col=1)
    fig_temporal.update_layout(
        template='plotly_white', height=700, showlegend=True,
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)')
    )

    # ================= Insights automáticos =================
    # Top región con menor MAE y con mayor MAE
    region_stats = df.groupby('region', as_index=False)['prediction_error'].mean().rename(columns={'prediction_error':'mae'})
    best_region = region_stats.nsmallest(1, 'mae') if _safe_len(region_stats)>0 else None
    worst_region = region_stats.nlargest(1, 'mae')  if _safe_len(region_stats)>0 else None

    insight_lines = [
        f"Global R²: {_fmt(all_m['r2'])} | Global MAE: {_fmt(all_m['mae'])} | Global RMSE: {_fmt(all_m['rmse'])}.",
        f"Records: {all_m['count']} (Train: {train_m['count'] if train_m else 0} | Test: {test_m['count'] if test_m else 0})."
    ]
    if best_region is not None and worst_region is not None and _safe_len(best_region)>0 and _safe_len(worst_region)>0:
        insight_lines.append(
            f"Best fit by region: {best_region.iloc[0]['region']} (MAE≈{_fmt(best_region.iloc[0]['mae'],3)}). "
            f"Highest error by region: {worst_region.iloc[0]['region']} (MAE≈{_fmt(worst_region.iloc[0]['mae'],3)})."
        )
    if not (all_m['mbe'] is None or np.isnan(all_m['mbe'])):
        if all_m['mbe'] > 0.02:
            insight_lines.append("The model tends to **overpredict** slightly (positive MBE).")
        elif all_m['mbe'] < -0.02:
            insight_lines.append("The model tends to **underpredict** slightly (negative MBE).")

    insights_block = html.Ul([html.Li(line) for line in insight_lines])

    return (kpi_cards, fig_scatter, fig_error, fig_comparison, fig_top_errors,
            fig_regional, fig_map, fig_temporal, insights_block)

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("🌍 HAPPINESS PREDICTION ANALYSIS DASHBOARD")
    print("=" * 70)
    print(f"📊 Total records loaded: {len(df_global)}")
    print(f"📅 Available years: {sorted(df_global['year'].unique())}")
    print(f"🌎 Available regions: {df_global['region'].nunique()}")
    print(f"🏳️ Unique countries: {df_global['country'].nunique()}")
    print("=" * 70)
    print("🚀 Starting dashboard server...")
    print("🌐 Access the dashboard at: http://127.0.0.1:8050")
    print("=" * 70)
    app.run_server(debug=True, port=8050)
