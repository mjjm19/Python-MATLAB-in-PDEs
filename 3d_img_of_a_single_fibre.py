import pandas as pd
import plotly.express as px


data = pd.read_csv('/Users/mercyjoshan/Desktop/fibres data/corrected_csv_data3/fiber_export_2.csv')

# Considering only the columns required
required_columns = [' coordinate_x', ' coordinate_y', ' coordinate_z', ' diameter', ' temperature']
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"The CSV file must contain the following columns: {required_columns}")

# Extracting the data
data = data.rename(columns=lambda x: x.strip())  # Remove any leading/trailing spaces in column names
x = data['coordinate_x']
y = data['coordinate_y']
z = data['coordinate_z']
diameter = data['diameter']
temperature = data['temperature']

# Create a DataFrame for plotting
df = pd.DataFrame({
    'X Coordinate': x,
    'Y Coordinate': y,
    'Z Coordinate': z,
    'Diameter': diameter,
    'Temperature': temperature
})

# Create a 3D scatter plot with Plotly
fig = px.scatter_3d(
    df,
    x='X Coordinate',
    y='Y Coordinate',
    z='Z Coordinate',
    color='Temperature',  # Color by temperature
    size='Diameter',  
    hover_data=['Diameter', 'Temperature', 'X Coordinate', 'Y Coordinate', 'Z Coordinate'],
    color_continuous_scale='jet',  # Red, green, yellow, blue color scale
    title="3D Visualization of single fiber"
)

# Show the interactive plot
fig.show()
