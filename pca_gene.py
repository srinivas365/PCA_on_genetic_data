"""
GenePca is class used to work on PCA of gene datasets

GenePca(x_dataframe,y_dataframe)

standardize() 
    -standardize the given x_dataframe

set_components(components=2)
    -will reduce x_dataframe into given components features

get_reduced_set(std_scale=0)
    -will return reduced set after PCA on it 
    -if std_scale=1 x_dataframe will get standardized before PCA

getpca()
    -return pca object

get_evr()
    -return explained_variance_ratio

get_ev()
    -return explained_variance 

fill_nans(measure='mean')
    -replace the Nan values in column with column mean/median

visualize()
    -visualize the datasets
    -applicable only for two dimensions

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
sns.set()

class Error(Exception):
   """Base class for other exceptions"""
   pass

class GenePca(object):
    """docstring for ClassName"""

    def __init__(self, x,y):
        try:
            if x.shape[0]==y.shape[0]:
                self.x=x
                self.y=y
                print('x shape:',x.shape)
                print('y shape:',y.shape)
                nan_list=self.x.columns[self.x.isna().any()].tolist()
                print('x dataset contains nan values in columns :',nan_list)
            else:
                raise Error
        except Error:
            print('x rows:',x.shape[0])
            print('y rows:',y.shape[0])
            print('GP Error: dataframes shape mismatch')
    def standardize(self):
        self.sc_x=StandardScaler()
        self.x=self.sc_x.fit_transform(self.x)             
    def set_components(self,components=2):
        self.pca=PCA(n_components=components)
        
    def get_reduced_set(self,std_scale=0):
        try:
            if std_scale!=0 and std_scale!=1:
                raise Error
            elif std_scale==1:
                self.standardize()
                self.red_x=self.pca.fit_transform(self.x)
                self.red_x=pd.DataFrame(self.red_x)
            else:
                self.red_x=self.pca.fit_transform(self.x)
                self.red_x=pd.DataFrame(self.red_x)
            return self.red_x 
        except Error:
            print("Error:wrong value for scale")

    def visualize(self):
        try:
            if self.red_x.shape[1]==2:
                classes=set(self.y)
                cmap = plt.get_cmap('Set1', len(classes))
                cmap.set_under('gray')
                fig, ax = plt.subplots()
                cax = ax.scatter(self.red_x.iloc[:, 0], self.red_x.iloc[:, 1],
                            c=self.y ,s=100, cmap=cmap, vmin=self.y.min(), vmax=self.y.max())
                fig.colorbar(cax, extend='min')
                plt.xlabel('PC1')
                plt.ylabel('PC2')
                plt.show()
            else:
                raise Error
        except Error:
            print("GP Error:contains more than two dimensions")
    def get_evr(self):
        try:
            if self.pca==None:
                raise Error
            return self.pca.explained_variance_ratio_
        except Error:
            print("GP Error: PCA object Not found")
    def get_ev(self):
         try:
            if self.pca==None:
                raise Error
            return self.pca.explained_variance_
         except Error:
            print("GP Error: PCA object Not found")
    def fill_nans(self,measure='mean'):
        nan_list=self.x.columns[self.x.isna().any()].tolist()
        self.x=self.x.apply(pd.to_numeric)
        try:
            for i in nan_list:
                if measure=='mean':
                    self.x[i].fillna(self.x[i].mean(),inplace=True)
                elif measure=='median':
                    self.x[i].fillna(self.x[i].median(),inplace=True)
                else:
                    raise Error
                print("removed nan values in column:",i)
        except Error:
            print("GP Error:unknow measure choose only median or mean")
        
    def getpca(self):
        return self.pca