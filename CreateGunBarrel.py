import xlsxwriter

# Create a new workbook and add a worksheet
workbook = xlsxwriter.Workbook("OilBarrelPlot.xlsx")
worksheet = workbook.add_worksheet()

# Data as Python arrays
data = {
    "grid_x": [-2640, -1320, 0, 1320, 2640, 3960, 5280, 6600, 7920],
    "depth": [-6000, -6500, -7000, -7500, -8000, -8500],
    "vertical_line_x": [0, 0],
    "vertical_line_y": [-8500, -6000],
    "annotation_x": [0],  # X-value for annotation (center of the chart)
    "annotation_y": [-8700], # Y-value for annotation (near top of chart area)
}

# Write data to the worksheet and get ranges
worksheet.write(0, 0, "Grid X (ft)")
worksheet.write(0, 1, "Depth (ft)")
for i, (x, y) in enumerate(zip(data["grid_x"], data["depth"]), start=1):
    worksheet.write(i, 0, x)
    worksheet.write(i, 1, y)

# Write vertical line data
worksheet.write(0, 3, "Vertical Line X")
worksheet.write(0, 4, "Vertical Line Y")
for i, (x, y) in enumerate(zip(data["vertical_line_x"], data["vertical_line_y"]), start=1):
    worksheet.write(i, 3, x)
    worksheet.write(i, 4, y)

# Write annotation data
worksheet.write(0, 6, "Annotation X")
worksheet.write(0, 7, "Annotation Y")
for i, (x, y) in enumerate(zip(data["annotation_x"], data["annotation_y"]), start=1):
    worksheet.write(i, 6, x)
    worksheet.write(i, 7, y)

# Create a scatter chart
chart = workbook.add_chart({"type": "scatter"})

# Configure the main series
chart.add_series({
    "categories": f"=Sheet1!$A$2:$A${len(data['grid_x'])+1}",  # X-values
    "values": f"=Sheet1!$B$2:$B${len(data['depth'])+1}",        # Y-values
    "marker": {"type": "circle", "size": 7},                   # Circle markers
})

# Add the vertical line series
chart.add_series({
    "categories": "=Sheet1!$D$2:$D$3",  # X-values for the line
    "values": "=Sheet1!$E$2:$E$3",      # Y-values for the line
    "line": {
        "color": "blue",
        "width": 1,  # Thin line
        "dash_type": "dash",  # Dashed line
    },
    "marker": {"type": "none"},  # No markers for the line
})

# Add the annotation series
chart.add_series({
    "categories": "=Sheet1!$G$2:$G$2",  # X-value for annotation
    "values": "=Sheet1!$H$2:$H$2",      # Y-value for annotation
    "marker": {"type": "none"},         # Hide marker
    "data_labels": {
        "value": True,
        "custom": [{"text": "Section Line"}],  # Annotation text
        "position": "below"                 # Position label in chart area
    },
})

# Set chart title and axis titles
chart.set_title({"name": "Oil Barrel Plot"})
chart.set_x_axis({
    "name": "Lateral Bottom Hole Spacing (ft)",
    "min": -2640,
    "max": 7920,
    "major_unit": 1320,
    "name_font": {"bold": True},
    "label_position": "low",
    "crossing": "min",
})
chart.set_y_axis({
    "name": "Depth Below MSL (ft)",
    "min": -8500,
    "max": -6000,
    "major_unit": 500,
    "name_font": {"bold": True},
    "label_position": "low",
})

# Adjust plot area and chart area
chart.set_plotarea({"x": 0.1, "y": 0.1, "width": 0.7, "height": 0.7})
chart.set_chartarea({"x": 0.1, "y": 0.1, "width": 0.7, "height": 0.7})

# Set chart size and layout
chart.set_size({"width": 1100, "height": 550})  # ~11.5" x 8"
chart.set_legend({"none": True})  # Disable legend

# Insert the chart into the worksheet
worksheet.insert_chart("D5", chart)

# Close the workbook
workbook.close()
print("Oil barrel plot with chart area annotation created.")
