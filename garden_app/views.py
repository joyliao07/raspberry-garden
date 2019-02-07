from .models import Temperature
from garden_api.models import SoilMoisture
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404, get_object_or_404

import bokeh.plotting as bk
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, Label, BoxZoomTool, PanTool, ZoomInTool, ZoomOutTool, ResetTool

@login_required
def weekly_view(request):
    """To render weekly_view with its content."""

    # To populate temp_list:
    temps = Temperature.objects.all()
    temp_date = []
    temp_read = []
    temp_list = []
    i = 0
    for item in temps:
        if item.date_added.date() not in temp_date and i < 7:
            temp_date.append(item.date_added.date())
            temp_read.append(item.temperature)
            i += 1
    for i in range(len(temp_date)):
        obj = {'date_added': temp_date[i], 'temperature': temp_read[i]}
        temp_list.append(obj)

    # To populate water_list:
    waters = SoilMoisture.objects.all()
    water_date = []
    water_read = []
    water_list = []
    for i in range(len(waters)):
        if waters[i].time_stamp.date() not in water_date and i < 7:
            water_date.append(waters[i].time_stamp.date())
            water_read.append('Dry')
            if water_read[i] == 'Dry':
                if waters[i].has_moisture == 'True':
                    water_read[i] = 'Has Water'
    for i in range(len(water_date)):
        obj = {'time_stamp': water_date[i], 'has_moisture': water_read[i]}
        water_list.append(obj)

    context = {
        # 'temperatures': get_list_or_404(Temperature),
        'temperatures': temp_list,
        # 'waterlevel': get_list_or_404(SoilMoisture),
        'waterlevel': water_list,
    }

    return render(request, 'raspberry/weekly.html', context)


@login_required
def monthly_view(request):
    """To render monthly_view with its content."""

    # TO POPULATE TEMP_DATE AND TEMP_READ:
    temps = Temperature.objects.all()
    temp_date = []
    temp_read = []
    i = 0
    for item in temps:
        if item.date_added.date() not in temp_date and i < 31:
            temp_date.append(item.date_added.date())
            temp_read.append(item.temperature)
            i += 1

    # TO PLOT TEMPERATURE STOCK_CHART
    p1 = bk.figure(title=f'Temperature', x_axis_type="datetime", width=350, height=300)
    p1.grid.grid_line_alpha = 0.3
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Temperature'
    p1.line(temp_date, temp_read, color='red')
    p1.legend.location = "top_left"
    script_temperature, div_temperature = components(p1)

    # TO POPULATE WATER_DATE AND WATER_READ:
    waters = SoilMoisture.objects.all()
    water_date = []
    water_read = []
    for i in range(len(waters)):
        if waters[i].time_stamp.date() not in water_date and i < 7:
            water_date.append(waters[i].time_stamp.date())
            water_read.append(0)
            if water_read[i] == 0:
                if waters[i].has_moisture == 'True':
                    water_read[i] = 1

    # TO PLOT WATER IRIS_CHART
    p3 = figure(title="WaterLevel", x_axis_type="datetime", width=350, height=300)
    p3.xaxis.axis_label = 'Date'
    p3.yaxis.axis_label = 'WaterLevel'

    p3.circle(water_date, water_read, color='blue', fill_alpha=0.2, size=10)

    script_water, div_water = components(p3)

    context = {
        'temperatures': get_list_or_404(Temperature),
        'the_script_temperature': script_temperature,
        'the_div_temperature': div_temperature,
        'the_script_water': script_water,
        'the_div_water': div_water,
    }

    return render(request, 'raspberry/monthly.html', context)
