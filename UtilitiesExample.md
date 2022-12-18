---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Utilities


## Imports

```python
import pandas
import pathlib
import numpy
import glob
import utilities as utils
import plotly.graph_objs as go
from plotly.subplots import make_subplots
```

```python
cell_volume = 130.6 * 200.5 * 37.2 / 1000 / 1000 / 1000
```

## Read data

Read in all of the csv data files into a single dataframe

```python
data_directory = pathlib.Path().cwd() / "data"
assert data_directory.is_dir(), f"Error: {filename.as_posix()} is not a file"
```

```python
files = data_directory.glob("*.csv")
df = pandas.concat((pandas.read_csv(f) for f in files), ignore_index=True)
```

```python
df.head()
```

Create a new column for the cycle time

```python
# Make a dictionary of the first and last timestep in a cycle
# Algorithm: isolate the totTime_s column at each cycle and grab the first and last entry (0, -1)
# ex {1: [first_time, last_time]}

cycle_time_dict = {}

for cycle in df.cycle.unique():
    tmp = df[df.cycle == cycle]["totTime_s"]
    fl = [tmp.iloc[i] for i in (0, -1)]
    cycle_time_dict[cycle] = fl
```

```python
# Create a new column by mapping to the cycle_time_dict
df["cycleTimeStart_s"] = df["cycle"].map(lambda x: cycle_time_dict[x][0])
df["cycleTime_s"] = df["totTime_s"] - df["cycleTimeStart_s"]
df["Qheat_W"] = df["Qheat_Wm3"] * cell_volume

df
```

## Cycle Capacity

```python
utils.returnCycleCapacity(df)
```

## Plots

```python
def return_layout(xaxis_title, yaxis_title):
    layout = go.Layout(
        xaxis=dict(
            #title="Time (s)",
            title=xaxis_title,
            # type="log",
            autorange=True,
            showgrid=True,
            zeroline=False,
            showline=True,
            ticks="",
            showticklabels=True,
            titlefont=dict(
                size=24,
            ),
            tickfont=dict(
                size=18,
                color="black",
            ),
        ),
        yaxis=dict(
            #title="Voltage (V)",
            title=yaxis_title,
            # type="log",
            autorange=True,
            showgrid=True,
            zeroline=False,
            showline=True,
            ticks="",
            showticklabels=True,
            titlefont=dict(
                size=24,
            ),
            tickfont=dict(
                size=18,
                color="black",
            ),
        ),
    )
    return layout
```

```python code_folding=[]
data = []

fig = make_subplots(specs=[[{"secondary_y": True}]])

trace = go.Scatter(
    x=df.totTime_s,
    y=df.voltage_V,
    mode="lines",
    name="Voltage (V)"

)
fig.add_trace(trace, secondary_y=False)

trace = go.Scatter(
    x=df.totTime_s,
    y=df.Temp_K - 273.15,
    mode="lines",
    name="Temperature (C)"
)
fig.add_trace(trace, secondary_y=True)


# Set x-axis title
fig.update_xaxes(title_text="Time (s)")

# Set y-axes titles
fig.update_yaxes(title_text="Voltage (V)", secondary_y=False)
fig.update_yaxes(title_text="Temperature (C)", secondary_y=True)


#figure = go.Figure(data=trace, layout=layout)
fig.show()
```

```python
data = []

for cycle in df.cycle.unique():
    trace = go.Scatter(
        x=df.cycleTime_s[df.cycle == cycle],
        y=df.voltage_V[df.cycle == cycle],
        mode="lines",
        name=f"cyle = {cycle}",
    )
    data.append(trace)

figure = go.Figure(data=data, layout=return_layout("Time (s)", "Voltage (V)"))
figure.show()
```

```python
data = []

for cycle in df.cycle.unique():
    trace = go.Scatter(
        x=df.cycleTime_s[df.cycle == cycle],
        y=df.Qheat_W[df.cycle == cycle],
        mode="lines",
        name=f"cyle = {cycle}",
    )
    data.append(trace)

figure = go.Figure(data=data, layout=return_layout("Time (s)", "Heat Gen (W)"))
figure.show()
```

```python
# average heat gen for step 2 (charge)
df[df.step == 2].Qheat_W.mean()
```

```python
# find the duration of each step

step_time = []

for cycle in df.cycle.unique():
    tmp = df[df.cycle == cycle] #["totTime_s"]
    
    for step in tmp.step.unique():
        tmp2 = tmp[df.step == step]["totTime_s"]
        fl = [tmp2.iloc[i] for i in (0, -1)]
        fl.insert(0, step)
        fl.insert(0, cycle)
        step_time.append(fl)

timing = pandas.DataFrame(step_time, columns=["cycle", "step", "start_time", "end_time"])
timing["step_duration_s"] = timing["end_time"] - timing["start_time"]

timing
```

```python

```
