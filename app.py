# --- ライブラリのインポート ---
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# --- データの準備 (Pandas) ---
# Plotlyに組み込まれているGapminderデータセットを読み込みます。
# このデータには、世界の国々の年代ごとの平均寿命、人口、一人当たりGDPなどが含まれています。
df = px.data.gapminder()

# --- Dashアプリケーションのインスタンスを作成 ---
app = Dash(__name__)

# --- アプリケーションのレイアウトを定義 ---
# ここでアプリの見た目をHTMLのように組み立てます。
app.layout = html.Div([
    # アプリケーションのメインタイトル
    html.H1(
        children='Gapminderデータ：経済力と平均寿命の関係',
        style={'textAlign': 'center', 'fontFamily': 'sans-serif'}
    ),

    # グラフを表示するためのコンポーネント
    # id='graph-with-slider' という名前をつけ、後から操作できるようにします。
    dcc.Graph(id='graph-with-slider'),

    # 年を選択するためのスライダー
    # id='year-slider' という名前をつけ、ユーザーの操作を受け取ります。
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])

# --- コールバックを定義 (インタラクティブ性の核) ---
# 「スライダーが動いたら、グラフを更新する」というルールを定義します。
@app.callback(
    Output('graph-with-slider', 'figure'), # 出力先
    Input('year-slider', 'value')         # 入力元
)
def update_figure(selected_year):
    # スライダーで選ばれた年でデータを絞り込みます。
    filtered_df = df[df.year == selected_year]
    
    # 絞り込んだデータで、Plotlyのグラフを再作成します。
    fig = px.scatter(
        filtered_df,
        x="gdpPercap", y="lifeExp",
        size="pop", color="continent", hover_name="country",
        log_x=True, size_max=60,
        range_x=[100, 100000], range_y=[25, 90]
    )
    
    # グラフの見た目を少し調整します。
    fig.update_layout(transition_duration=500, title_text=f'{selected_year}年の状況')
    
    # 作成したグラフを返すと、画面上のグラフが更新されます。
    return fig
  # サーバーが参照するための変数を定義
server = app.server

# Colab用の起動コードは削除、またはコメントアウトします
# if __name__ == '__main__':
#     app.run(jupyter_mode='inline')
