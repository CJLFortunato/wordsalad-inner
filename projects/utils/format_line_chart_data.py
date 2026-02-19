from django.utils.timezone import localtime
from .get_progress_color import get_progress_color

def format_line_chart_data(progress, target_count):
    data = []
    # print(progress)
    for item in progress:
        data.append({
            "label": localtime(item.insertion_date).strftime("%d/%m/%Y %H:%M"),
            "y": item.word_count,
            "color": get_progress_color((item.word_count / target_count) * 100),
            "lineColor": get_progress_color((item.word_count / target_count) * 100)
        })




    # print(data)
    return data