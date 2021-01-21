from pyecharts import options as opts
from pyecharts.charts import Line, Pie, Grid, Timeline

import json

with open('balance1.json', 'r') as f:
    balance1 = json.load(f)
with open('balance2.json', 'r') as f:
    balance2 = json.load(f)

B1 = list(filter(lambda a: a["月份"] > '2010-00', balance1))
B2 = list(filter(lambda a: a["月份"] > '2010-00', balance2))

def DrawPie(B, T, name):
    timeline = Timeline()
    for i in range(0, len(B), 1):
        pie = Pie()
        pie.add('', list(map(lambda a: [a, B[i][a] if a in B[i] else 0], T)))
        pie.set_global_opts(title_opts=opts.TitleOpts(title=name + ' ' +B[i]["月份"]),
                            legend_opts=opts.LegendOpts(is_show=False) )
        pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    
        # grid = Grid(init_opts=opts.InitOpts(width="1200px", height="420px"))
        # grid.add(pie1, grid_opts=opts.GridOpts(pos_left="58%"))
        # grid.add(pie2, grid_opts=opts.GridOpts(pos_right="58%"))
        timeline.add(pie, B[i]["月份"])

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
    timeline.render(name + '.html')

def DrawLine(B, T, name):
    line = Line({"width": "1200px", "height": "720px"})
    line.add_xaxis(xaxis_data=list(map(lambda b: b["月份"], B)))
    for t in T:
        line.add_yaxis(series_name=t,y_axis=list(map(lambda b: b[t] if t in b else 0, B)),label_opts=opts.LabelOpts(is_show=False))
    line.set_global_opts(
            xaxis_opts=opts.AxisOpts(name="月份", 
                                    axislabel_opts=opts.LabelOpts(rotate=-15),
                                    axistick_opts=opts.AxisTickOpts(is_align_with_label=True),),
            yaxis_opts=opts.AxisOpts(name="亿", 
                                    splitline_opts=opts.SplitLineOpts(is_show=True),
                                    axistick_opts=opts.AxisTickOpts(is_show=True)),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            title_opts=opts.TitleOpts(title=name, subtitle=""),
            legend_opts=opts.LegendOpts(pos_left="left", orient="vertical", padding=180),
        )

    line.render(name + '.html')

t = ["国外资产", "外汇", "货币黄金", "其他国外资产", "对政府债权", "中央政府", "对其他存款性公司债权", "对其他金融性公司债权", "对非金融性部门债权", "其他资产", "总资产", "储备货币", "货币发行", "金融性公司存款", "其他存款性公司存款", "其他金融性公司存款", "非金融机构存款", "不计入储备货币的金融性公司存款", "发行债券", "国外负债", "政府存款", "自有资金", "其他负债", "总负债"]
DrawLine(B1, t, "货币当局资产负债表")
t = ["国外资产", "对政府债权", "对其他存款性公司债权", "对其他金融性公司债权", "其他资产", "对非金融性部门债权"]
t = ["外汇", "货币黄金", "其他国外资产", "对政府债权", "对其他存款性公司债权", "对其他金融性公司债权", "其他资产", "对非金融性部门债权"]
DrawPie(B1, t, "货币当局资产负债表-资产")
t = ["外汇", "货币黄金", "其他国外资产"]
DrawPie(B1, t, "货币当局资产负债表-资产-国外资产")
t = ["储备货币", "发行债券", "国外负债", "政府存款", "自有资金", "其他负债"]
t = ["货币发行", "其他存款性公司存款", "对其他金融性公司债权", "非金融机构存款", "发行债券", "国外负债", "政府存款", "自有资金", "其他负债"]
DrawPie(B1, t, "货币当局资产负债表-负债")

t = ["国外资产", "储备资产", "准备金存款", "库存现金", "对政府债权", "对中央政府债权", "对中央银行债权", "对其他存款性公司债权", "对其他金融机构债权", "对非金融机构债权", "对其他居民部门债权", "其他资产", "总资产", "对非金融机构及住户负债", "纳入广义货币的存款", "单位活期存款", "单位定期存款", "个人存款", "不纳入广义货币的存款", "可转让存款", "其他存款", "其他负债存款", "对中央银行负债", "对其他存款性公司负债", "对其他金融性公司负债", "计入广义货币的存款", "国外负债", "债券发行", "实收资本", "其他负债", "总负债"]
DrawLine(B2, t, "其他存款性公司资产负债表")
t = ["国外资产", "储备资产", "对政府债权", "对中央银行债权", "对其他存款性公司债权", "对其他金融机构债权", "对非金融机构债权", "对其他居民部门债权", "其他资产"]
DrawPie(B2, t, "其他存款性公司资产负债表-资产")
t = ["准备金存款", "库存现金"]
DrawPie(B2, t, "其他存款性公司资产负债表-资产-储备资产")
t = ["对非金融机构及住户负债", "对中央银行负债", "对其他存款性公司负债", "对其他金融性公司负债", "国外负债", "债券发行", "实收资本", "其他负债"]
DrawPie(B2, t, "其他存款性公司资产负债表-负债")
t = ["单位活期存款", "单位定期存款", "个人存款", "可转让存款", "其他存款", "其他负债存款"]
DrawPie(B2, t, "其他存款性公司资产负债表-负债-存款")
