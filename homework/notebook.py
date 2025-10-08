#%% 
# PREPARACIÓN
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os

# Intentar importar display si se ejecuta en Jupyter
try:
    from IPython.display import display
except ImportError:
    display = print  # fallback si no existe

pd.set_option("display.notebook_repr_html", True)


#%% 
# CARGA DE TABLAS
drivers = pd.read_csv(
    "files/input/drivers.csv",
    sep=",",
    thousands=None,
    decimal="."
)
drivers.head()


timesheet = pd.read_csv(
    "files/input/timesheet.csv",
    sep=",",
    thousands=None,
    decimal="."
)
timesheet.head()


#%%
# MEDIA DE HORAS Y MILLAS POR CONDUCTOR
mean_timesheet = timesheet.groupby("driverId").mean()
mean_timesheet.pop("week")
mean_timesheet.head()


#%% 
# REGISTROS POR DEBAJO DE LA MEDIA
mean_hours_logged_by_driver = timesheet.groupby("driverId")["hours-logged"].transform("mean")

timesheet_with_means = timesheet.copy()
timesheet_with_means["mean_hours-logged"] = mean_hours_logged_by_driver

timesheet_below = timesheet_with_means[
    timesheet_with_means["hours-logged"] < timesheet_with_means["mean_hours-logged"]
]
display(timesheet_below.head())
display(timesheet_below.tail())


#%% 
# CÓMPUTO TOTAL DE HORAS Y MILLAS POR CONDUCTOR
sum_timesheet = timesheet.groupby("driverId").sum()
sum_timesheet.head(10)

timesheet.groupby("driverId")["hours-logged"].agg([min, max])


#%% 
# UNIÓN DE TABLAS
summary = pd.merge(
    sum_timesheet,
    drivers[["driverId", "name"]],
    on="driverId",
)
summary.head()


#%% 
# ALMACENAMIENTO DE RESULTADOS
if not os.path.exists("files/output"):
    os.makedirs("files/output")

summary.to_csv(
    "files/output/summary.csv",
    sep=",",
    header=True,
    index=False,
)


#%%
# ORDENAMIENTO POR MILLAS Y TOP 10
top10 = summary.sort_values(by="miles-logged", ascending=False).head(10)
top10 = top10.set_index("name")


#%% 
# GRÁFICO DE BARRAS HORIZONTALES
top10["miles-logged"].plot.barh(color="tab:orange", alpha=0.6)

plt.gca().invert_yaxis()

plt.gca().get_xaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
)

plt.xticks(rotation=90)

plt.gca().spines["left"].set_color("lightgray")
plt.gca().spines["bottom"].set_color("gray")
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

if not os.path.exists("files/plots"):
    os.makedirs("files/plots")

plt.savefig("files/plots/top10_drivers.png", bbox_inches="tight")
plt.show()
