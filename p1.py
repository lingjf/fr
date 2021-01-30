from pyecharts import options as opts
from pyecharts.charts import Line, Pie, Grid, Timeline

import json
import utils
import dao
M, Z, D = dao.get()

utils.DrawLine(M, list(map(lambda a: {
                            "公布M2": a[0]["M2"],
                            "计算m2": a[1]["货币发行"] - a[2]["库存现金"] + a[2]["单位活期存款"] + a[2]["单位定期存款"] + a[2]["个人存款"] + a[2]["计入广义货币的存款"],
                            "公布M1": a[0]["M1"],
                            "计算m1": a[1]["货币发行"] - a[2]["库存现金"] + a[2]["单位活期存款"],
                            "公布M0": a[0]["M0"],
                            "计算m0": a[1]["货币发行"] - a[2]["库存现金"],
                            "计算'm0": a[3]["流通中货币"],
                        }, Z)),
    "货币供应量"
)
