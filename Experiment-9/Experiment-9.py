# data loading
# data cleaning-check for missing values,fillna,duplicate
# statistics analysis-mean,mode,meadian
# customer segmentation-k means clustering
# visualization-scatter plot,bar chart
# customer insights-insights of each customer segement
# customere engagement recommendation

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


#Data Loading
df=pd.read_csv("Online Retail.csv")

print(df.head())
print(df.shape)

#Data Cleaning
print("------------------------------------------------Data Cleaning----------------------------------------------")
print(df.isnull().sum())

print(df['Description'].values)
df['CustomerID']=df['CustomerID'].ffill()
df['Description']=df['Description'].bfill()
print(df.duplicated().sum())
df.duplicated()
df.drop_duplicates()
print(df.isnull().sum())


#Statistics Analysis
print("------------------------------------------------Statistics Analysis----------------------------------------------")
print(df.describe())



# customer segmentation-k means clustering
print("------------------------------------------------customer segmentation-k means clustering----------------------------------------------")

# Selecting features for clustering
features = df[['Quantity', 'UnitPrice']].dropna()
# Standardizing the features
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)
# Applying KMeans clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(features_scaled)
df['Cluster'] = kmeans.labels_
print(df[['Quantity', 'UnitPrice', 'Cluster']].head())
# Visualizing the clusters
plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='Quantity', y='UnitPrice', hue='Cluster', palette='Set1')
plt.title('KMeans Clustering of Customers')
plt.show()
# Insights from clusters
cluster_insights = df.groupby('Cluster').agg({'Quantity':'mean', 'UnitPrice':'mean', 'CustomerID':'nunique'}).reset_index()
print("Cluster Insights:")
print(cluster_insights)


# visualization-scatter plot,bar chart
print("------------------------------------------------visualization-scatter plot,bar chart----------------------------------------------")
plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='Quantity', y='UnitPrice', hue='Country')
plt.title('Scatter plot of Quantity vs UnitPrice')
plt.show()
plt.figure(figsize=(12,6))
sns.barplot(data=df, x='Country', y='Quantity', ci=None)
plt.title('Bar chart of Quantity by Country')
plt.xticks(rotation=90)
plt.show()


# customer insights-insights of each customer segement
print("------------------------------------------------customer insights-insights of each customer segement----------------------------------------------")
country_insights=df.groupby('Country').agg({'Quantity':'sum','UnitPrice':'mean'}).reset_index()
print(country_insights)


# customere engagement recommendation
print("------------------------------------------------customere engagement recommendation----------------------------------------------")
top_countries=country_insights.sort_values(by='Quantity', ascending=False).head(5)
print("Top 5 countries by Quantity:")
print(top_countries)
print("Recommendations:")
for index, row in top_countries.iterrows():
    print(f"Increase marketing efforts in {row['Country']} to boost sales further.")
    if row['UnitPrice'] < df['UnitPrice'].mean():
        print(f"Consider promotional pricing strategies in {row['Country']} to attract more customers.")
    else:
        print(f"Maintain premium pricing in {row['Country']} to sustain profitability.")
