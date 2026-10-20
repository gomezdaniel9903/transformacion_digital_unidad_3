import numpy as np
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,average_precision_score,roc_auc_score,confusion_matrix,brier_score_loss
def medir(y,p,t=.5):
    pred=(np.asarray(p)>=t).astype(int);tn,fp,fn,tp=confusion_matrix(y,pred,labels=[0,1]).ravel()
    return dict(accuracy=float(accuracy_score(y,pred)),precision=float(precision_score(y,pred,zero_division=0)),recall=float(recall_score(y,pred)),f1=float(f1_score(y,pred)),average_precision=float(average_precision_score(y,p)),roc_auc=float(roc_auc_score(y,p)),brier=float(brier_score_loss(y,p)),tn=int(tn),fp=int(fp),fn=int(fn),tp=int(tp),alertas=int(pred.sum()),n=len(y))
def wilson(k,n,z=1.95996398454):
    p=k/n;den=1+z*z/n;mid=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [float(mid-half),float(mid+half)]
