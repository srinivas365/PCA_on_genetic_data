from pca_gene import *

dataset=pd.read_csv('gene_data.csv')
metaset=pd.read_csv('meta.csv')



#data preprocessing
dataset=dataset.transpose()
dataset.drop(['Unnamed: 0'],inplace=True)
dataset.drop(['symbol'],inplace=True)
dataset=dataset.replace({'ssssss': '39.0', 'hhhh' : '321.43'}, regex=True)



#importing GenePca class
genepca=GenePca(dataset,metaset['Time'])

#filling nan values with mean
genepca.fill_nans(measure='mean')

#setting dimension to 2
genepca.set_components(2)

#reduced dataset
red_set=genepca.get_reduced_set(std_scale=1)
print(red_set)
print('Explained variance:',genepca.get_ev())
print('Explained variance ratio:',genepca.get_evr())
#visualizing
genepca.visualize()