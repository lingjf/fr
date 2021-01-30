from pyecharts import options as opts
from pyecharts.charts import Line, Pie, Grid, Timeline
from pyecharts.commons.utils import JsCode


def deunit(Values):
    types = Values[-1].keys()
    s = 10000
    for t in types:
        for v in Values:
            if v[t] > 0:
                s = min(s, v[t])
    u = 1
    if s > 1000:
        u = 10000
    return 10000

def DrawLine(Months, Values, Title, Html=None):
    line = Line({"width": "100%", "height": "720px"})
    line.add_xaxis(xaxis_data=Months)
    u = deunit(Values)
    types = Values[-1].keys()
    for t in types:
        line.add_yaxis(series_name=t,
                       y_axis=list(map(lambda a: max(0, a[t])/u, Values)),
                       symbol_size=0,
                       label_opts=opts.LabelOpts(is_show=False))
    line.set_global_opts(
            xaxis_opts=opts.AxisOpts(name="月份", 
                                    axislabel_opts=opts.LabelOpts(rotate=-15),
                                    axistick_opts=opts.AxisTickOpts(is_align_with_label=True),),
            yaxis_opts=opts.AxisOpts(name="亿" if u == 1 else "万亿", 
                                    splitline_opts=opts.SplitLineOpts(is_show=True),
                                    axistick_opts=opts.AxisTickOpts(is_show=True)),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            title_opts=opts.TitleOpts(title=Title, subtitle=""),
            legend_opts=opts.LegendOpts(pos_left="left", orient="vertical", padding=180),
        )

    line.render(Html if Html else Title + '.html')

def genLine(Months, Values, Title, i):
    line = Line()
    line.add_xaxis(xaxis_data=Months)
    u = deunit(Values)
    types = Values[-1].keys()
    for t in types:
        line.add_yaxis(series_name=t,y_axis=list(map(lambda a: max(0, a[t])/u, Values)),label_opts=opts.LabelOpts(is_show=False),symbol_size=0,)
    x = [
        opts.LegendOpts(pos_left="0px", orient="vertical"),
        opts.LegendOpts(pos_left="90%", orient="vertical"),
    ]
    line.set_global_opts(xaxis_opts=opts.AxisOpts(name="月份", 
                                                  axislabel_opts=opts.LabelOpts(rotate=-15),
                                                  axistick_opts=opts.AxisTickOpts(is_align_with_label=True),),
                         yaxis_opts=opts.AxisOpts(name="亿" if u == 1 else "万亿", 
                                                  splitline_opts=opts.SplitLineOpts(is_show=True),
                                                  axistick_opts=opts.AxisTickOpts(is_show=True)),
                         tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                         title_opts=opts.TitleOpts(title=Title, subtitle="", pos_left="center"),
                         legend_opts=x[i],
        )
    return line

def genLines(Months, Valuess, Title) -> Grid:
    grid = Grid(init_opts=opts.InitOpts(width="100%", height="600px"))
    lines = []
    for i, Values in enumerate(Valuess):
        lines.append(genLine(Months, Values, Title, i))
    grid.add(lines[0],grid_opts=opts.GridOpts(pos_right="54%"))
    grid.add(lines[1],grid_opts=opts.GridOpts(pos_left="54%"))
    return grid


def genPie(Month, Values, Title) -> Pie:
    pie = Pie()
    n = len(Values)
    r = [
        [],
        [0, "70%"],
        [0, "50%"],
        [0, "30%"],
        [0, "30%"],
    ]
    x = [
        [], # 0
        [["50%", "50%"]], # 1
        [["25%", "50%"], ["75%", "50%"]], # 2
        [["25%", "25%"], ["75%", "25%"], ["25%", "75%"]], # 3
        [["25%", "25%"], ["75%", "25%"], ["25%", "75%"], ["75%", "75%"]], # 4
    ]
    for i, Value in enumerate(Values):
        pie.add(
            "",
            [[k,v] for k,v in Value.items()],
            radius=r[n],
            center=x[n][i],
        )
    pie.set_global_opts(title_opts=opts.TitleOpts(subtitle=Title, title=Month, pos_bottom=0))
    fn = " function(params) { return params.name + ': ' + Math.round(params.value/10)/1000 + '万亿'; } "
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"),
                        tooltip_opts=opts.TooltipOpts(trigger="item", formatter=JsCode(fn))
                       )
    return pie

def genPies(Months, Valuess, Title) -> Timeline:
    timeline = Timeline({"width": "100%", "height": "720px"})
    for i in range(0, len(Months), 1):
        Values = []
        for a in Valuess:
            Values.append(a[i])
        pie = genPie(Months[i], Values, Title)
        timeline.add(pie, Months[i])

    timeline.add_schema(
        is_auto_play = True,
        is_loop_play = False,
        play_interval = 900,
        # axis_type = "time",
        # orient = "vertical", #"horizontal",
        symbol = 'rect',
        symbol_size = 2,
        linestyle_opts = opts.LineStyleOpts(width=1, color='rgb(255,0,0,0.5)'),
        checkpointstyle_opts = opts.TimelineCheckPointerStyle(symbol_size=8, border_width=2),
        # label_opts = opts.LabelOpts(interval=12)
    )
    return timeline


if __name__ == '__main__':
    a = genPie("2001-01", [{"M0":1, "M1": 2}], "hello")
    a = genPie("2001-01", [{"M0":1, "M1": 2}, {"M2":2, "M3": 2}], "hello")
    a = genPie("2001-01", [{"M0":1, "M1": 2}, {"M2":2, "M3": 2}, {"M4":3, "M5": 5}], "hello")
    a = genPie("2001-01", [{"M0":1, "M1": 2}, {"M2":2, "M3": 2}, {"M4":3, "M5": 5}, {"M6":3, "M7": 5}], "hello")
    a.render('c.html')