# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import mode

# First load the data file
dataframe = pd.read_csv('Cheapestelectriccars-EVDatabase.csv')
# to see the which type of data we have
dataframe.head()

# Now we get the Manufacturer name from car names
dataframe['Manufacturer'] = dataframe.Name.str.split(' ', 1, expand=True)[0]
dataframe['Manufacturer']

# clean data and prepara the data for analysis

dataframe = dataframe.fillna('0')
dataframe = dataframe.replace({'-': ""}, regex=True)
dataframe = dataframe.replace({'£': ""}, regex=True)
dataframe = dataframe.replace({'€': ""}, regex=True)
dataframe = dataframe.replace({'km/h': ""}, regex=True)
dataframe = dataframe.replace({'Wh/km': ""}, regex=True)
dataframe = dataframe.replace({'km': ""}, regex=True)
dataframe = dataframe.replace({'sec': ""}, regex=True)
dataframe = dataframe.rename(columns={'Subtitle': 'KWH'})
dataframe = dataframe.replace({'Battery Electric Vehicle |       ', ""}, regex=True)
dataframe = dataframe.replace(to_replace='Battery Electric Vehicle |       ', value='', regex=True)
dataframe = dataframe.replace('[^a-zA-Z0-9]', '', regex=True)
dataframe = dataframe.replace({'kWh': ""}, regex=True)

# Now here i store the all column name in list except these columns(Name, Drive, Manufacturer)

All_columns_list = dataframe.columns.tolist()
column_list = []
for i in All_columns_list:
    if i != "Name" and i != "Drive" and i != "Manufacturer":
        column_list.append(i)

column_list

# Now look at nature of data and type of data we have
dataframe.info()

# Now here i change the data of all columns which is store in column_list into numeric for analysis
dataframe[column_list] = dataframe[column_list].apply(pd.to_numeric, errors='coerce', axis=1)
dataframe =dataframe.fillna('0')
dataframe.info()

# correlation between data
# This function ignore the N/A, 0 values and Text format
dataframe.corr()
plt.figure(figsize=(8,6))
sns.heatmap(dataframe.corr(), annot=True)

Drive = []
for i in dataframe["Drive"]:
    Drive.append(i)
count = mode(Drive)

# look at the each type of drive technology
sns.countplot(x = 'Drive', data = dataframe).set(title=('Highest Drive by: '+count))

count = dataframe[dataframe['NumberofSeats'] == float(dataframe.NumberofSeats.mode())].Drive.mode()
#relation between number of seats and drive both
plt.figure(figsize=(8,6))
sns.countplot(x = 'NumberofSeats', hue='Drive', data=dataframe).set(title= str(count) + ' has highest number of seats ')

# to see manyfacturer count
plt.figure(figsize=(18,10))
sns.countplot(y = 'Manufacturer', data = dataframe)
plt.ylabel("Manufacturer of Different Cars")
plt.show()

# # look at relation between acceleartion and KWh Capacity
#plt.figure(figsize=(5,10))
sns.relplot(data=dataframe, x ="Acceleration", y ="KWH", hue="Drive", height=8.27, aspect=11.7/8.27)
plt.xlabel("Acceleration in sec")
plt.ylabel("EV Battery Capacity in KWh")
plt.show()

# Relation ship between top speed and range
sns.lineplot(x = "TopSpeed", y= "Range", data=dataframe)
plt.xlabel("Top speed of Cas in Km/h")
plt.ylabel("Range of Drive in Km")

sns.relplot(y="Efficiency", x="FastChargeSpeed", data=dataframe, height=8.27, aspect=11.7/8.27)
plt.xlabel("Fast Charge speed in km/h")
plt.ylabel("Battery Efficiency in Wh/km")
plt.show()

sns.relplot(y="KWH", x="PriceinUK", data=dataframe, height=8.27, aspect=11.7/8.27)
plt.xlabel("PriceinUK")
plt.ylabel("Battery Capacity")
plt.show()