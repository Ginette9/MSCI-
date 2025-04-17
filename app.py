from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from plotly.subplots import make_subplots

app = Flask(__name__)

# 读取 Excel 数据
df = pd.read_excel('MSCI_company_full_data.xlsx')

# 添加评级年份列
df['评级年份'] = pd.to_datetime(df['评级时间']).dt.year

# 定义评级等级的排序顺序
rating_order = ['CCC', 'B', 'BB', 'BBB', 'A', 'AA', 'AAA']

# 定义地区中英文映射
region_mapping = {
    'China': '中国',
    'Hong Kong': '香港',
    'Taiwan': '台湾',
    'United States': '美国',
    'Japan': '日本',
    'South Korea': '韩国',
    'Singapore': '新加坡',
    'India': '印度',
    'Malaysia': '马来西亚',
    'Thailand': '泰国',
    'Indonesia': '印度尼西亚',
    'Philippines': '菲律宾',
    'Vietnam': '越南',
    'Pakistan': '巴基斯坦',
    'Bangladesh': '孟加拉国',
    'Sri Lanka': '斯里兰卡',
    'Kazakhstan': '哈萨克斯坦',
    'Uzbekistan': '乌兹别克斯坦',
    'Mongolia': '蒙古',
    'Cambodia': '柬埔寨',
    'Myanmar': '缅甸',
    'Laos': '老挝',
    'Nepal': '尼泊尔',
    'Bhutan': '不丹',
    'Maldives': '马尔代夫',
    'Brunei': '文莱',
    'Timor-Leste': '东帝汶',
    'Afghanistan': '阿富汗',
    'Tajikistan': '塔吉克斯坦',
    'Kyrgyzstan': '吉尔吉斯斯坦',
    'Turkmenistan': '土库曼斯坦',
    'Azerbaijan': '阿塞拜疆',
    'Georgia': '格鲁吉亚',
    'Armenia': '亚美尼亚',
    'Cyprus': '塞浦路斯',
    'Turkey': '土耳其',
    'Israel': '以色列',
    'Lebanon': '黎巴嫩',
    'Jordan': '约旦',
    'Saudi Arabia': '沙特阿拉伯',
    'United Arab Emirates': '阿联酋',
    'Qatar': '卡塔尔',
    'Kuwait': '科威特',
    'Bahrain': '巴林',
    'Oman': '阿曼',
    'Yemen': '也门',
    'Iraq': '伊拉克',
    'Syria': '叙利亚',
    'Iran': '伊朗',
    'Egypt': '埃及',
    'Morocco': '摩洛哥',
    'Tunisia': '突尼斯',
    'Algeria': '阿尔及利亚',
    'Libya': '利比亚',
    'Sudan': '苏丹',
    'South Sudan': '南苏丹',
    'Eritrea': '厄立特里亚',
    'Djibouti': '吉布提',
    'Somalia': '索马里',
    'Ethiopia': '埃塞俄比亚',
    'Kenya': '肯尼亚',
    'Tanzania': '坦桑尼亚',
    'Uganda': '乌干达',
    'Rwanda': '卢旺达',
    'Burundi': '布隆迪',
    'Democratic Republic of the Congo': '刚果民主共和国',
    'Republic of the Congo': '刚果共和国',
    'Gabon': '加蓬',
    'Equatorial Guinea': '赤道几内亚',
    'Cameroon': '喀麦隆',
    'Central African Republic': '中非共和国',
    'Chad': '乍得',
    'Niger': '尼日尔',
    'Nigeria': '尼日利亚',
    'Benin': '贝宁',
    'Togo': '多哥',
    'Ghana': '加纳',
    'Côte d\'Ivoire': '科特迪瓦',
    'Liberia': '利比里亚',
    'Sierra Leone': '塞拉利昂',
    'Guinea': '几内亚',
    'Guinea-Bissau': '几内亚比绍',
    'Senegal': '塞内加尔',
    'The Gambia': '冈比亚',
    'Mauritania': '毛里塔尼亚',
    'Mali': '马里',
    'Burkina Faso': '布基纳法索',
    'Angola': '安哥拉',
    'Namibia': '纳米比亚',
    'Botswana': '博茨瓦纳',
    'Zimbabwe': '津巴布韦',
    'Mozambique': '莫桑比克',
    'Malawi': '马拉维',
    'Zambia': '赞比亚',
    'Lesotho': '莱索托',
    'Eswatini': '斯威士兰',
    'Madagascar': '马达加斯加',
    'Comoros': '科摩罗',
    'Mauritius': '毛里求斯',
    'Seychelles': '塞舌尔',
    'Cape Verde': '佛得角',
    'São Tomé and Príncipe': '圣多美和普林西比',
    'Western Sahara': '西撒哈拉',
    'South Africa': '南非',
    'United Kingdom': '英国',
    'France': '法国',
    'Germany': '德国',
    'Italy': '意大利',
    'Spain': '西班牙',
    'Portugal': '葡萄牙',
    'Netherlands': '荷兰',
    'Belgium': '比利时',
    'Switzerland': '瑞士',
    'Austria': '奥地利',
    'Sweden': '瑞典',
    'Norway': '挪威',
    'Denmark': '丹麦',
    'Finland': '芬兰',
    'Iceland': '冰岛',
    'Ireland': '爱尔兰',
    'Luxembourg': '卢森堡',
    'Greece': '希腊',
    'Poland': '波兰',
    'Czech Republic': '捷克共和国',
    'Slovakia': '斯洛伐克',
    'Hungary': '匈牙利',
    'Romania': '罗马尼亚',
    'Bulgaria': '保加利亚',
    'Croatia': '克罗地亚',
    'Slovenia': '斯洛文尼亚',
    'Estonia': '爱沙尼亚',
    'Latvia': '拉脱维亚',
    'Lithuania': '立陶宛',
    'Malta': '马耳他',
    'Albania': '阿尔巴尼亚',
    'North Macedonia': '北马其顿',
    'Montenegro': '黑山',
    'Serbia': '塞尔维亚',
    'Bosnia and Herzegovina': '波黑',
    'Kosovo': '科索沃',
    'Moldova': '摩尔多瓦',
    'Ukraine': '乌克兰',
    'Belarus': '白俄罗斯',
    'Russia': '俄罗斯',
    'Canada': '加拿大',
    'Mexico': '墨西哥',
    'Brazil': '巴西',
    'Argentina': '阿根廷',
    'Chile': '智利',
    'Peru': '秘鲁',
    'Colombia': '哥伦比亚',
    'Venezuela': '委内瑞拉',
    'Ecuador': '厄瓜多尔',
    'Bolivia': '玻利维亚',
    'Paraguay': '巴拉圭',
    'Uruguay': '乌拉圭',
    'Guyana': '圭亚那',
    'Suriname': '苏里南',
    'French Guiana': '法属圭亚那',
    'Falkland Islands': '福克兰群岛',
    'Australia': '澳大利亚',
    'New Zealand': '新西兰',
    'Papua New Guinea': '巴布亚新几内亚',
    'Fiji': '斐济',
    'Solomon Islands': '所罗门群岛',
    'Vanuatu': '瓦努阿图',
    'New Caledonia': '新喀里多尼亚',
    'French Polynesia': '法属波利尼西亚',
    'Samoa': '萨摩亚',
    'Tonga': '汤加',
    'Kiribati': '基里巴斯',
    'Tuvalu': '图瓦卢',
    'Nauru': '瑙鲁',
    'Palau': '帕劳',
    'Marshall Islands': '马绍尔群岛',
    'Micronesia': '密克罗尼西亚',
    'Northern Mariana Islands': '北马里亚纳群岛',
    'Guam': '关岛',
    'American Samoa': '美属萨摩亚',
    'Hawaii': '夏威夷',
    'Alaska': '阿拉斯加',
    'Puerto Rico': '波多黎各',
    'U.S. Virgin Islands': '美属维尔京群岛',
    'British Virgin Islands': '英属维尔京群岛',
    'Cayman Islands': '开曼群岛',
    'Bermuda': '百慕大',
    'Greenland': '格陵兰',
    'Faroe Islands': '法罗群岛',
    'Svalbard': '斯瓦尔巴群岛',
    'Aruba': '阿鲁巴',
    'Curaçao': '库拉索',
    'Sint Maarten': '荷属圣马丁',
    'Saint Martin': '法属圣马丁',
    'Saint Barthélemy': '圣巴泰勒米',
    'Guadeloupe': '瓜德罗普',
    'Martinique': '马提尼克',
    'Saint Pierre and Miquelon': '圣皮埃尔和密克隆',
    'Wallis and Futuna': '瓦利斯和富图纳',
    'Mayotte': '马约特',
    'Réunion': '留尼汪',
    'Christmas Island': '圣诞岛',
    'Cocos Islands': '科科斯群岛',
    'Norfolk Island': '诺福克岛',
    'Heard Island and McDonald Islands': '赫德岛和麦克唐纳群岛',
    'French Southern and Antarctic Lands': '法属南部领地',
    'Bouvet Island': '布韦岛',
    'South Georgia and the South Sandwich Islands': '南乔治亚和南桑威奇群岛',
    'Antarctica': '南极洲'
}

# 定义可用于图表的维度
chart_dimensions = {
    '评级等级': {'values': rating_order},
    '一级行业': {'values': sorted(df['一级行业'].unique())},
    '所属地区': {'values': sorted(df['所属地区'].unique())},
    '评级变动': {'values': sorted(df['评级变动描述'].unique(), key=lambda x: float(df[df['评级变动描述'] == x]['评级变动'].iloc[0]) if pd.notna(x) else float('-inf'))},
}

@app.route('/')
def index():
    # 获取评级变动并按数字大小排序
    sorted_changes = sorted(
        df['评级变动描述'].unique(),
        key=lambda x: float(df[df['评级变动描述'] == x]['评级变动'].iloc[0]) if pd.notna(x) else float('-inf')
    )
    
    # 获取所有可用的筛选条件
    filters = {
        'industries_l1': sorted(df['一级行业'].unique().tolist()),
        'rating_changes': sorted_changes,
        'regions': sorted(df['所属地区'].unique().tolist()),
        'ratings': rating_order,
        'years': sorted(df['评级年份'].unique().tolist()),
        'dimensions': list(chart_dimensions.keys()),
        'region_mapping': region_mapping  # 添加地区映射到模板
    }
    return render_template('index.html', filters=filters)

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    data = request.json
    chart_type = data.get('chart_type')
    filters = data.get('filters', {})
    dimension = data.get('dimension', '评级等级')  # 默认使用评级等级作为维度
    
    # 应用筛选条件
    filtered_df = df.copy()
    
    # 处理多选筛选条件
    if filters.get('industry_l1'):
        filtered_df = filtered_df[filtered_df['一级行业'].isin(filters['industry_l1'])]
    if filters.get('rating_change'):
        filtered_df = filtered_df[filtered_df['评级变动描述'].isin(filters['rating_change'])]
    if filters.get('region'):
        filtered_df = filtered_df[filtered_df['所属地区'].isin(filters['region'])]
    if filters.get('rating'):
        filtered_df = filtered_df[filtered_df['评级等级'].isin(filters['rating'])]
    if filters.get('year'):
        filtered_df = filtered_df[filtered_df['评级年份'].isin([int(y) for y in filters['year']])]

    # 处理维度筛选
    dimension_filter = None
    if dimension == '评级等级' and filters.get('rating'):
        dimension_filter = filters['rating']
    elif dimension == '一级行业' and filters.get('industry_l1'):
        dimension_filter = filters['industry_l1']
    elif dimension == '评级变动' and filters.get('rating_change'):
        dimension_filter = filters['rating_change']
    elif dimension == '所属地区' and filters.get('region'):
        dimension_filter = filters['region']

    fig = None
    if chart_type == 'bar':
        if dimension == '评级等级':
            counts = filtered_df[dimension].value_counts()
            if dimension_filter:
                counts = counts.reindex(dimension_filter)
            else:
                counts = counts.reindex(rating_order)
        elif dimension == '评级变动':
            counts = filtered_df['评级变动描述'].value_counts()
            if dimension_filter:
                counts = counts.reindex(dimension_filter)
            else:
                sorted_index = sorted(
                    counts.index,
                    key=lambda x: float(df[df['评级变动描述'] == x]['评级变动'].iloc[0]) if pd.notna(x) else float('-inf')
                )
                counts = counts.reindex(sorted_index)
        else:
            counts = filtered_df[dimension].value_counts()
            if dimension_filter:
                counts = counts.reindex(dimension_filter)
            elif dimension in chart_dimensions:
                counts = counts.reindex(chart_dimensions[dimension]['values'])
        
        fig = go.Figure(data=[
            go.Bar(
                x=counts.index,
                y=counts.values,
                text=counts.values,
                textposition='auto',
            )
        ])
        fig.update_layout(
            title=f'按{dimension}的分布',
            xaxis_title='维度值',
            yaxis_title='公司数量'
        )
    
    elif chart_type == 'pie':
        if dimension == '评级等级':
            counts = filtered_df[dimension].value_counts()
            if dimension_filter:
                counts = counts.reindex(dimension_filter)
            else:
                counts = counts.reindex(rating_order)
        elif dimension == '评级变动':
            counts = filtered_df['评级变动描述'].value_counts()
            if dimension_filter:
                counts = counts.reindex(dimension_filter)
            else:
                sorted_index = sorted(
                    counts.index,
                    key=lambda x: float(df[df['评级变动描述'] == x]['评级变动'].iloc[0]) if pd.notna(x) else float('-inf')
                )
                counts = counts.reindex(sorted_index)
        else:
            counts = filtered_df[dimension].value_counts()
            if dimension_filter:
                counts = counts.reindex(dimension_filter)
            elif dimension in chart_dimensions:
                counts = counts.reindex(chart_dimensions[dimension]['values'])
            
        fig = px.pie(
            values=counts.values,
            names=counts.index,
            title=f'按{dimension}的分布'
        )
    
    elif chart_type == 'line':
        if dimension == '评级时间':
            # 生成评级时间趋势的折线图
            time_trend = filtered_df.groupby('评级时间').size().reset_index()
            time_trend.columns = ['评级时间', '评级数量']
            fig = px.line(
                time_trend,
                x='评级时间',
                y='评级数量',
                title='评级时间分布趋势'
            )
        else:
            if dimension == '评级变动':
                group_col = '评级变动描述'
            else:
                group_col = dimension
                
            time_series = filtered_df.groupby(['评级时间', group_col]).size().reset_index()
            time_series.columns = ['评级时间', dimension, '数量']
            
            if dimension_filter:
                time_series = time_series[time_series[dimension].isin(dimension_filter)]
            
            if dimension == '评级变动':
                # 按评级变动数字排序图例
                sorted_changes = sorted(
                    time_series[dimension].unique(),
                    key=lambda x: float(df[df['评级变动描述'] == x]['评级变动'].iloc[0]) if pd.notna(x) else float('-inf')
                )
                time_series[dimension] = pd.Categorical(time_series[dimension], categories=sorted_changes, ordered=True)
                
            fig = px.line(
                time_series,
                x='评级时间',
                y='数量',
                color=dimension,
                title=f'按{dimension}的时间趋势'
            )

    if fig:
        return jsonify({
            'chart_data': fig.to_json(),
            'success': True
        })
    
    return jsonify({
        'success': False,
        'error': '无法生成图表'
    })

if __name__ == '__main__':
    app.run(debug=True) 