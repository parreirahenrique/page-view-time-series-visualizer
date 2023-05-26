import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import calendar
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to "date".)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col=0)

# Clean data
df = df[(df["value"] > df["value"].quantile(0.025)) & (df["value"] < df["value"].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, axis = plt.subplots(nrows=1, ncols=1, figsize=(14,6))
    plt.plot(df.index.to_numpy(), df["value"], color="red")
    axis.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    axis.set_xlabel("Date")
    axis.set_ylabel("Page Views")

    # Save image and return fig (don"t change this part)
    fig.savefig("line_plot.png")
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar = df_bar.groupby(pd.PeriodIndex(df_bar["date"], freq="M"))["value"].mean().to_frame()
    df_bar["month"] = df_bar.index.month
    df_bar["year"] = df_bar.index.year
    df_bar = df_bar.sort_values(by="month", axis=0)

    month_dict = {1 : "January", 2 : "February", 3 : "March", 4 : "April", 
              5 : "May" , 6 : "June", 7 : "July", 8 : "August", 
              9 : "September", 10 : "October" , 11 : "November", 12 : "December"}
    df_bar["month"] = df_bar["month"].apply(lambda x: list(month_dict.values())[x - 1])
    
    # Draw bar plot
    fig = plt.figure(figsize=(14,6))
    axis = sns.barplot(data=df_bar, y="value", x="year", hue="month", palette="bright")
    axis.set_xlabel("Years")
    axis.set_ylabel("Average Page Views")
    axis.legend(title="Months", loc="upper left")
    
    # Save image and return fig (don"t change this part)
    fig.savefig("bar_plot.png")
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.month for d in df_box.date]
    df_box = df_box.sort_values(by="month", axis=0)
    df_box["month"] = df_box["month"].apply(lambda x: calendar.month_abbr[x])

    # Draw box plots (using Seaborn)
    fig, (axis1, axis2) = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))
    sns.boxplot(ax=axis1, data=df_box, y="value", x="year", palette="bright")
    axis1.set_title("Year-wise Box Plot (Trend)")
    axis1.set_xlabel("Year")
    axis1.set_ylabel("Page Views")
    sns.boxplot(ax=axis2, data=df_box, y="value", x="month", palette="bright")
    axis2.set_title("Month-wise Box Plot (Seasonality)")
    axis2.set_xlabel("Month")
    axis2.set_ylabel("Page Views")
    
    # Save image and return fig (don"t change this part)
    fig.savefig("box_plot.png")
    return fig
