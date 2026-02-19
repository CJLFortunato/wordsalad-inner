def format_donut_chart_data (projects):
    data = {
        "zero": 0,
        "low": 0,
        "middle": 0,
        "high": 0,
        "over": 0
    }
    for project in projects:
        if project.percentage > 110:
            data["over"] += 1
        elif project.percentage > 100 and project.percentage < 110:
            data["high"] += 1
        elif project.percentage > 33 and project.percentage < 100:
            data["middle"] += 1
        elif project.percentage > 0 and project.percentage <= 33:
            data["low"] += 1
        else:
            data["zero"] += 1

    formatted_data = [
        {"label": 'zero', "y": data["zero"], "color": 'hsl(210, 10%, 40%)'},
        {"label": 'low', "y": data["low"], "color": 'hsl(0, 50%, 60%)'},
        {"label": 'middle', "y": data["middle"], "color": 'hsl(45, 95%, 70%)'},
        {"label": 'high', "y": data["high"], "color": 'hsl(130, 70%, 70%)'},
        {"label": 'over', "y": data["over"], "color": 'hsl(260, 50%, 70%)'},
    ]

    return formatted_data
