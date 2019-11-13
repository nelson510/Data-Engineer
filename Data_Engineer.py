#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 21:25:09 2019

@author: nelson
"""
#import package
import csv
#import numpy as np


header = ["time","bid_price","ask_price","bid_size","ask_size","seq_num"]
#TimeDic contain time as a key and list of "orderid+side" as value 
TimeDic = {}
#oderid+side as key, price and zise as value
PriceDic = {}
#count how many time
previousrow =[]
#currentime = ""
#nexttime =""
iterator = 0
'''
def getbidprice(time):
    #loop and get the highest price of bider
    highprice = 0;
    lowprice = 10000000;
    listofbuy =[]
    listofsell =[]
    listofid = TimeDic.get(time)
    for x in listofid:
        if "BUY" in x:
            listofbuy.append(x)
            
        if "SELL" in x:
            listofsell.append(x)
            
    for x in listofbuy:
        listofP = PriceDic.get(x)
        if float(listofP[0])>highprice:
            highprice=float(listofP[0])
    #get the biggest number 

    for x in listofsell:
        listofP2 = PriceDic.get(x)
        if float(listofP2[0])>lowprice:
            lowprice=float(listofP2[0])
            
    for x in listofsell:
        listofP2 = PriceDic.get(x)
        if float(listofP2[0])<lowprice:
            lowprice = listofP2[0]
    #print(lowprice)
    return highprice,lowprice
'''

def getbidprice():
    #loop and get the highest price of bider
    listofbuy =[]
    listofsell =[]
    highprice = 0
    lowprice = 0
    for x in PriceDic:
        if "BUY" in x:
            listofbuy.append(x)
            
        if "SELL" in x:
            listofsell.append(x)
            
    for x in listofbuy:
        listofP = PriceDic.get(x)
        if float(listofP[0])>highprice:
            highprice=float(listofP[0])
    #get the biggest number 

    for x in listofsell:
        listofP2 = PriceDic.get(x)
        if float(listofP2[0])>lowprice:
            lowprice=float(listofP2[0])
            
    for x in listofsell:
        listofP2 = PriceDic.get(x)
        if float(listofP2[0])<lowprice:
            lowprice = listofP2[0]
    #print(lowprice)
    return highprice,lowprice



def getsize(side,price):   
    BidPriceDic = {}
    SellPriceDic = {}
    for key in PriceDic:
        if "BUY" in key:
            PriceSizeSet= PriceDic.get(key)
            if PriceSizeSet[0] not in BidPriceDic:
                BidPriceDic[PriceSizeSet[0]] = int(PriceSizeSet[1])
            else:
                BidPriceDic[PriceSizeSet[0]]=BidPriceDic.get(PriceSizeSet[0]) + int(PriceSizeSet[1])
            
    for key in PriceDic:
        if "SELL" in key:
            PriceSizeSet2= PriceDic.get(key)
            if PriceSizeSet2[0] not in SellPriceDic:
                SellPriceDic[PriceSizeSet2[0]] = int(PriceSizeSet2[1])
            else:
                SellPriceDic[PriceSizeSet2[0]]=SellPriceDic.get(PriceSizeSet2[0]) + int(PriceSizeSet2[1])
            
    if side == "BUY":
        size = BidPriceDic.get(price)
    elif side == "SELL":
        size = SellPriceDic.get(price)
   
    #print(BidPriceDic)
    return size
        

def rerow(row,writer): 
   
    if row[5] == "1.7976931348623157e+308":
        return True
    if row[5] == "-1.7976931348623157e+308":
        return True
    
    global iterator
    global previousrow
     #final output row
    currentrow = []
    idside = row[3]+row[4];
    #add order id
    if row[3] != '':
        #create data structure
        if row[0] in TimeDic.keys():
            TimeDic[row[0]].append(idside)
        else:
            TimeDic[row[0]] = [idside]     
        if idside not in PriceDic.keys():
            row5 = float(row[5])
            row6 = int(row[6])
            PriceDic[idside] = ([row5,row6])
    #set time
        currentrow.append(row[0])
    #get bestprice
        bestprice,lowprice = getbidprice();
        if bestprice == 0 and iterator != 0:
            bestprice = previousrow[1]
            currentrow.append(bestprice)
        else:
            currentrow.append(bestprice)
    #get lowestprice
        if lowprice == 0 and iterator != 0:
            lowprice = previousrow[2]
            currentrow.append(lowprice)
        else:
            currentrow.append(lowprice)
     #get bidsize   
        bidsize = getsize("BUY",bestprice)
        currentrow.append(bidsize)
     #get sellsize   
        sellsize = getsize("SELL",lowprice)
        currentrow.append(sellsize)
    #get seq
        currentrow.append(row[1])
        if iterator==0:
            previousrow=currentrow
        else:
            if previousrow[0] == row[0]:
                previousrow=currentrow
            if previousrow[0] != row[0]:
                writer.writerow(previousrow)
                previousrow = currentrow
                
                
    if row[8] != '':
        idside = row[8]+row[9]
        modify = PriceDic.get(idside)
        modify[0] = float(row[10])
        modify[1] = int(row[11])
        
        currentrow.append(row[0])
    #get bestprice
        bestprice,lowprice = getbidprice();
        if bestprice == 0 and iterator != 0:
            bestprice = previousrow[1]
            currentrow.append(bestprice)
        else:
            currentrow.append(bestprice)
    #get lowestprice
        if lowprice == 0 and iterator != 0:
            lowprice = previousrow[2]
            currentrow.append(lowprice)
        else:
            currentrow.append(lowprice)
     #get bidsize   
        bidsize = getsize("BUY",bestprice)
        currentrow.append(bidsize)
     #get sellsize   
        sellsize = getsize("SELL",lowprice)
        currentrow.append(sellsize)
    #get seq
        currentrow.append(row[1])
        if iterator==0:
            previousrow=currentrow
        else:
            if previousrow[0] == row[0]:
                previousrow=currentrow
            if previousrow[0] != row[0]:
                writer.writerow(previousrow)
                previousrow = currentrow
                
                
    if row[13] != '':
        idside3 = row[13]+row[14]
        del PriceDic[idside3]
        
        currentrow.append(row[0])
    #get bestprice
        bestprice,lowprice = getbidprice();
        if bestprice == 0 and iterator != 0:
            bestprice = previousrow[1]
            currentrow.append(bestprice)
        else:
            currentrow.append(bestprice)
    #get lowestprice
        if lowprice == 0 and iterator != 0:
            lowprice = previousrow[2]
            currentrow.append(lowprice)
        else:
            currentrow.append(lowprice)
     #get bidsize   
        bidsize = getsize("BUY",bestprice)
        currentrow.append(bidsize)
     #get sellsize   
        sellsize = getsize("SELL",lowprice)
        currentrow.append(sellsize)
    #get seq
        currentrow.append(row[1])
        if iterator==0:
            previousrow=currentrow
        else:
            if previousrow[0] == row[0]:
                previousrow=currentrow
            if previousrow[0] != row[0]:
                writer.writerow(previousrow)
                previousrow = currentrow
     
    
    if (row[15] != '' and row[18] != ''):
        if row[16]=='':
            idside = row[15]+"BUY"
        else:
            idside = row[15]+row[16]
        #print(idside)
        trade = PriceDic.get(idside)
        #print(trade)
        #print(trade)
        if trade[0] == float(row[18]):
            trade[1]= trade[1]-int(row[17])
            if trade[1] == 0:
                del PriceDic[idside]
            
        currentrow.append(row[0])
    #get bestprice
        bestprice,lowprice = getbidprice();
        if bestprice == 0 and iterator != 0:
            bestprice = previousrow[1]
            currentrow.append(bestprice)
        else:
            currentrow.append(bestprice)
    #get lowestprice
        if lowprice == 0 and iterator != 0:
            lowprice = previousrow[2]
            currentrow.append(lowprice)
        else:
            currentrow.append(lowprice)
     #get bidsize   
        bidsize = getsize("BUY",bestprice)
        currentrow.append(bidsize)
     #get sellsize   
        sellsize = getsize("SELL",lowprice)
        currentrow.append(sellsize)
    #get seq
        currentrow.append(row[1])
        if iterator==0:
            previousrow=currentrow
        else:
            if previousrow[0] == row[0]:
                previousrow=currentrow
            if previousrow[0] != row[0]:
                writer.writerow(previousrow)
                previousrow = currentrow 
            
    iterator=iterator+1
    
    
        #print(finalcurrentrow[0])
        
        
        
        
  
        
        
   # print(TimeDic)
   # print(PriceDic)
    
    
    
with open("market_data.csv","r") as infile, open("Result.csv", "w") as outfile:
   rows = csv.reader(infile)
   writer = csv.writer(outfile)
   next(rows)  # skip the headers
   writer.writerow(header) #write the headers
   #print(next(rows)[0])
       
   for row in rows:
      rerow(row,writer)
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      
    
