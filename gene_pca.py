

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

dataset=pd.read_csv('gene_data.csv')
dataset=dataset.transpose()
print(dataset.shape)
dataset.drop(['Unnamed: 0'],inplace=True)

dataset.drop(['symbol'],inplace=True)


dataset=dataset.replace({'ssssss': '39.0', 'hhhh' : '321.43'}, regex=True)

print(dataset.columns[dataset.isna().any()].tolist())

dataset=dataset.apply(pd.to_numeric)


dataset[12076].fillna(dataset[12076].median(),inplace=True)

dataset.columns[dataset.isna().any()].tolist()


df=pd.DataFrame(dataset)
from sklearn.preprocessing import StandardScaler
sc_x=StandardScaler()
dataset=sc_x.fit_transform(dataset)

from sklearn.decomposition import PCA
pca=PCA(n_components=2)
x=pca.fit_transform(dataset)
explained_variance=pca.explained_variance_ratio_
print(explained_variance)
print(pca.explained_variance_)
df_y=pd.read_csv('meta.csv')
print(x)
final_dy=pd.DataFrame(x)

final_dy['target']=df_y['Time']

final_dy.columns=['PC1','PC2','Target']


classes=set(final_dy.Target)
cmap = plt.get_cmap('Set1', len(classes))
cmap.set_under('gray')

fig, ax = plt.subplots()
cax = ax.scatter(final_dy.iloc[:, 0], final_dy.iloc[:, 1],
            c=final_dy.Target ,s=100, cmap=cmap, vmin=final_dy.Target.min(), vmax=final_dy.Target.max())
fig.colorbar(cax, extend='min')

plt.show()