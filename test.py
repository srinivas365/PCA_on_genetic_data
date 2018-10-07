from pca_gene import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

dataset=pd.read_csv('gene_data.csv')
metaset=pd.read_csv('meta.csv')



#data preprocessing
dataset=dataset.transpose()
dataset.drop(['Unnamed: 0'],inplace=True)
dataset.drop(['symbol'],inplace=True)




#importing GenePca class
genepca=GenePca(dataset,metaset['Cluster'])

#filling nan values with mean
genepca.fill_nans(measure='mean')

#setting dimension to 2
genepca.set_components(2)

#reduced dataset
dataset=genepca.get_reduced_set(std_scale=1)
pca=genepca.getpca()

print('Explained variance:',genepca.get_ev())
print('Explained variance ratio:',genepca.get_evr())



x_train,x_test,y_train,y_test=train_test_split(dataset,metaset['Cluster'],test_size=0.3,random_state=20)


'''
Random forest classifier has good accuracy when compared to 
other classification
algorithms

'''

#random forest 
from sklearn.ensemble import RandomForestClassifier
classifier=RandomForestClassifier(n_estimators=10,criterion='entropy',random_state=0)



'''
#LogisticRegression
from sklearn.linear_model import LogisticRegression
classifier=LogisticRegression(random_state=0)

#naive bayes
from sklearn.naive_bayes import GaussianNB
classifier=GaussianNB()


#random forest 
from sklearn.ensemble import RandomForestClassifier
classifier=RandomForestClassifier(n_estimators=10,criterion='entropy',random_state=0)


#kmeans 
from sklearn.neighbors import KNeighborsClassifier
classifier=KNeighborsClassifier(n_neighbors=5,metric='minkowski',p=2)

'''

#training dataset
classifier.fit(x_train,y_train)

#testing dataset
y_pred=classifier.predict(x_test)
print('Actaul--Predicted')
for i,j in zip(y_test.values,y_pred):
	print(i,'-',j)



#visualizing
genepca.visualize()
