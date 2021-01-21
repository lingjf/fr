
import json
from matplotlib import pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Line, Pie, Grid, Timeline


with open('mmm.json', 'r') as f:
    mmm = json.load(f)

month = list(map(lambda a: a["月份"], mmm))
m0 = list(map(lambda a: a["M0"]/10000, mmm))
m1 = list(map(lambda a: a["M1"]/10000, mmm))
m2 = list(map(lambda a: a["M2"]/10000, mmm))

def old():
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False

    plt.title('货币供应量')
    plt.Figure(figsize=(8, 4))
    plt.plot(month,m0,label='M0')
    plt.plot(month,m1,label='M1')
    plt.plot(month,m2,label='M2')

    plt.legend(loc='upper left')
    plt.xlabel('月份')
    plt.ylabel('万亿元')

    # plt.gca().yaxis.tick_right()
    # plt.gca().yaxis.set_label_position("right")
    plt.gca().yaxis.get_major_formatter().set_scientific(False)
    plt.gca().yaxis.get_major_formatter().set_useOffset(False)
    plt.gca().xaxis.set_major_locator(plt.LinearLocator(numticks=10))
    plt.show()


line = Line()
line.add_xaxis(xaxis_data=month)
line.add_yaxis(series_name="M0",y_axis=m0,label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5),)
line.add_yaxis(series_name="M1",y_axis=m1,label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5),)
line.add_yaxis(series_name="M2",y_axis=m2,label_opts=opts.LabelOpts(is_show=False),areastyle_opts=opts.AreaStyleOpts(opacity=0.5),)
line.set_global_opts(
        xaxis_opts=opts.AxisOpts(name="月份", 
                                 axislabel_opts=opts.LabelOpts(rotate=-15),
                                 axistick_opts=opts.AxisTickOpts(is_align_with_label=True),),
        yaxis_opts=opts.AxisOpts(name="万亿", 
                                 splitline_opts=opts.SplitLineOpts(is_show=True),
                                 axistick_opts=opts.AxisTickOpts(is_show=True)),
        tooltip_opts=opts.TooltipOpts(trigger="none", axis_pointer_type="cross"),
        title_opts=opts.TitleOpts(title="货币供应量", subtitle=""),
    )

line.render('货币供应量.html')
