from tkinter import*
import pandas as pd
import random
import os
import time;
import csv
import numpy as np
import matplotlib.pyplot as plt

file="database.csv"
def res():
    global ho,aw,hom1,draw1,awy1,ggg1,ng,ove1,und1
    ho=0
    aw=0
    hom1=0
    draw1=0
    awy1=0
    ggg1=0
    ng=0
    ove1=0
    und1=0
    


data=pd.read_csv("index5.csv")
datatt="index5.csv"




global hom1,draw1,awy1,ove1,und1,ggg1,ng

#reading the data without any null value
data=data[["B365H","B365D","B365A","FTHG","FTAG"]]
#print(data.head())
def factorial(k):
    fact=1
    for i in range(1,k+1):
        fact=fact*i
    return fact
def poisson(l,k):
    upper=(l**k)*np.exp(-l)
    lower=factorial(k)
    return (upper/lower)

def search(x1,x2,df):
    global hom1,draw1,awy1,ove1,und1,ggg1,ng
    data1=df.loc[(df['B365H']<=x1+0.001)&(df['B365H']>=x1-0.001)&(df['B365A']<=x2+0.001)&(df['B365A']>=x2-0.001)]
    
    leng=len(data1)
    #print("total now",leng)
    mm="prediction.txt"
    
    
    if(leng>=1):
        
        meanh=data1["FTHG"].mean()
        meanA=data1["FTAG"].mean()
        h0=poisson(meanh,0)
        h1=poisson(meanh,1)
        h2=poisson(meanh,2)
        h3=poisson(meanh,3)
        h4=poisson(meanh,4)
        h5=poisson(meanh,5)
        #print(h0+h2+h3+h4+h5)
        a0=poisson(meanA,0)
        a1=poisson(meanA,1)
        a2=poisson(meanA,2)
        a3=poisson(meanA,3)
        a4=poisson(meanA,4)
        a5=poisson(meanA,5)
        #print(a0+a1+a2+a3+a4+a5)

        #cal culating home chance
        h1_chance=(h1*a0)
        h2_chance=(h2*a0)+(h2*a1)
        h3_chance=(h3*a0)+(h3*a1)+(h3*a2)
        h4_chance=(h4*a0)+(h4*a1)+(h4*a2)+(h4*a3)
        h5_chance=(h5*a0)+(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)
        home_chance=round(h1_chance+h2_chance+h3_chance+h4_chance+h5_chance,3)
        #print("the home chance is",home_chance)
        #calculating the away chance
        a1_chance=(a1*h0)
        a2_chance=(a2*h0)+(a2*h1)
        a3_chance=(a3*h0)+(a3*h1)+(a3*h2)
        a4_chance=(a4*h0)+(a4*h1)+(a4*h2)+(a4*h3)
        a5_chance=(a5*h0)+(a5*h1)+(a5*h2)+(a5*h3)
        away_chance=round(a1_chance+a2_chance+a3_chance+a4_chance+a5_chance,3)
    
    
        #print("the away chance is",away_chance)    
        #calculate the values of draws
        draw=round((h0*a0)+(h1*a1)+(h2*a2)+(h3*a3)+(h4*a4)+(h5*a5),3)
        #print("the draw is",draw)
        slices=[home_chance,draw,away_chance]
        cols=['b','r','g']
        my_l=['home','draw','away']
        plt.pie(slices,labels=my_l,colors=cols,startangle=4,autopct='%1.1f%%' )
        plt.legend(loc=4)
    
        #plt.show()

        total=(draw+home_chance+away_chance)
        #print("the sum total is",total)
        #calculate the over
        h0_over=(h0*a3)+(h0*a4)+(h0*a5)
        h1_over=(h1*a2)+(h1*a3)+(h1*a4)+(h1*a5)
        h2_over=(h2*a1)+(h2*a2)+(h2*a3)+(h2*a4)+(h2*a5)
        h3_over=(h3*a0)+(h3*a1)+(h3*a2)+(h3*a3)+(h3*a4)+(h3*a5)
        h4_over=(h4*a0)+(h4*a1)+(h4*a2)+(h4*a3)+(h4*a4)+(h4*a5)
        h5_over=(h5*a0)+(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)+(h5*a5)
        over=round(h0_over+h1_over+h2_over+h3_over+h4_over+h5_over,3)
        under=round(total-over,3)
        #print("over under",over,under)
        slices=[over,under]
        cols=['b','r']
        my_l=['over','under']
        plt.pie(slices,labels=my_l,colors=cols,startangle=4,autopct='%1.1f%%' )
        plt.legend(loc=4)
    
        #plt.show()
        #calculating the goal goals
        g1=(h1*a1)+(h1*a2)+(h1*a3)+(h1*a4)+(h1*a5)
        g2=(h2*a1)+(h2*a2)+(h2*a3)+(h2*a4)+(h2*a5)
        g3=(h3*a1)+(h3*a2)+(h3*a3)+(h3*a4)+(h3*a5)
        g4=(h4*a1)+(h4*a2)+(h4*a3)+(h4*a4)+(h4*a5)
        g5=(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)+(h5*a5)
        goal_goal=round(g1+g2+g3+g4+g5,3)
        no_goal=round((total-goal_goal),3)
        #print("goal goal no goal goal",goal_goal,no_goal)
        data_home=data1.loc[data1["FTHG"]>data1["FTAG"]]
        hom1=round((len(data_home)/leng),3)
        data_draw=data1.loc[data1["FTHG"]==data1["FTAG"]]
        draw1=round((len(data_draw)/leng),3)
        data_away=data1.loc[data1["FTHG"]<data1["FTAG"]]
        awy1=round((len(data_away)/leng),3)
        data_over=data1.loc[(data1["FTHG"]+data1["FTAG"])>2.5]
        ove1=round((len(data_over)/leng),3)
        data_under=data1.loc[(data1["FTHG"]+data1["FTAG"])<2.5]
        und1=round((len(data_under)/leng),3)
        data_gg=data1.loc[(data1["FTHG"]>0)&(data1["FTAG"]>0)]
        ggg1=round((len(data_gg)/leng),3)
        
        ng=round((1-ggg1),3)
        #print("the home is",hom1,draw1,awy1,ove1,und1,ggg1,ng)
        h11=(home_chance/total)
        d11=(draw/total)
        a11=(away_chance/total)
        g11=(goal_goal/total)
        ng11=(no_goal/total)
        over11=(over/total)
        under11=(under/total)
        hh22=(h11+hom1)/2
        dd22=(d11+draw1)/2
        aa22=(a11+awy1)/2
        gg22=(g11+ggg1)/2
        ng22=(ng11+ng)/2
        over22=(over11+ove1)/2
        under22=(under11+und1)/2
        # creating a canvas
        '''def prop(n):
            return 360*n
        
        c1=Canvas(f,width=500,height=400)
        c1.pack( fill=BOTH,expand=True)
        c=Canvas(c1,width=150,height=100)
        c.pack(side=LEFT)
        
        c.create_arc((1,1,50,90),fill="red",outline="blue",start=prop(0),extent=prop(hh22))
        c.create_arc((2,2,50,90),fill="pink",outline="blue",start=prop(hh22),extent=prop(dd22))
        c.create_arc((2,2,50,90),fill="green",outline="blue",start=prop(hh22+dd22),extent=prop(aa22))
        c.create_text(90,10,text="red:Home")
        c.pack()
        c.create_text(90,50,text="pink:Draw")
        c.pack()
        c.create_text(90,70,text="Green:Away")
        c.pack()
        
        
        
        c=Canvas(c1,width=150,height=100)
        c.pack(side=LEFT ,expand=True)
        c.create_arc((1,1,50,90),fill="red",outline="blue",start=prop(0),extent=prop(over22))
        c.create_arc((1,1,50,90),fill="pink",outline="blue",start=prop(over22),extent=prop(under22))
        
        c.create_text(90,10,text="red:over")
        c.pack()
        c.create_text(90,50,text="pink:under")
        c.pack()
        
        
        
        c=Canvas(c1,width=150,height=100)
        c.pack(side=LEFT)
        c.create_arc((1,1,50,90),fill="#00FFFF",outline="blue",start=prop(0),extent=prop(gg22))
        c.create_arc((1,1,50,90),fill="pink",outline="blue",start=prop(gg22),extent=prop(ng22))
        
        c.create_text(90,10,text="AQua:BTS" )
        c.pack()
        c.create_text(90,50,text="No GG")
        c.pack()'''
        mm="prediction.txt"
        
        try:
       
            with open(mm,"w") as m:
                 m.write("\t home\t"+"draw\t"+"away\n")
                 m.write("\t"+str(round(hh22,2))+"\t")
                 m.write(str(round(dd22,2))+"\t")
                 m.write(str(round(aa22,2))+"\t\n")
                 m.write("\t goal goal\t"+"no goal goal\n")
                 m.write("\t"+str(round(gg22,2))+"\t\t")
                 m.write(str(round(ng22,2))+"\n")
                 m.write("\t *****OVER UNDER 2.5******\n")
                 m.write("\t OVER2.5\t"+"UNDER2.5\n")
                 m.write("\t"+str(round(over22,2))+"\t")
                 m.write(str(round(under22,2))+"\n")
                 m.write(" the total combination are"+str(leng)+"\t count"+"\n")
                 #print("done")
            m.close()
            
        except:
        
            with open(mm,"a+") as m:
                m.write ("/t")
            m.close()
            
    else:
        #print("the combination is small")
        with open(mm,"w") as m:
            m.write ("there is no cobination of that kind")
        m.close()
    return [round(hh22,2),round(dd22,2),round(aa22,2),round(gg22,2),round(ng22,2),round(over22,2),round(under22,2)]
def search_hd(x1,x2,df):
    global hom1,draw1,awy1,ove1,und1,ggg1,ng
    data1=df.loc[(df['B365H']<=x1+0.001)&(df['B365H']>=x1-0.001)&(df['B365D']<=x2+0.001)&(df['B365D']>=x2-0.001)]
    
    leng=len(data1)
    #print("total now",leng)
    mm="prediction.txt"
    
    
    if(leng>=1):
        
        meanh=data1["FTHG"].mean()
        meanA=data1["FTAG"].mean()
        h0=poisson(meanh,0)
        h1=poisson(meanh,1)
        h2=poisson(meanh,2)
        h3=poisson(meanh,3)
        h4=poisson(meanh,4)
        h5=poisson(meanh,5)
        #print(h0+h2+h3+h4+h5)
        a0=poisson(meanA,0)
        a1=poisson(meanA,1)
        a2=poisson(meanA,2)
        a3=poisson(meanA,3)
        a4=poisson(meanA,4)
        a5=poisson(meanA,5)
        #print(a0+a1+a2+a3+a4+a5)

        #cal culating home chance
        h1_chance=(h1*a0)
        h2_chance=(h2*a0)+(h2*a1)
        h3_chance=(h3*a0)+(h3*a1)+(h3*a2)
        h4_chance=(h4*a0)+(h4*a1)+(h4*a2)+(h4*a3)
        h5_chance=(h5*a0)+(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)
        home_chance=round(h1_chance+h2_chance+h3_chance+h4_chance+h5_chance,3)
        #print("the home chance is",home_chance)
        #calculating the away chance
        a1_chance=(a1*h0)
        a2_chance=(a2*h0)+(a2*h1)
        a3_chance=(a3*h0)+(a3*h1)+(a3*h2)
        a4_chance=(a4*h0)+(a4*h1)+(a4*h2)+(a4*h3)
        a5_chance=(a5*h0)+(a5*h1)+(a5*h2)+(a5*h3)
        away_chance=round(a1_chance+a2_chance+a3_chance+a4_chance+a5_chance,3)
    
    
        #print("the away chance is",away_chance)    
        #calculate the values of draws
        draw=round((h0*a0)+(h1*a1)+(h2*a2)+(h3*a3)+(h4*a4)+(h5*a5),3)
        #print("the draw is",draw)
        slices=[home_chance,draw,away_chance]
        cols=['b','r','g']
        my_l=['home','draw','away']
        plt.pie(slices,labels=my_l,colors=cols,startangle=4,autopct='%1.1f%%' )
        plt.legend(loc=4)
    
        #plt.show()

        total=(draw+home_chance+away_chance)
        #print("the sum total is",total)
        #calculate the over
        h0_over=(h0*a3)+(h0*a4)+(h0*a5)
        h1_over=(h1*a2)+(h1*a3)+(h1*a4)+(h1*a5)
        h2_over=(h2*a1)+(h2*a2)+(h2*a3)+(h2*a4)+(h2*a5)
        h3_over=(h3*a0)+(h3*a1)+(h3*a2)+(h3*a3)+(h3*a4)+(h3*a5)
        h4_over=(h4*a0)+(h4*a1)+(h4*a2)+(h4*a3)+(h4*a4)+(h4*a5)
        h5_over=(h5*a0)+(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)+(h5*a5)
        over=round(h0_over+h1_over+h2_over+h3_over+h4_over+h5_over,3)
        under=round(total-over,3)
        #print("over under",over,under)
        slices=[over,under]
        cols=['b','r']
        my_l=['over','under']
        plt.pie(slices,labels=my_l,colors=cols,startangle=4,autopct='%1.1f%%' )
        plt.legend(loc=4)
    
        #plt.show()
        #calculating the goal goals
        g1=(h1*a1)+(h1*a2)+(h1*a3)+(h1*a4)+(h1*a5)
        g2=(h2*a1)+(h2*a2)+(h2*a3)+(h2*a4)+(h2*a5)
        g3=(h3*a1)+(h3*a2)+(h3*a3)+(h3*a4)+(h3*a5)
        g4=(h4*a1)+(h4*a2)+(h4*a3)+(h4*a4)+(h4*a5)
        g5=(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)+(h5*a5)
        goal_goal=round(g1+g2+g3+g4+g5,3)
        no_goal=round((total-goal_goal),3)
        #print("goal goal no goal goal",goal_goal,no_goal)
        data_home=data1.loc[data1["FTHG"]>data1["FTAG"]]
        hom1=round((len(data_home)/leng),3)
        data_draw=data1.loc[data1["FTHG"]==data1["FTAG"]]
        draw1=round((len(data_draw)/leng),3)
        data_away=data1.loc[data1["FTHG"]<data1["FTAG"]]
        awy1=round((len(data_away)/leng),3)
        data_over=data1.loc[(data1["FTHG"]+data1["FTAG"])>2.5]
        ove1=round((len(data_over)/leng),3)
        data_under=data1.loc[(data1["FTHG"]+data1["FTAG"])<2.5]
        und1=round((len(data_under)/leng),3)
        data_gg=data1.loc[(data1["FTHG"]>0)&(data1["FTAG"]>0)]
        ggg1=round((len(data_gg)/leng),3)
        
        ng=round((1-ggg1),3)
        #print("the home is",hom1,draw1,awy1,ove1,und1,ggg1,ng)
        h11=(home_chance/total)
        d11=(draw/total)
        a11=(away_chance/total)
        g11=(goal_goal/total)
        ng11=(no_goal/total)
        over11=(over/total)
        under11=(under/total)
        hh22=(h11+hom1)/2
        dd22=(d11+draw1)/2
        aa22=(a11+awy1)/2
        gg22=(g11+ggg1)/2
        ng22=(ng11+ng)/2
        over22=(over11+ove1)/2
        under22=(under11+und1)/2
        
        mm="prediction.txt"
        try:
       
            with open(mm,"a+") as m:
                 m.write("\t home draw \n \t home\t"+"draw\t"+"away\n")
                 m.write("\t"+str(round(hh22,2))+"\t")
                 m.write(str(round(dd22,2))+"\t")
                 m.write(str(round(aa22,2))+"\t\n")
                 m.write("\t goal goal\t"+"no goal goal\n")
                 m.write("\t"+str(round(gg22,2))+"\t\t")
                 m.write(str(round(ng22,2))+"\n")
                 m.write("\t *****OVER UNDER 2.5******\n")
                 m.write("\t OVER2.5\t"+"UNDER2.5\n")
                 m.write("\t"+str(round(over22,2))+"\t")
                 m.write(str(round(under22,2))+"\n")
                 m.write(" the total combination are"+str(leng)+"\t count"+"\n")
                 #print("done")
            m.close()
        except:
        
            with open(mm,"a+") as m:
                m.write ("/t")
            m.close()
    else:
        #print("the combination is small")
        with open(mm,"w") as m:
            m.write ("there is no cobination of that kind")
        m.close()
    return [round(hh22,2),round(dd22,2),round(aa22,2),round(gg22,2),round(ng22,2),round(over22,2),round(under22,2)]
def search_ad(x1,x2,df):
    global hom1,draw1,awy1,ove1,und1,ggg1,ng
    data1=df.loc[(df['B365A']<=x1+0.001)&(df['B365A']>=x1-0.001)&(df['B365D']<=x2+0.001)&(df['B365D']>=x2-0.001)]
    
    leng=len(data1)
    #print("total now",leng)
    mm="prediction.txt"
    
    
    if(leng>=1):
        
        meanh=data1["FTHG"].mean()
        meanA=data1["FTAG"].mean()
        h0=poisson(meanh,0)
        h1=poisson(meanh,1)
        h2=poisson(meanh,2)
        h3=poisson(meanh,3)
        h4=poisson(meanh,4)
        h5=poisson(meanh,5)
        #print(h0+h2+h3+h4+h5)
        a0=poisson(meanA,0)
        a1=poisson(meanA,1)
        a2=poisson(meanA,2)
        a3=poisson(meanA,3)
        a4=poisson(meanA,4)
        a5=poisson(meanA,5)
        #print(a0+a1+a2+a3+a4+a5)

        #cal culating home chance
        h1_chance=(h1*a0)
        h2_chance=(h2*a0)+(h2*a1)
        h3_chance=(h3*a0)+(h3*a1)+(h3*a2)
        h4_chance=(h4*a0)+(h4*a1)+(h4*a2)+(h4*a3)
        h5_chance=(h5*a0)+(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)
        home_chance=round(h1_chance+h2_chance+h3_chance+h4_chance+h5_chance,3)
        #print("the home chance is",home_chance)
        #calculating the away chance
        a1_chance=(a1*h0)
        a2_chance=(a2*h0)+(a2*h1)
        a3_chance=(a3*h0)+(a3*h1)+(a3*h2)
        a4_chance=(a4*h0)+(a4*h1)+(a4*h2)+(a4*h3)
        a5_chance=(a5*h0)+(a5*h1)+(a5*h2)+(a5*h3)
        away_chance=round(a1_chance+a2_chance+a3_chance+a4_chance+a5_chance,3)
    
    
        #print("the away chance is",away_chance)    
        #calculate the values of draws
        draw=round((h0*a0)+(h1*a1)+(h2*a2)+(h3*a3)+(h4*a4)+(h5*a5),3)
        #print("the draw is",draw)
        slices=[home_chance,draw,away_chance]
        cols=['b','r','g']
        my_l=['home','draw','away']
        plt.pie(slices,labels=my_l,colors=cols,startangle=4,autopct='%1.1f%%' )
        plt.legend(loc=4)
    
        #plt.show()

        total=(draw+home_chance+away_chance)
        #print("the sum total is",total)
        #calculate the over
        h0_over=(h0*a3)+(h0*a4)+(h0*a5)
        h1_over=(h1*a2)+(h1*a3)+(h1*a4)+(h1*a5)
        h2_over=(h2*a1)+(h2*a2)+(h2*a3)+(h2*a4)+(h2*a5)
        h3_over=(h3*a0)+(h3*a1)+(h3*a2)+(h3*a3)+(h3*a4)+(h3*a5)
        h4_over=(h4*a0)+(h4*a1)+(h4*a2)+(h4*a3)+(h4*a4)+(h4*a5)
        h5_over=(h5*a0)+(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)+(h5*a5)
        over=round(h0_over+h1_over+h2_over+h3_over+h4_over+h5_over,3)
        under=round(total-over,3)
        #print("over under",over,under)
        slices=[over,under]
        cols=['b','r']
        my_l=['over','under']
        plt.pie(slices,labels=my_l,colors=cols,startangle=4,autopct='%1.1f%%' )
        plt.legend(loc=4)
    
        #plt.show()
        #calculating the goal goals
        g1=(h1*a1)+(h1*a2)+(h1*a3)+(h1*a4)+(h1*a5)
        g2=(h2*a1)+(h2*a2)+(h2*a3)+(h2*a4)+(h2*a5)
        g3=(h3*a1)+(h3*a2)+(h3*a3)+(h3*a4)+(h3*a5)
        g4=(h4*a1)+(h4*a2)+(h4*a3)+(h4*a4)+(h4*a5)
        g5=(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)+(h5*a5)
        goal_goal=round(g1+g2+g3+g4+g5,3)
        no_goal=round((total-goal_goal),3)
        #print("goal goal no goal goal",goal_goal,no_goal)
        data_home=data1.loc[data1["FTHG"]>data1["FTAG"]]
        hom1=round((len(data_home)/leng),3)
        data_draw=data1.loc[data1["FTHG"]==data1["FTAG"]]
        draw1=round((len(data_draw)/leng),3)
        data_away=data1.loc[data1["FTHG"]<data1["FTAG"]]
        awy1=round((len(data_away)/leng),3)
        data_over=data1.loc[(data1["FTHG"]+data1["FTAG"])>2.5]
        ove1=round((len(data_over)/leng),3)
        data_under=data1.loc[(data1["FTHG"]+data1["FTAG"])<2.5]
        und1=round((len(data_under)/leng),3)
        data_gg=data1.loc[(data1["FTHG"]>0)&(data1["FTAG"]>0)]
        ggg1=round((len(data_gg)/leng),3)
        
        ng=round((1-ggg1),3)
        #print("the home is",hom1,draw1,awy1,ove1,und1,ggg1,ng)
        h11=(home_chance/total)
        d11=(draw/total)
        a11=(away_chance/total)
        g11=(goal_goal/total)
        ng11=(no_goal/total)
        over11=(over/total)
        under11=(under/total)
        hh22=(h11+hom1)/2
        dd22=(d11+draw1)/2
        aa22=(a11+awy1)/2
        gg22=(g11+ggg1)/2
        ng22=(ng11+ng)/2
        over22=(over11+ove1)/2
        under22=(under11+und1)/2
        
        mm="prediction.txt"
        try:
       
            with open(mm,"a+") as m:
                 m.write("\t away draw \n \t home\t"+"draw\t"+"away\n")
                 m.write("\t"+str(round(hh22,2))+"\t")
                 m.write(str(round(dd22,2))+"\t")
                 m.write(str(round(aa22,2))+"\t\n")
                 m.write("\t goal goal\t"+"no goal goal\n")
                 m.write("\t"+str(round(gg22,2))+"\t\t")
                 m.write(str(round(ng22,2))+"\n")
                 m.write("\t *****OVER UNDER 2.5******\n")
                 m.write("\t OVER2.5\t"+"UNDER2.5\n")
                 m.write("\t"+str(round(over22,2))+"\t")
                 m.write(str(round(under22,2))+"\n")
                 m.write(" the total combination are"+str(leng)+"\t count"+"\n")
                 #print("done")
            m.close()
        except:
        
            with open(mm,"a+") as m:
                m.write ("/t")
            m.close()
    else:
        #print("the combination is small")
        with open(mm,"w") as m:
            m.write ("there is no cobination of that kind")
        m.close()
    return [round(hh22,2),round(dd22,2),round(aa22,2),round(gg22,2),round(ng22,2),round(over22,2),round(under22,2)]

def search2(x1,d1,x2,df):
    global hom1,draw1,awy1,ove1,und1,ggg1,ng
    data1=df.loc[(df['B365H']<=x1+0.001)&(df['B365H']>=x1-0.001)&(df['B365D']<=d1+0.001)&(df['B365D']>=d1-0.001)&(df['B365A']<=x2+0.001)&(df['B365A']>=x2-0.001)]
    
    leng=len(data1)
    #print("total now",leng)
    mm="prediction.txt"
    
    
    if(leng>=1):
        
        meanh=data1["FTHG"].mean()
        meanA=data1["FTAG"].mean()
        h0=poisson(meanh,0)
        h1=poisson(meanh,1)
        h2=poisson(meanh,2)
        h3=poisson(meanh,3)
        h4=poisson(meanh,4)
        h5=poisson(meanh,5)
        #print(h0+h2+h3+h4+h5)
        a0=poisson(meanA,0)
        a1=poisson(meanA,1)
        a2=poisson(meanA,2)
        a3=poisson(meanA,3)
        a4=poisson(meanA,4)
        a5=poisson(meanA,5)
        #print(a0+a1+a2+a3+a4+a5)

        #cal culating home chance
        h1_chance=(h1*a0)
        h2_chance=(h2*a0)+(h2*a1)
        h3_chance=(h3*a0)+(h3*a1)+(h3*a2)
        h4_chance=(h4*a0)+(h4*a1)+(h4*a2)+(h4*a3)
        h5_chance=(h5*a0)+(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)
        home_chance=round(h1_chance+h2_chance+h3_chance+h4_chance+h5_chance,3)
        #print("the home chance is",home_chance)
        #calculating the away chance
        a1_chance=(a1*h0)
        a2_chance=(a2*h0)+(a2*h1)
        a3_chance=(a3*h0)+(a3*h1)+(a3*h2)
        a4_chance=(a4*h0)+(a4*h1)+(a4*h2)+(a4*h3)
        a5_chance=(a5*h0)+(a5*h1)+(a5*h2)+(a5*h3)
        away_chance=round(a1_chance+a2_chance+a3_chance+a4_chance+a5_chance,3)
    
    
        #print("the away chance is",away_chance)    
        #calculate the values of draws
        draw=round((h0*a0)+(h1*a1)+(h2*a2)+(h3*a3)+(h4*a4)+(h5*a5),3)
        #print("the draw is",draw)
        slices=[home_chance,draw,away_chance]
        cols=['b','r','g']
        my_l=['home','draw','away']
        plt.pie(slices,labels=my_l,colors=cols,startangle=4,autopct='%1.1f%%' )
        plt.legend(loc=4)
    
        #plt.show()

        total=(draw+home_chance+away_chance)
        #print("the sum total is",total)
        #calculate the over
        h0_over=(h0*a3)+(h0*a4)+(h0*a5)
        h1_over=(h1*a2)+(h1*a3)+(h1*a4)+(h1*a5)
        h2_over=(h2*a1)+(h2*a2)+(h2*a3)+(h2*a4)+(h2*a5)
        h3_over=(h3*a0)+(h3*a1)+(h3*a2)+(h3*a3)+(h3*a4)+(h3*a5)
        h4_over=(h4*a0)+(h4*a1)+(h4*a2)+(h4*a3)+(h4*a4)+(h4*a5)
        h5_over=(h5*a0)+(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)+(h5*a5)
        over=round(h0_over+h1_over+h2_over+h3_over+h4_over+h5_over,3)
        under=round(total-over,3)
        #print("over under",over,under)
        slices=[over,under]
        cols=['b','r']
        my_l=['over','under']
        plt.pie(slices,labels=my_l,colors=cols,startangle=4,autopct='%1.1f%%' )
        plt.legend(loc=4)
    
        #plt.show()
        #calculating the goal goals
        g1=(h1*a1)+(h1*a2)+(h1*a3)+(h1*a4)+(h1*a5)
        g2=(h2*a1)+(h2*a2)+(h2*a3)+(h2*a4)+(h2*a5)
        g3=(h3*a1)+(h3*a2)+(h3*a3)+(h3*a4)+(h3*a5)
        g4=(h4*a1)+(h4*a2)+(h4*a3)+(h4*a4)+(h4*a5)
        g5=(h5*a1)+(h5*a2)+(h5*a3)+(h5*a4)+(h5*a5)
        goal_goal=round(g1+g2+g3+g4+g5,3)
        no_goal=round((total-goal_goal),3)
        #print("goal goal no goal goal",goal_goal,no_goal)
        data_home=data1.loc[data1["FTHG"]>data1["FTAG"]]
        hom1=round((len(data_home)/leng),3)
        data_draw=data1.loc[data1["FTHG"]==data1["FTAG"]]
        draw1=round((len(data_draw)/leng),3)
        data_away=data1.loc[data1["FTHG"]<data1["FTAG"]]
        awy1=round((len(data_away)/leng),3)
        data_over=data1.loc[(data1["FTHG"]+data1["FTAG"])>2.5]
        ove1=round((len(data_over)/leng),3)
        data_under=data1.loc[(data1["FTHG"]+data1["FTAG"])<2.5]
        und1=round((len(data_under)/leng),3)
        data_gg=data1.loc[(data1["FTHG"]>0)&(data1["FTAG"]>0)]
        ggg1=round((len(data_gg)/leng),3)
        
        ng=round((1-ggg1),3)
        #print("the home is",hom1,draw1,awy1,ove1,und1,ggg1,ng)
        h11=(home_chance/total)
        d11=(draw/total)
        a11=(away_chance/total)
        g11=(goal_goal/total)
        ng11=(no_goal/total)
        over11=(over/total)
        under11=(under/total)
        hh22=(h11+hom1)/2
        dd22=(d11+draw1)/2
        aa22=(a11+awy1)/2
        gg22=(g11+ggg1)/2
        ng22=(ng11+ng)/2
        over22=(over11+ove1)/2
        under22=(under11+und1)/2
        # creating a canvas
        
        mm="prediction.txt"
        try:
       
            with open(mm,"a+") as m:
                 m.write("\n \t\t All odds\n\t home\t"+"draw\t"+"away\n")
                 m.write("\t"+str(round(hh22,2))+"\t")
                 m.write(str(round(dd22,2))+"\t")
                 m.write(str(round(aa22,2))+"\t\n")
                 m.write("\t goal goal\t"+"no goal goal\n")
                 m.write("\t"+str(round(gg22,2))+"\t\t")
                 m.write(str(round(ng22,2))+"\n")
                 m.write("\t *****OVER UNDER 2.5******\n")
                 m.write("\t OVER2.5\t"+"UNDER2.5\n")
                 m.write("\t"+str(round(over22,2))+"\t")
                 m.write(str(round(under22,2))+"\n")
                 m.write(" the total combination are"+str(leng)+"\t count"+"\n")
                 #print("done")
            m.close()
        except:
        
            with open(mm,"a+") as m:
                m.write ("/t")
            m.close()
    else:
        #print("the combination is small")
        with open(mm,"a+") as m:
            m.write ("there is no cobination of that kind")
        m.close()

    return [round(hh22,2),round(dd22,2),round(aa22,2),round(gg22,2),round(ng22,2),round(over22,2),round(under22,2)]

root=Tk()
root.geometry("800x700+250+10")
root.title("POISSION DISTRIBUTION BY Jackmangichui@gmail.com")
Tops=Frame(root,width=1000,height=200,bg="#FF1493",relief=RAISED)
Tops.pack(side=TOP,padx=4,pady=5)
label=Label(Tops,font=('arial',15,'bold'),text="Home Odds")
label.grid(row=0,column=0)
label=Label(Tops,font=('arial',15,'bold'),text="Draw Odds")
label.grid(row=0,column=1)
label=Label(Tops,font=('arial',15,'bold'),text="Away Odds")
label.grid(row=0,column=2)
f=Frame(root,width=800,height=620,bg="#DCDCDC",relief=SUNKEN)
f.pack(padx=4,pady=5)
def main():
    # creating the frames
    global hom1,draw1,awy1,ove1,und1,ggg1,ng
    res()
    

    data5="odd"+".csv"
    '''with open(data5) as k:
        data1=k.readlines()
        #data1.split("\n")
        datak=list(data1)
        print("data",datak)'''
    datak=['1.06\n', '1.07\n', '1.08\n', '1.09\n', '1.1\n', '1.11\n', '1.12\n', '1.13\n', '1.14\n', '1.16\n', '1.17\n', '1.18\n', '1.19\n', '1.2\n', '1.22\n', '1.25\n', '1.28\n', '1.29\n', '1.3\n', '1.33\n', '1.35\n', '1.36\n', '1.39\n', '1.4\n', '1.44\n', '1.45\n', '1.48\n', '1.5\n', '1.53\n', '1.55\n', '1.57\n', '1.6\n', '1.61\n', '1.62\n', '1.64\n', '1.65\n', '1.66\n', '1.67\n', '1.7\n', '1.72\n', '1.73\n', '1.75\n', '1.8\n', '1.83\n', '1.85\n', '1.89\n', '1.9\n', '1.91\n', '1.95\n', '2\n', '2.04\n', '2.05\n', '2.1\n', '2.14\n', '2.15\n', '2.2\n', '2.25\n', '2.29\n', '2.3\n', '2.35\n', '2.37\n', '2.38\n', '2.39\n', '2.4\n', '2.45\n', '2.5\n', '2.54\n', '2.55\n', '2.6\n', '2.62\n', '2.63\n', '2.65\n', '2.7\n', '2.75\n', '2.79\n', '2.8\n', '2.87\n', '2.88\n', '2.89\n', '2.9\n', '2.95\n', '3\n', '3.1\n', '3.2\n', '3.25\n', '3.29\n', '3.3\n', '3.39\n', '3.4\n', '3.5\n', '3.6\n', '3.75\n', '3.79\n', '3.8\n', '3.9\n', '4\n', '4.1\n', '4.2\n', '4.33\n', '4.4\n', '4.5\n', '4.6\n', '4.75\n', '4.8\n', '4.9\n', '5\n', '5.25\n', '5.5\n', '5.75\n', '5.8\n', '6\n', '6.25\n', '6.5\n', '7\n', '7.5\n', '8\n', '8.5\n', '9\n', '9.5\n', '10\n', '11\n', '12\n', '13\n', '14\n', '15\n', '17\n', '19\n', '21\n', '23\n']

    lst=StringVar()
    lst1=StringVar()
    lst2=StringVar()
    lst3=StringVar()

    lst2.set(datak[50])
    lst3.set(datak[80])
    lst1.set(datak[90])

    selectI=OptionMenu(Tops,lst2,*datak)
    selectI.grid(row=1,column=0)
    selectI=OptionMenu(Tops,lst1,*datak)
    selectI.grid(row=1,column=1)
    selectI=OptionMenu(Tops,lst3,*datak)
    selectI.grid(row=1,column=2)

    def exit1():
        root.destroy()
    def reset():
        for wid in f.winfo_children():
                wid.destroy()
    def reset_win():
        for wid in root.winfo_children():
                wid.destroy()
        Tops=Frame(root,width=1000,height=200,bg="#FF1493",relief=RAISED)
        Tops.pack(side=TOP,padx=4,pady=5)
        label=Label(Tops,font=('arial',15,'bold'),text="Home1 Odds")
        label.grid(row=1,column=0)
        label=Label(Tops,font=('arial',15,'bold'),text="Draw Odds")
        label.grid(row=1,column=1)
        label=Label(Tops,font=('arial',15,'bold'),text="Away Odds")
        label.grid(row=1,column=2)
        f=Frame(root,width=800,height=620,bg="#DCDCDC",relief=SUNKEN)
        f.pack(padx=4,pady=5)
        mm="help.txt"
        
        scroll = Scrollbar(f)
        scroll.pack(side=LEFT,fill=Y)
        text = Text(f, font=('bold'),height=26, width=165,fg="#000000",bg="#DCDCDC",yscrollcommand=scroll.set)
        
        with open(mm) as j:
            data1=j.readlines()
            for row in data1:
                text.insert(END,row)

        j.close()
        
        text.pack()
        scroll.config(command=text.yview)

        

    
        btreset=Button(Tops,padx=3,pady=1,bd=10,fg="black",font=('arial',12,'bold'),width=5,text="EXIT",bg="#32cd32",command=exit1).grid(row=0,column=3)
    
        btreset=Button(Tops,padx=3,pady=1,bd=10,fg="black",font=('arial',12,'bold'),width=5,text="HOME",bg="#32cd32",command=exit1).grid(row=0,column=2)
    
    def submit():
    
        var5=lst2.get()
        var6=var5.strip()
        var7=lst3.get()
        var8=var7.strip()
        var9=lst1.get()
        var10=var9.strip()
        do=float(var10)
        ho=float(var6)
        aw=float(var8)
        reset()
        mm="prediction.txt"
        with open(mm,"a+") as m:
            m.write("\n")
        m.close()
        ho1=ho-0.01
        aw1=aw-0.01
        ho2=ho+0.01
        aw2=aw+0.01
        print(len(data))
        fine=[["home","draw","away","HFT","AFT"]]
        for i in range((100)):
            dt1=data.iloc[i,0]
            dt2=data.iloc[i,1]
            dt3=data.iloc[i,2]
            dt4=data.iloc[i,3]
            dt5=data.iloc[i,4]
            #print(dt1,dt2,dt3,dt4,dt5)
            fha=search(dt1,dt3,data)
            fhd=search_hd(dt1,dt2,data)
            fad=search_ad(dt3,dt2,data)
            fhda=search2(dt1,dt2,dt3,data)
            #print(fhda[0],fha[0],fhd[0],fad[0])
            may=str(dt1)+","+str(dt2)+","+str(dt3)+","+str(dt4)+","+str(dt5)+"\n"
            
            pr=[[dt1,dt2,dt3,dt4,dt5]]
            if((fhda[0]>=.5)&(fhda[0]<=.6)):
                
                if((fha[0]>=fhda[0])):
                    try:
                        fine=fine+pr
                        
                    except:
                        fine=fine+pr
                
        
        
        pd.DataFrame(fine).to_csv("testing.csv",header=None,index=None)
        scroll = Scrollbar(f)
        scroll.pack(side=RIGHT,fill=Y)
        text = Text(f, font=('bold'),height=26, width=165,fg="#000000",bg="#DCDCDC",yscrollcommand=scroll.set)
        
        with open(mm) as j:
            data1=j.readlines()
            for row in data1:
                text.insert(END,row)

        j.close()
        
        text.pack()
        text['state']="disabled"
        scroll.config(command=text.yview)
    btreset=Button(Tops,padx=3,pady=1,bd=10,fg="black",font=('arial',12,'bold'),width=5,text="HELP",bg="#32cd32",command=reset_win).grid(row=0,column=3)
    btreset=Button(Tops,padx=3,pady=1,bd=10,fg="black",font=('arial',15,'bold'),width=10,text="SUBMIT",bg="#FF8C00",command=submit).grid(row=10,column=0)
    btreset=Button(Tops,padx=3,pady=1,bd=10,fg="black",font=('arial',15,'bold'),width=10,text="CLEAR",bg="powder blue", command=reset).grid(row=10,column=1)
    btreset=Button(Tops,padx=3,pady=1,bd=10,fg="black",font=('arial',15,'bold'),width=10,text="EXIT",bg="#8B0000",command=exit1).grid(row=10,column=2)
main()
root.mainloop()
