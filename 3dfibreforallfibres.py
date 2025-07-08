#In this project, I created a fibre model visualization using python. 
#The 3D fibres shown is being extruded from a multiple nozzles during a fibre melt-blowing process based on 250 csv data files, each with around 2000 data points.


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

folder_path = "/Users/mercyjoshan/Desktop/fibres data/corrected_csv_data3"     # Folder containing the CSV files

fiber_data = []                                                                # Initialize lists for combined data

# Iterate over all CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        
        
        data = pd.read_csv(file_path)                             # Read the CSV file
      
        required_columns = [' coordinate_x', ' coordinate_y', ' coordinate_z', ' diameter', ' temperature']
        if not all(col in data.columns for col in required_columns):
            print(f"Skipping {filename}: Missing required columns.")
            continue
        
        data = data.rename(columns=lambda x: x.strip())            # Remove any leading/trailing spaces in column names
        data['Fiber'] = filename
        fiber_data.append(data)

combined_data = pd.concat(fiber_data, ignore_index=True)           # Combining all fibers into a single DataFrame


df = pd.DataFrame({                                                # Create a DataFrame for plotting
    'X Coordinate': combined_data['coordinate_x'],
    'Y Coordinate': combined_data['coordinate_y'],
    'Z Coordinate': combined_data['coordinate_z'],
    'Diameter': combined_data['diameter'],
    'Temperature': combined_data['temperature'],
    'Fiber': combined_data['Fiber']
})

# Creating a 3D scatter plot with Plotly
fig = px.scatter_3d(
    df,
    x='X Coordinate',
    y='Y Coordinate',
    z='Z Coordinate',
    color='Temperature',
    size='Diameter',
    hover_data=['Diameter', 'Temperature', 'X Coordinate', 'Y Coordinate', 'Z Coordinate', 'Fiber'],
    color_continuous_scale='jet',
    title="3D Visualization of Fibers"
)

# Adding lines connecting points for each fiber
for fiber_name in df['Fiber'].unique():
    fiber_df = df[df['Fiber'] == fiber_name]
    fiber_df = fiber_df.sort_values(by=['X Coordinate', 'Y Coordinate', 'Z Coordinate'])  
    line_trace = go.Scatter3d(
        x=fiber_df['X Coordinate'],
        y=fiber_df['Y Coordinate'],
        z=fiber_df['Z Coordinate'],
        mode='lines',
        line=dict(color='gray', width=1),
        name=fiber_name,
        showlegend=False
    )
    fig.add_trace(line_trace)

# Plotting
fig.show()
