from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import pandas as pd
from Election import *
import time
import json
# Create your views here.
def home(request):
    return render(request,"base.html")
#@login_required
def login_page(request):
    if request.method=="POST":
        user_name=request.POST.get("user_name")
        password=request.POST.get("password")
        a=User.objects.filter(username=user_name).exists()
        print(a)
        if not (User.objects.filter(username=user_name).exists()):
            messages.error(request,"Invalid User Name")
            return render(request,"login.html")
            
        user=authenticate(username=user_name,password=password)#this method check user name and password that would be authenticated password is encrypted
        if user is None:
            messages.error(request,"Invalid Credentials")
        else:
            login(request,user)
            return redirect("/home_prediction/")
    return render(request,"login.html")

def register_page(request):
    if request.method=="POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        user_name=request.POST.get("user_name")
        password=request.POST.get("password")
        user=User.objects.filter(username=user_name)
        if user.exists():
            messages.info(request,"User already exists with this name")
            return redirect("/register/")
        user=User.objects.create(first_name=first_name,
                            last_name=last_name,
                            username=user_name)
        user.set_password(password)
        user.save()
        messages.info(request,"Account Created Successfully")

        return redirect("/register/")
    return render(request,"register.html")
def log_out_page(request):
    logout(request)
    return redirect("/")
def home_prediction(request):
    return render(request,"prediction.html")
def summary(request):
    return render(request,"summary.html")
UT=["Jammu_and_kashmir","Chandigarh","Andaman_and_Nicobar","Daman_and_Diu","Lakshadweep"]
# def prediction(request):
#     if request.method=="POST":
#        state=request.POST.get("state")
#        INDIA=request.POST.getlist("INDIA")
#        NDA=request.POST.getlist("NDA")
#        Other=request.POST.getlist("Other")
#        if state =="Choose...":
#          messages.info(request,"state has not been selected")
#          return redirect("/prediction/")
#        if state in UT:
#             df1=pd.read_csv("Election/ALL_STATE.csv")
#             df1.fillna(0,inplace=True)
#             print(df1)
#             swing=df1.loc[df1["State"] == state]
#             print("Swing",swing)
#             election_state = "Election\\" + state + ".csv"
#             loksabha=pd.read_csv(election_state,encoding="windows-1252")
#             loksabha['NDA']=0
#             loksabha['INDIA']=0
#             loksabha["Other"]=0
#             loksabha.fillna(0,inplace=True)
#             print(loksabha)
#             for b in NDA:
#                 if b in loksabha.columns:
#                     t=int(swing.loc[:,b].values)
#                     loksabha['NDA']=loksabha['NDA']+loksabha[b]+((loksabha[b]*(t))/100)
#             for a in INDIA:
#                 if a in loksabha.columns:
#                      t=int(swing.loc[:,a].values)
#                      loksabha["INDIA"]=loksabha["INDIA"]+loksabha[a]+((loksabha[a]*(t))/100)
#             for c in Other:
#                 if c in loksabha.columns:
#                     t=int(swing.loc[:,a].values)
#                     loksabha["Other"]=loksabha["Other"]+loksabha[c]+((loksabha[c]*(t))/100)
#             print(loksabha)
#             st_india=loksabha["INDIA"].sum()
#             st_nda=loksabha["NDA"].sum()
#             st_other=loksabha["Other"].sum()
#             NDA=0
#             INDIA=0 
#             Other=0
#             for index,row in loksabha.iterrows():
#                 if row["NDA"]>row["INDIA"]and row["NDA"]>row["Other"]:
#                     print("NDA",row["Constituency_Name"])
#                     NDA=NDA+1
#                 elif row["INDIA"]>row["NDA"] and row["INDIA"]>row["Other"]:
#                     print("INDIA",row["Constituency_Name"])
#                     INDIA=INDIA+1
#                 elif row["Other"]>row["NDA"]and row["Other"]>row["INDIA"] :
#                     print("Other",row["Constituency_Name"])
#                     Other=Other+1 
#             return render(request,"result.html",{"d":[NDA,INDIA,Other],"n":["NDA","INDIA","Other"],"state":state,'a':[st_nda,st_india,st_other]})
#        else:
#             df1=pd.read_csv("Election/ALL_STATE.csv")
#             df1.fillna(0,inplace=True)
#             print(df1)
#             swing=df1.loc[df1["State"] == state]
#             print("Swing",swing)
#             election_state = "Election\\" + state + ".csv"
#             state_name="Assembly\\"+state+".csv"
#             loksabha=pd.read_csv(election_state,encoding="windows-1252")
#             loksabha['NDA']=0
#             loksabha['INDIA']=0
#             loksabha["Other"]=0
#             loksabha.fillna(0,inplace=True)
#             print(loksabha)
#             for b in NDA:
#                 if b in loksabha.columns:
#                    t=int(swing.loc[:,b].values)
#                    loksabha['NDA']=loksabha['NDA']+loksabha[b]+((loksabha[b]*(t))/100)
#             for a in INDIA:
#                 if a in loksabha.columns:
#                     t=int(swing.loc[:,a].values)
#                     loksabha["INDIA"]=loksabha["INDIA"]+loksabha[a]+((loksabha[a]*(t))/100)
#             for c in Other:
#                 if c in loksabha.columns:
#                     t=int(swing.loc[:,a].values)
#                     loksabha["Other"]=loksabha["Other"]+loksabha[c]+((loksabha[c]*(t))/100)
#             print(loksabha)
#             state_assembly=pd.read_csv(state_name,encoding="windows-1252")
#             state_assembly.fillna(0,inplace=True)
#             print(state_assembly)
#             state_assembly.drop(columns="Strong_Party",axis="columns",inplace=True)
#             group_the_constituency=state_assembly.groupby("Constituency_Name")
#             print(group_the_constituency)
#             base=group_the_constituency.sum()
#             base["NDA"]=0
#             base["INDIA"]=0
#             base["Other"]=0
#             for a in base.columns:
#                 if a in NDA:
#                     base["NDA"]+=base[a]
#             for b in base.columns:
#                 if b in INDIA:
#                     base["INDIA"]+=base[b]
#             for c in base.columns:
#                 if c in Other:
#                     base["Other"]+=base[c]
#             st_nda=base["NDA"].sum()
#             st_india=base["INDIA"].sum()
#             st_other=base["Other"].sum()

#             # Declaring the two variable India and NDa for counting their Seats
#             NDA=0
#             INDIA=0 
#             Other=0
#             #algorithm for Predicting the result
#             for (index1,row1),(index2,row2) in zip(loksabha.iterrows(),base.iterrows()):
#                if row1["NDA"]-row1["INDIA"]>50000 and row1["NDA"]-row1["Other"]>50000 and row2["NDA"]>row2["INDIA"] and row2["NDA"]>row2["Other"]:
#                     print("NDA",row1["Constituency_Name"])
#                     NDA=NDA+1
#                elif row1["INDIA"]-row1["NDA"]>50000 and row1["INDIA"]-row1["Other"]>50000 and row2["INDIA"]>row2["NDA"] and row2["INDIA"]>row2["Other"]:
#                     print("INDIA",row1["Constituency_Name"])
#                     INDIA=INDIA+1
#                elif row1["Other"]-row1["NDA"]>50000 and row1["Other"]-row1["INDIA"]>50000 and row2["Other"]>row2["NDA"] and row2["Other"]>row2["INDIA"]:
#                    print("BRS",row1["Constituency_Name"])
#                    Other=Other+1 
#                elif row2["NDA"]>row2["INDIA"] and row2["NDA"]>row2["Other"]:
#                   print("NDA",row1["Constituency_Name"])
#                   NDA=NDA+1
#                elif row2["INDIA"]>row2["NDA"] and row2["INDIA"]>row2["Other"]:
#                   print("INDIA",row1["Constituency_Name"])
#                   INDIA=INDIA+1
#                elif row2["Other"]>row2["INDIA"] and row2["Other"]>row2["NDA"]:
#                   print("BRS",row1["Constituency_Name"])
#                   Other=Other+1
#             return render(request,"result.html",{"d":[NDA,INDIA,Other],"n":["NDA","INDIA","Other"],"state":state,'a':[st_nda,st_india,st_other]})
#     return render(request,"prediction.html")

def prediction(request):
    if request.method=="POST":
       state=request.POST.get("state")
       INDIA=request.POST.getlist("INDIA")
       NDA=request.POST.getlist("NDA")
       Other=request.POST.getlist("Other")
       if state =="Choose...":
         messages.info(request,"state has not been selected")
         return redirect("/prediction/")
       if state in UT:
            df1=pd.read_csv("Election/ALL_STATE.csv")
            df1.fillna(0,inplace=True)
            print(df1)
            swing=df1.loc[df1["State"] == state]
            print("Swing",swing)
            election_state = "Election\\" + state + ".csv"
            loksabha=pd.read_csv(election_state,encoding="windows-1252")
            loksabha['NDA']=0
            loksabha['INDIA']=0
            loksabha["Other"]=0
            loksabha.fillna(0,inplace=True)
            print(loksabha)
            for b in NDA:
                if b in loksabha.columns:
                    t=int(swing.loc[:,b].values)
                    loksabha['NDA']=loksabha['NDA']+loksabha[b]+((loksabha[b]*(t))/100)
            for a in INDIA:
                if a in loksabha.columns:
                     t=int(swing.loc[:,a].values)
                     loksabha["INDIA"]=loksabha["INDIA"]+loksabha[a]+((loksabha[a]*(t))/100)
            for c in Other:
                if c in loksabha.columns:
                    t=int(swing.loc[:,a].values)
                    loksabha["Other"]=loksabha["Other"]+loksabha[c]+((loksabha[c]*(t))/100)
            print(loksabha)
            st_india=loksabha["INDIA"].sum()
            st_nda=loksabha["NDA"].sum()
            st_other=loksabha["Other"].sum()
            NDA=0
            INDIA=0 
            Other=0
            loksabha["Winning_Alliance"]=" "
            for index,row in loksabha.iterrows():
                if row["NDA"]>row["INDIA"]and row["NDA"]>row["Other"]:
                    print("NDA",row["Constituency_Name"])
                    loksabha.at[index,"Winning_Alliance"]="NDA"
                    NDA=NDA+1
                elif row["INDIA"]>row["NDA"] and row["INDIA"]>row["Other"]:
                    print("INDIA",row["Constituency_Name"])
                    loksabha.at[index,"Winning_Alliance"]="INDIA"
                    INDIA=INDIA+1
                elif row["Other"]>row["NDA"]and row["Other"]>row["INDIA"] :
                    print("Other",row["Constituency_Name"])
                    Other=Other+1 
                    loksabha.at[index,"Winning_Alliance"]="Other"
                df=loksabha[["Constituency_Name","Seat_Type","Winning_Alliance"]]
                df=pd.DataFrame(df)
                json_records = df.reset_index().to_json(orient ='records') 
                data = [] 
                data =json.loads(json_records) 
                print(data)
            return render(request,"result.html",{"d":[NDA,INDIA,Other],"n":["NDA","INDIA","Other"],"state":state,'a':[st_nda,st_india,st_other],"lok":data})
       else:
            df1=pd.read_csv("Election/ALL_STATE.csv")
            df1.fillna(0,inplace=True)
            print(df1)
            swing=df1.loc[df1["State"] == state]
            print("Swing",swing)
            election_state = "Election\\" + state + ".csv"
            state_name="Assembly\\"+state+".csv"
            loksabha=pd.read_csv(election_state,encoding="windows-1252")
            loksabha['NDA']=0
            loksabha['INDIA']=0
            loksabha["Other"]=0
            loksabha.fillna(0,inplace=True)
            print(loksabha)
            for b in NDA:
                if b in loksabha.columns:
                   t=int(swing.loc[:,b].values)
                   loksabha['NDA']=loksabha['NDA']+loksabha[b]+((loksabha[b]*(t))/100)
            for a in INDIA:
                if a in loksabha.columns:
                    t=int(swing.loc[:,a].values)
                    loksabha["INDIA"]=loksabha["INDIA"]+loksabha[a]+((loksabha[a]*(t))/100)
            for c in Other:
                if c in loksabha.columns:
                    t=int(swing.loc[:,a].values)
                    loksabha["Other"]=loksabha["Other"]+loksabha[c]+((loksabha[c]*(t))/100)
            print(loksabha)
            state_assembly=pd.read_csv(state_name,encoding="windows-1252")
            state_assembly.fillna(0,inplace=True)
            print(state_assembly)
            state_assembly.drop(columns="Strong_Party",axis="columns",inplace=True)
            group_the_constituency=state_assembly.groupby("Constituency_Name")
            print(group_the_constituency)
            base=group_the_constituency.sum()
            print("base",base)
            base["NDA"]=0
            base["INDIA"]=0
            base["Other"]=0
            for a in base.columns:
                if a in NDA:
                    base["NDA"]+=base[a]
            for b in base.columns:
                if b in INDIA:
                    base["INDIA"]+=base[b]
            for c in base.columns:
                if c in Other:
                    base["Other"]+=base[c]
            st_nda=base["NDA"].sum()
            st_india=base["INDIA"].sum()
            st_other=base["Other"].sum()

            # Declaring the two variable India and NDa for counting their Seats
            NDA=0
            INDIA=0 
            Other=0
            loksabha["Winning_Alliance"]=""
            #algorithm for Predicting the result
            for (index1,row1),(index2,row2) in zip(loksabha.iterrows(),base.iterrows()):
               if row1["NDA"]-row1["INDIA"]>50000 and row1["NDA"]-row1["Other"]>50000 and row2["NDA"]>row2["INDIA"] and row2["NDA"]>row2["Other"]:
                    print("NDA",row1["Constituency_Name"])
                    loksabha.at[index1,"Winning_Alliance"]="NDA"
                    NDA=NDA+1
               elif row1["INDIA"]-row1["NDA"]>50000 and row1["INDIA"]-row1["Other"]>50000 and row2["INDIA"]>row2["NDA"] and row2["INDIA"]>row2["Other"]:
                    print("INDIA",row1["Constituency_Name"])
                    loksabha.at[index1,"Winning_Alliance"]="INDIA"
                    INDIA=INDIA+1
               elif row1["Other"]-row1["NDA"]>50000 and row1["Other"]-row1["INDIA"]>50000 and row2["Other"]>row2["NDA"] and row2["Other"]>row2["INDIA"]:
                   print("BRS",row1["Constituency_Name"])
                   loksabha.at[index1,"Winning_Alliance"]="Other"
                   Other=Other+1 
               elif row2["NDA"]>row2["INDIA"] and row2["NDA"]>row2["Other"]:
                  print("NDA",row1["Constituency_Name"])
                  loksabha.at[index1,"Winning_Alliance"]="NDA"
                  NDA=NDA+1
               elif row2["INDIA"]>row2["NDA"] and row2["INDIA"]>row2["Other"]:
                  print("INDIA",row1["Constituency_Name"])
                  loksabha.at[index1,"Winning_Alliance"]="INDIA"
                  INDIA=INDIA+1
               elif row2["Other"]>row2["INDIA"] and row2["Other"]>row2["NDA"]:
                  loksabha.at[index1,"Winning_Alliance"]="Other"
                  print("BRS",row1["Constituency_Name"])
                  Other=Other+1
            df=loksabha[["Constituency_Name","Seat_Type","Winning_Alliance"]]
            df=pd.DataFrame(df)
            json_records = df.reset_index().to_json(orient ='records') 
            data = [] 
            data =json.loads(json_records) 
            return render(request,"result.html",{"d":[NDA,INDIA,Other],"n":["NDA","INDIA","Other"],"state":state,'a':[st_nda,st_india,st_other],'lok':data})
    return render(request,"prediction.html")

