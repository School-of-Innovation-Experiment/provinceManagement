# coding: UTF-8
'''
Created on 2013-3-30

@author: sytmac
'''

def DateFormatTransfer(date_string):
    '''
    from mm/dd/yyyy to yyyy-mm-dd
    '''
    yy = date_string.split('/')[-1]
    mm = date_string.split('/')[0]
    dd = date_string.split('/')[1]
    
    return yy+'-'+mm+'-'+dd