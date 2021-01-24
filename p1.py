from pyecharts import options as opts
from pyecharts.charts import Line, Pie, Grid, Timeline

import json

with open('mmm.json', 'r') as f:
    mmm = json.load(f)
with open('balance1.json', 'r') as f:
    balance1 = json.load(f)
with open('balance2.json', 'r') as f:
    balance2 = json.load(f)

M = list(filter(lambda a: a["月份"] > '2006-00', mmm))
B1 = list(filter(lambda a: a["月份"] > '2006-00', balance1))
B2 = list(filter(lambda a: a["月份"] > '2006-00', balance2))

def DrawLine(Months, Values):
    line = Line({"width": "1200px", "height": "720px"})
    line.add_xaxis(xaxis_data=Months)
    for v in Values:
        line.add_yaxis(series_name=v,y_axis=Values[v],label_opts=opts.LabelOpts(is_show=False))
    line.set_global_opts(
            xaxis_opts=opts.AxisOpts(name="月份", 
                                    axislabel_opts=opts.LabelOpts(rotate=-15),
                                    axistick_opts=opts.AxisTickOpts(is_align_with_label=True),),
            yaxis_opts=opts.AxisOpts(name="万亿", 
                                    splitline_opts=opts.SplitLineOpts(is_show=True),
                                    axistick_opts=opts.AxisTickOpts(is_show=True)),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            title_opts=opts.TitleOpts(title="货币供应量", subtitle=""),
            legend_opts=opts.LegendOpts(pos_left="left", orient="vertical", padding=180),
        )

    line.render('货币供应量.html')

Months = list(map(lambda a: a["月份"], M))
M0 = list(map(lambda a: a["M0"], M))
M1 = list(map(lambda a: a["M1"], M))
M2 = list(map(lambda a: a["M2"], M))

Z = list(zip(M, B1, B2))

m0 = list(map(lambda a: a[1]["货币发行"] - a[2]["库存现金"], Z))
m1 = list(map(lambda a: a[1]["货币发行"] - a[2]["库存现金"]
                        + a[2]["单位活期存款"], Z))
m2 = list(map(lambda a: a[1]["货币发行"] - a[2]["库存现金"]
                        + a[2]["单位活期存款"]
                        + a[2]["单位定期存款"] + a[2]["个人存款"] + a[2]["计入广义货币的存款"], Z))

DrawLine(Months, {
        "公布M2": [a/10000 for a in M2], "计算m2": [a/10000 for a in m2],
        "公布M1": [a/10000 for a in M1], "计算m1": [a/10000 for a in m1],
        "公布M0": [a/10000 for a in M0], "计算m0": [a/10000 for a in m0],
    }
)
