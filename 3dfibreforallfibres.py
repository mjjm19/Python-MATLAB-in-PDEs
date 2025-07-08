"""import pandas as pd
import plotly.express as px
import os

# Folder containing the CSV files
folder_path = "/Users/mercyjoshan/Desktop/fibres data/corrected_csv_data3"

# Initialize lists for combined data
fiber_data = []

# Iterate over all CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        
        # Read the CSV file
        data = pd.read_csv(file_path)
        
        # Ensure the required columns are present
        required_columns = [' coordinate_x', ' coordinate_y', ' coordinate_z', ' diameter', ' temperature']
        if not all(col in data.columns for col in required_columns):
            print(f"Skipping {filename}: Missing required columns.")
            continue
        
        # Remove any leading/trailing spaces in column names
        data = data.rename(columns=lambda x: x.strip())
        
        # Add a column to identify the fiber (use the filename)
        data['Fiber'] = filename  # Optional: to distinguish fibers in hover data
        
        # Append to the combined list
        fiber_data.append(data)

# Combine all fibers into a single DataFrame
combined_data = pd.concat(fiber_data, ignore_index=True)

# Create a DataFrame for plotting
df = pd.DataFrame({
    'X Coordinate': combined_data['coordinate_x'],
    'Y Coordinate': combined_data['coordinate_y'],
    'Z Coordinate': combined_data['coordinate_z'],
    'Diameter': combined_data['diameter'],
    'Temperature': combined_data['temperature'],
    'Fiber': combined_data['Fiber']
})

# Create a 3D scatter plot with Plotly
fig = px.scatter_3d(
    df,
    x='X Coordinate',
    y='Y Coordinate',
    z='Z Coordinate',
    color='Temperature',  # Color by temperature
    size='Diameter',  # Size by diameter
    hover_data=['Diameter', 'Temperature', 'X Coordinate', 'Y Coordinate', 'Z Coordinate', 'Fiber'],
    color_continuous_scale='jet',  # Red, green, yellow, blue color scale
    title="3D Visualization of Fiber Data from Multiple Files"
)

# Show the interactive plot
fig.show()"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Folder containing the CSV files
folder_path = "/Users/mercyjoshan/Desktop/fibres data/corrected_csv_data3"

# Initialize lists for combined data
fiber_data = []

# Iterate over all CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        
        # Read the CSV file
        data = pd.read_csv(file_path)
        
        # Ensure the required columns are present
        required_columns = [' coordinate_x', ' coordinate_y', ' coordinate_z', ' diameter', ' temperature']
        if not all(col in data.columns for col in required_columns):
            print(f"Skipping {filename}: Missing required columns.")
            continue
        
        # Remove any leading/trailing spaces in column names
        data = data.rename(columns=lambda x: x.strip())
        
        # Add a column to identify the fiber (use the filename)
        data['Fiber'] = filename
        
        # Append to the combined list
        fiber_data.append(data)

# Combine all fibers into a single DataFrame
combined_data = pd.concat(fiber_data, ignore_index=True)

# Create a DataFrame for plotting
df = pd.DataFrame({
    'X Coordinate': combined_data['coordinate_x'],
    'Y Coordinate': combined_data['coordinate_y'],
    'Z Coordinate': combined_data['coordinate_z'],
    'Diameter': combined_data['diameter'],
    'Temperature': combined_data['temperature'],
    'Fiber': combined_data['Fiber']
})

# Create a 3D scatter plot with Plotly Express
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

# Add lines connecting points for each fiber
for fiber_name in df['Fiber'].unique():
    fiber_df = df[df['Fiber'] == fiber_name]
    # Ensure points are sorted (adjust sorting logic if needed)
    fiber_df = fiber_df.sort_values(by=['X Coordinate', 'Y Coordinate', 'Z Coordinate'])  # Modify as per your data's order
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

# Show the interactive plot
fig.show()