# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_eda.ipynb (unless otherwise specified).

__all__ = ['setup', 'describe', 'savepath', 'plot']

# Cell

from tqdm import tqdm
import os
from contextlib import redirect_stdout
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

# Cell
#hide

# ローカル変数 --------------------------------------
_save_dir = Path("./output")  # プロットの自動保存ディレクトリ

## ローカル関数 --------------------------------------

pass

# Cell
def setup(sub_dir = "", save_dir = "output"):
    """ライブラリの初期設定をする。
    """
    # --------------  グラフサイズ設定パラメータ  -----------------------
    size_inch, size_px = 15, 2000  #15, 2000が基本。(15,800)も可能（保存したグラフは見切れる）　　colabは、グラフの横幅[px]が画面の横幅[px]を超えると縮小表示、満たないときはそのままグラフ表示する。

    # 横幅（インチ）を指定したときに、指定pxとなるようなDPIを計算。
    # Jupyter表示時はインチ単位指定だが、ファイル保存時はpx単位になるため。
    _h_inch = size_inch * 9/16
    _dpi = int(size_px / size_inch)
    _fontsize = size_inch * 2  # 15インチ・2kpxなら30px, 5インチ・2kpxなら10px　でちょうどよかった。
    # グラフのデフォルト設定。 ↑と同一セルだと初期化がうまくいかなかった。
    sns.set_style(style="whitegrid")
    plt.rcParams.update({
      'font.size' : _fontsize
      ,'figure.figsize' : [size_inch, _h_inch]  #[20.0, 10.0]
      ,'figure.dpi' : _dpi  #300
      ,'savefig.dpi' : _dpi
      ,'figure.titlesize' : 'large'
      ,'legend.fontsize' : 'small'
      ,'axes.labelsize' : 'medium'
      ,'xtick.labelsize' : 'small'
      ,'ytick.labelsize' : 'small'
      })
    global _save_dir
    _save_dir = Path(save_dir)/sub_dir  #).resolve()
    print(f"lileda> 出力フォルダ : '{_save_dir.resolve()}'")

    # matplotlibに日本語フォントのインストール ------------------------------
    # matplotlibの日本語化（参考：https://qiita.com/uehara1414/items/6286590d2e1ffbf68f6c）
    import japanize_matplotlib
    japanize_matplotlib.japanize()
    print(f"lileda> matplotlibに日本語フォント「{plt.rcParams['font.family']}」を設定しました")

# モジュールを読込んだ時に、デフォルト値で初期設定する。printの出力は捨てる。　with redirect_stdout(open(os.devnull, 'w')):
setup()


# Cell
def describe(df):
    """DataFrameの要約（統計量や欠損値の数など）を表示する。
    """
    print("データ形式")
    data = df.head(1).copy()
    data.rename(index={0:"0"}, inplace=True)
    dtype_row = pd.DataFrame(data.dtypes).T
    dtype_row.rename(index={0:"dtype"}, inplace=True)
    data = pd.concat([data, dtype_row])

    display(data)
    def my_describe(_df):
        smry = _df.describe()
        smry.loc["欠損数"] = _df.isna().sum()
        smry.loc["欠損率"] = smry.loc["欠損数"] / df.index.size * 100
        display(smry.round(3))

    if df.select_dtypes('number').columns.size !=0:
        print("要約統計量（数値）")
        my_describe(df.select_dtypes('number'))
    if df.select_dtypes(exclude='number').columns.size !=0:
        print("要約統計量（数値以外）")
        my_describe(df.select_dtypes(exclude='number'))



# Cell
def savepath(filename):
    """保存先の絶対パスを返す。
    """
    _suffix = ""
    if Path(filename).suffix == '' : _suffix = ".png"
    p = _save_dir/f"{filename}{_suffix}"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p.resolve()


# Cell
def plot(ax_grid, tl=None, xl=None, yl=None, xtl=None, savename=None, ld_out=False):
    """matplotlibやseabornのグラフにタイトル・軸ラベルを設定し、フォントサイズ・グラフサイズを調整して、画像ファイルとして保存する。
    """
    fig=None
    if isinstance(ax_grid, plt.Axes):
        # seabornのAxesレベル関数か、pyplotで生成したグラフの場合
        ax = ax_grid
        fig = ax.figure
        if tl is not None : ax.set_title(tl)
        if xl is not None : ax.set_xlabel(xl)
        if yl is not None : ax.set_ylabel(yl)
        if xtl is not None : ax.set(xtickLabels = xtl)
        if ld_out : ax.legend(loc="upper left", bbox_to_anchor=(1,1))  # 凡例をグラフ枠の外側へ配置
    elif isinstance(ax_grid,  (sns.FacetGrid, sns.PairGrid, sns.JointGrid, sns.pairplot, sns.jointplot)):
        # seaborn のfigureレベル関数で生成したグラフの場合
        g = ax_grid
        fig = g.fig
        # g.fig.set_figheight(size_inch);  g.fig.set_figwidth(size_inch)  # figsizeの修正。あとから修正すると余白やタイトル位置が変になるので、面倒だがグラフ生成のたびにheightで指定することにした。
        if tl is not None :
            # タイトルを追加するときは、そのまま追加するとファイル保存したときにタイトルが見切れるので、
            # グラフを縦に90%に縮めてタイトルを設置
            g.fig.subplots_adjust(top=0.9)
            g.fig.suptitle(tl)  #, y=1.02
        ax = g.fig.axes[0] #Gridに対しては、最初のAxesにだけラベル名変更などの操作をする
        if xl is not None : ax.set_xlabel(xl)
        if yl is not None : ax.set_ylabel(yl)
        if xtl is not None : ax.set(xtickLabels = xtl)
        if ld_out : ax.legend(loc="upper left", bbox_to_anchor=(1,1))  # 凡例をグラフ枠の外側へ配置
    # save figure
    p = _save_dir; p.mkdir(parents=True, exist_ok=True)
    if savename is not None : fig.savefig(savepath(savename))
    elif tl is not None : fig.savefig(savepath(tl))