# import seaborn as sns
# import matplotlib_inline.backend_inline
import matplotlib.pyplot as plt
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from skimage import io
import streamlit as st

def BoW_eda(df, n=30, text_column='caption', drop=['<number>'], context='paper', title_suffix=None,
    filename=None, path=r'C:\Users\silvh\OneDrive\data science job search\content'):
    sns.reset_defaults()    
    # %matplotlib inline
    # matplotlib_inline.backend_inline.set_matplotlib_formats('retina')
    plt.rcParams['savefig.dpi'] = 300
    
    # sns.set_theme(context=context, style='ticks')
    df = df.drop(columns=drop)
    top_n = df.sum().sort_values(ascending=False).head(n).sort_values()
    # ax = sns.barplot(df[top_n.index.tolist()], estimator='sum',errorbar=None) # this works but gives deprecated warning
    fig, ax = plt.subplots()
    ax.barh(top_n.index, top_n)
    ax.set_yticks(top_n.index) # This line suppresses the warning "UserWarning: FixedFormatter should only be used together with FixedLocator"
    title = f'Top {n} words in Instagram posts'
    if title_suffix:
        title = f'{title}: {title_suffix}'
    ax.set(xlabel='Count', ylabel='Word', title=title)
    ax.axis('tight')
    if filename:
        try:
            path = f'{path}/'.replace('\\','/')
            fig.savefig(path+filename, bbox_inches='tight')
            print('Saved: ', path+filename)
        except:
            print('Unable to save outputs')
    print('Time completed:', datetime.now())

    return top_n

@st.cache_data
def plot_images(df, n=6, top=True, max_columns=5, streamlit=False):
    """
    Plot the images/video thumbnails of either the top or 
    worst performing instagram media (posts, reels, carousels).
    """
    ncols = n if n<max_columns else max_columns
    nrows = (n + ncols - 1) // ncols
    sort_by = ['like_count']
    posts = df.sort_values(by=sort_by, ascending=False if top else True).head(n)
    posts['thumbnail_url'].fillna(posts['media_url'], inplace=True)
    fig = make_subplots(rows=nrows, cols=ncols)
    for index, url in enumerate(posts['thumbnail_url']):
        # print(index,':', url)
        fig.add_layout_image(
            x=0, y=0,
            xanchor='center', yanchor='middle',
            sizex=1, sizey=1,
            row=index // ncols + 1,
            col=index % ncols + 1,
            xref="x",
            yref="y",
            opacity=1.0,
            source=url
        )
    fig.update_xaxes(range=[-0.5,0.5], showticklabels=False)
    fig.update_yaxes(range=[-0.5,0.5], showticklabels=False)
    fig.update_layout(plot_bgcolor="white")
    if streamlit:
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig.show()
    return posts