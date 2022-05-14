import numpy as np
import scipy.stats as sps
import pandas as pd

# метод cuped для повышения чувствительности
def cuped(metric, covariate):
    
    #находим значение тета
    theta = metric.cov(covariate) / covariate.var()
    
    #находим cuped метрику
    cuped_metric = metric -  theta * (covariate - covariate.mean()) 
    
    return cuped_metric
    
    
class Tester(object):
    """
    Attributes:
    -----------
    control_data : pandas.DataFrame 
        таблица данных контрольной группы
    test_data : pandas.DataFrame 
        таблица данных тестовой группы 
    metrics : str
        целевая метрика
    sgn_lev: float 
        уровень значимости
        
    Methods:
    ---------
    effect()
        рассчитывает эффект ab-теста
    """
    
    def __init__(self, control_data, test_data, metrics, sgn_lev=0.05):
        
        self.control_data = control_data
        self.test_data = test_data
        self.metrics = metrics
        self.sgn_lev = sgn_lev 
        
    def effect(self, ):
        res = {} 
        res["effect_value"] = (self.test_data[self.metrics].mean() 
                              / self.control_data[self.metrics].mean() - 1)
        
        #находим p-value с помощью t-test
        _, p_val = sps.ttest_ind(self.control_data[self.metrics].values,
                                       self.test_data[self.metrics].values,
                                       equal_var=False)  
        #определим статистическую значимость 
        res["statistically significant"] = (p_val <= self.sgn_lev)
        
        return res     
    
        