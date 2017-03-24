# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
"""
 使用jinja2模板 生成 html 表格

"""
from jinja2 import Template

def get_html_table(tables):

    def header_to_html(header):
        """
        将表格的表头 转换成html
        :param header:
        :return:
        """
        th_style = u"min-width:80px;border: 1px solid #aaa;padding: 5px 10px;text-align: center;color: #001f3f;background-color: #7FDBFF; font-weight: bold;"

        def calc_rowspan(depth, header):
            cur_max_depth = depth
            for cell in header:
                if isinstance(cell, dict):
                    if len(cell) != 1:
                        raise Exception(u" dict size in header can only be 1 ")

                    cur_max_depth = max(cur_max_depth, calc_rowspan(depth + 1, cell.values()[0]))
                elif isinstance(cell, basestring):
                    pass
                else:
                    raise Exception(u"header can only contains basestring and dict ")
            return cur_max_depth

        def calc_colspan(size, header):
            for cell in header:
                if isinstance(cell, dict):
                    size += calc_colspan(0, cell.values()[0])
                else:
                    size += 1
            return size

        def html_header(max_depth, depth, header, html_rows):

            for cell in header:
                if isinstance(cell, dict):

                    html_rows.append([])

                    key = cell.keys()[0]
                    vals = cell[key]

                    html_rows[depth].append(
                        u'<td colspan="{c}" style="{style}">{v}</td>'.format(c=calc_colspan(0, vals), v=key,
                                                                             style=th_style))

                    html_header(max_depth, depth + 1, vals, html_rows)
                else:
                    if depth + 1 == max_depth:
                        html_rows[depth].append(u'<th style="{style}">{v}</th> '.format(v=cell, style=th_style))
                    else:
                        html_rows[depth].append(
                            u'<th rowspan="{r}" style="{style}">{v}</th> '.format(r=max_depth - depth, v=cell,
                                                                                  style=th_style))

        max_depth = calc_rowspan(0, header)

        html_rows = [[]]
        html_header(max_depth + 1, 0, header, html_rows)

        html = u''
        for cell in html_rows:
            html += u'<tr>{v}</tr>\n'.format(v=u''.join(cell))
        return html

    def regulate_table_params():
        """
        对表格参数进行规范化处理, 以更方便生成 html
        :param kwargs:
        :return:
        """
        for tab in tables:
            if u'title' not in tab: raise Exception(u'table must have a title ')
            if u'header' not in tab : raise Exception(u'table must have its header ')
            if u'data_list' not in tab: raise Exception(u'table must have data ')

            tab[u'col_num'] = len(tab[u'data_list'][0])
            tab.setdefault(u'desc', u'')
            tab.setdefault(u'wrap', lambda x, y: y) # x 代表 下标, y 代表 取值

            # header 支持多层, 每层的header可以 合并列, 得到更 简洁/美观 的表头
            header = tab[u'header']

            tab[u'header'] = header_to_html(header)


    html_template = u"""
        <table style=" border: 1px solid #aaa;border-collapse: collapse;" >
          {%for tab in tables%}
            <tr style="height:45px;">
              <td colspan={{tab.col_num}}  style="font-size:24px; color:#a0a0a0; border: 1px solid #aaa;border-collapse: collapse; ">{{tab.title}} </td>
            <tr>
            {{tab.header}}
            {% for row in tab.data_list %}
            <tr>
                {% for each in row %}
                    <td  style="border: 1px solid #aaa;padding: 5px 5px;text-align: right;">
                      {{ tab.wrap(loop.index, each) }}
                    </td>
                {% endfor %}
            </tr>
            {% endfor %}
            <tr> <td colspan={{tab.col_num}}><div> {{ tab.desc }}</div></td> </tr>
          {%endfor%}
        </table>

    """

    regulate_table_params()

    template = Template(html_template)
    return template.render({'tables': tables})


if __name__ == '__main__':

    class DEMO:
        u"""
           使用 webpy 搭建的一个简单的web服务, 来查看显示结果
        """
        def GET(self):
            web.header('Content-Type', 'text/html; charset=UTF-8')

            tables = [
                {
                  # 表格标题
                  u'title': u'表格1',
                  # 表头
                  u'header': [u'时间', u'指标2', u'指标3', u'指标4', u'指标5'],
                  # 数据项
                  u'data_list': [[u'2017-03-22', 2, 3, 4, 5], [u'2017-03-21', 5, 6, 4, 5]],
                    
                  u'desc': u'补充说明',
                    
                  # x 下标 y 数值, 根据下标 和 数值 对数据的显示重新包装, 实现 高亮 等功能
                  u'wrap': lambda x, y: "<font color='red'>{0}</font>".format(y) if x == 2 else y,
                },
                {
                    # 表格标题
                    u'title': u'表格2',
                    # 表头
                    u'header': [u'指标1', u'指标2', u'指标3', {u'公共头': [u'指标4', u'指标5']}],
                    # 数据项
                    u'data_list': [[u'2017-03-22', 2, 3, 4, 5], [u'2017-03-21', -5, 6, 4, 5]],

                    u'desc': u'补充说明',

                    # x 下标 y 数值, 根据下标 和 数值 对数据的显示重新包装, 实现 高亮 等功能
                    u'wrap': lambda x, y: "<font color='{c}'>{v}</font>".format(c='red' if y > 0 else 'green', v=y) if x == 2 else y,
                }
            ]
            
            html = get_html_table(tables=tables)
            return html


    import web
    reload(sys)
    sys.setdefaultencoding('utf-8')
    web.config.debug = False

    app = web.application(('/', 'DEMO'), globals())
    app.run()