#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spacy
import json
import logging
import random
import re
import datefinder
import pandas as pd
import nltk


# In[2]:


nlp = spacy.load('sample_work_model_300_drop_0.05')
nlp2 = spacy.load("en_core_web_sm")


# In[3]:


# In[5]:


class Entities:
    
    
    def __init__(self):
        self.ix = 0
    ## 1.base salary
    def format_string(self,txt):
        p=txt.replace("\n",' ')
        p= p.replace("\t", " ")
        return(p.replace('\xa0',' '))

    def reference(self,p):
        ref={'year':['year','annum','annual'],'month':['monthly','month'],'week':['week','weekly','weeks'],'bi-week':['bi-week','bi-weekly'],'days':['day','days']}
        for main,word in ref.items(): 
            for i in range(len(word)): 
                if word[i] in [re.sub("[^a-z]", "",x.lower()) for x in p.split()]: 
                    return(main)

    def Base_Salary(self,doc,val={}):
        base_salary = []
        final_base_salary=[]
        if not len(val):
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="Base_Salary":
                        base_salary.append(self.format_string(ent.text))
            if(len(base_salary)!= 0):

                base_salary_set = set(base_salary)
                base_salary_list = list(base_salary_set)
                for salary in base_salary:
                    money=re.findall('[\£\$\€\]{1}[,0-9]{1,10}',salary)
                    if(len(money)):
                        suffix=self.reference(salary)
                        if(suffix):
                            final_base_salary.append('{} {}'.format(money[0],"per " + suffix))
                        else:
                            final_base_salary.append('{}'.format(money[0]))

                if(len(final_base_salary)):
                    return(final_base_salary[0])
                elif(len(base_salary_list)):
                    base_salary_list=[x.title() for x in base_salary_list]
                    return(base_salary_list)
                else:
                    return("None")
            else:
                return (None)
        else:
            try:
                if 'Base_Salary' in val.keys():
                
                    ents=val['Base_Salary']
                    for i in range(len(ents)):
                        if ents[i]:
                            for salary in ents[i]:
                                money=re.findall('[\£\$\€\]{1}[,0-9]{1,10}',salary)
                                if(len(money)):
                                    suffix=self.reference(salary)
                                    if(suffix):
                                        final_base_salary.append('{} {}'.format(money[0],suffix))
                                    else:
                                        final_base_salary.append('{}'.format(money[0]))
                return(final_base_salary)
            except AssertionError as error:
                print(error)

                return(None)
                    
    ## 2.start_date
    def start_date(self,doc,val={}):
        start_date = []
        final_start_date=[]
        if not len(val):
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="Start_date":
                        start_date.append(self.format_string(ent.text))

            if(len(start_date)!= 0):

                start_date_set = set(start_date)

                start_date_list = list(start_date_set)

                for item in start_date_list:
                    matches = datefinder.find_dates(item)
                    for match in matches:
                        final_start_date.append(match.strftime("%m-%d-%Y"))
                if len(final_start_date)!=0:
                    return(final_start_date[0])
                else:
                    return("None")    
            else:
                return ("None")
        else:
            try:
                if 'Start_date' in val.keys():
                    ents=val['Start_date']
                    for i in range(len(ents)):
                        if ents[i]:
                            for item in ents[i]:
                                matches = datefinder.find_dates(self.format_string(item))
                                for match in matches:
                                    final_start_date.append(match.strftime("%d-%m-%Y"))
                return(final_start_date)
            except AssertionError as error:
                print(error)

                return("None")
                    
                
    ##3.End_date
    def end_date(self,doc,val):
        end_date = []
        final_end_date=[]
        if not len(val):
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="End_date":
                        end_date.append(self.format_string(ent.text))

            if(len(end_date)!= 0):

                end_date_set = set(end_date)
                end_date_list = list(end_date_set)
                for item in end_date_list:
                    matches = datefinder.find_dates(item)
                    for match in matches:
                        final_end_date.append(match.strftime("%d-%m-%Y"))
                if len(final_end_date)!=0:            
                    return(final_end_date[0])
                else:
                    return("None")
            else:
                return ("None")
        else:
            try: 
                if 'End_date' in val.keys():
                    ents=val['End_date']
                    for i in range(len(ents)):
                        if ents[i]:
                            for item in ents[i]:
                                matches = datefinder.find_dates(self.format_string(item))
                                for match in matches:
                                    final_start_date.append(match.strftime("%m-%d-%Y"))
                    return(final_start_date)
            except AssertionError as error:
                print(error)

                return("None")
    ##4.address of employee
    def address_employee(self,doc,val={}):
        address = []
        if not len(val):
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_ == "Address_Employee":
                        address.append(self.format_string(ent.text))
                if len(address) != 0:
                    if (len(address) != 1):
                        address_set = set(address)
                        address_list = list(address_set)
                        return address_list[0].title()
                    else:
                        return address[0].title()
                else:
                    return ("None")
        else:
            try: 
                if 'Address_Employee' in val.keys(): 
                
                    ents=val['Address_Employee']

                    for i in range(len(ents)):
                        if ents[i]:
                            address.append(self.format_string(ents[i][0]))
                    return(address)
                
            except AssertionError as error:
                print(error)
                return([None,None])
            
    ## 5.address of employer
    def address_employer(self,doc,val={}):
        address = []
        if not len(val):
            
            if doc.ents:
                for ent in doc.ents:

                    if ent.label_ == "Address_Employer":
                        address.append(self.format_string(ent.text))
                if len(address) != 0:
                    if (len(address) != 1):
                        address_set = set(address)
                        address_list = list(address_set)
                        return address_list[0].title()
                    else:
                        return address[0].title()
                else:
                    return ("None")
        else:
            try:
                if 'Address_Employer' in val.keys():
                    ents=val['Address_Employer']
                    for i in range(len(ents)):
                        if ents[i]:
                            address.append(self.format_string(ents[i][0]))
                    return(address)
            except AssertionError as error:
                print(error)
                return([None,None])
            
    ## 6.supervisor information
    def supervisor(self,doc,val={}):
        supervisor = []
        if not len(val):
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_ == "Supervisor_Info":
                        supervisor.append(self.format_string(ent.text))
                if len(supervisor) != 0:


                    supervisor_set = set(supervisor)
                    supervisor_list = list(supervisor_set)
                    return supervisor_list[0].title()
                else:
                    return ("No Information")
        else:
            try:
                if 'Supervisor_Info' in val.keys():
                    ents=val['Supervisor_Info']
                    for i in range(len(ents)):
                        if ents[i]:
                            supervisor.append(self.format_string(ents[i][0]))
                    return([ x.title() for x in supervisor])
            except AssertionError as error:
                print(error)

                return([None,None])
                

            
    ## 7.Stock
    def stock(self,doc,val={}):
        stock = []
        if not len(val):
            
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="Stock_options":    # need to make this efficient.
                        stock.append(ent.text)
            if(len(stock)!=0):
                stock=[((" ".join(x.split())).lower()).title() for x in stock]
                stock_set=set(stock)
                stock_list=list(stock_set)
              #if "stock option" or "stock options" in stock_list and : # need to make this efficient and introduce tokens
                for ix in stock_list:
               # if ix == "stock option" or "stock options":
                #        continue 
                    text = ix.replace("\xa0", " ")
                    return text
            else:
                return("No")
        else:
            try:
                if 'Stock_options' in val.keys():
                    ents=val['Stock_options']
                    for i in range(len(ents)):
                        if ents[i]:
                            stock.append(self.format_string(ents[i][0]))
                return(stock)
            except AssertionError as error:
                print(error)

                return([None,None])

    
    ## 8.non monetary
    def non_monetory_benefits(self,doc,val={}):
        benefit = []
        if not len(val):
            
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="Non_monetary_benefits":
                        benefit.append(ent.text)
            if(len(benefit)!=0):
                benefit=[" ".join(x.split()) for x in benefit]
                benefit=[x.title() for x in benefit]
                benefit_set=set(benefit)
                benefit_list=list(benefit_set)
                if(len(benefit_list)==1):
                    return(benefit_list[0])
                elif(len(benefit_list)==0):
                    return("No")
                else:
                    return(", ".join(x for x in benefit_list))
            else:
                return("None")
        else:
            try:
                if 'Non_monetary_benefits' in val.keys():
                    ents=val['Non_monetary_benefits']
                    for i in range(len(ents)):
                        if ents[i]:
                            benefit.append(self.format_string(ents[i][0]))
                    return(benefit)
            except AssertionError as error:
                print(error)

                return([None,None])
                
    ## 9.compensation
    def compensation(self,doc,val={}):
        comp = []
        if not len(val):
            
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="Other_compensation":
                        comp.append(ent.text)
            if(len(comp)!=0):
                comp=[((" ".join(x.split())).lower()).title() for x in comp]
                comp_set=set(comp)
                comp_list=list(comp_set)
                if(len(comp_list)==1):
                    return(comp_list[0])
                elif(len(comp_list)==0):
                    return(None)
                else:
                    return(", ".join(x for x in comp_list))
        else:
            try:
                if 'Other_compensation' in val.keys():
                    ents=val['Other_compensation']
                    for i in range(len(ents)):
                        if ents[i]:
                            comp.append(self.format_string(ents[i][0]))
                    return(comp)
            except AssertionError as error:
                print(error)

                return([None,None])
            
    ## 10.bonus
    def bonus(self,doc,val={}):
        bonus = []
        if not len(val):
            
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="Bonus":
                        bonus.append(ent.text)
            if(len(bonus)!=0):
                bonus=[((" ".join(x.split())).lower()) for x in bonus]
                bonus_set=set(bonus)
                bonus_list=list(bonus_set)
                if "bonus" or "bonuses" in bonus_list:
    
                    if len(bonus_list)==1 and len(bonus_list[0])==1:
                        return("Yes")
                    else:
                        if bonus_list[0]!="bonus" and bonus_list[0]!="bonuses" :
                            return(bonus_list[0].title())
                        else:
                            return("Yes")
    
            else:
                return("No")
        else:
            try: 
                if 'Bonus' in val.keys():
                    ents=val['Bonus']
                    for i in range(len(ents)):
                        if ents[i]:
                            if "bonus" or "bonuses" in ents[i]:
                                #flag = True
                                if len(ents[i])==1:
                                        bonus.append("Yes")



                                for ix in ents[i]:
                          #if ix == "bonus" or "bonuses":
                          #    continue 
                                    bonus.append(self.format_string(ix[0]))

                            else:
                                    bonus.append("No")
                    return(bonus)
            except AssertionError as error:
                print(error)

                return([None,None])
                
    
    ##11.Notice
    def Notice(self,doc,val={}):
        notice = []
        if not len(val):
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="Notice_period":
                        notice.append(ent.text)
            if(len(notice)!= 0):
                notice=[(" ".join(x.split())).lower() for x in notice]  
                notice_set = set(notice)
                notice_list = list(notice_set)
                text = nlp2(notice_list[0])
                for ent in text.ents:
                    if(ent.label_=="CARDINAL"):
                        suffix=self.reference(notice_list[0])
                        if(suffix):
                       
                            return(ent.text+ " " + suffix)
                else:
                    print(notice_list)
                    return(notice_list[0])        
            else:
                
                return ("None")
        else:
            try:
                if 'Notice_period' in val.keys():
                    ents=val['Notice_period']
                    for i in range(len(ents)):
                        if ents[i]:
                            text = nlp2(ents[i])
                            for ent in text.ents:
                                if(ent.label_=="CARDINAL"):
                                    notice.append(ent.text)
                            else:
                                notice.append("No")
                        return(notice)
            except AssertionError as error:
                print(error)

                return([None,None])
    ## 12.Role
    def roles(self,doc,val={}):
        role=[]
        if not len(val):
            
        
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="Role":
                        role.append(ent.text)
            if(len(role)!=0):
                role=[((" ".join(x.split())).lower()).title() for x in role]
                role_set=set(role)
                role_list=list(role_set)
                if len(role_list)==1:
                    return(" ".join(x.capitalize() for x in role_list[0].split()))
                elif len(role_list)==0:
                    return("None")
                else:
                    return(" ".join(x.capitalize() for x in role_list[0].split()))
        else:
            try:
                if 'Role' in val.keys():
                    ents=val['Role']
                    for i in range(len(ents)):
                        if ents[i]:
                            role.append(self.format_string(ents[i][0]))
                    return(role)
            except AssertionError as error:
                print(error)

                return([None,None])

            
    ## 13. at will
    def at_will(self,doc,val={}):
        will=[]
        possible=['at will','at-will']
        if not len(val):
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="At_will_not":
                        will.append(ent.text)
            if(len(will)!=0):
                will=[(" ".join(x.split())).lower() for x in will]
                will_set=set(will)
                will_list=list(will_set)
                for x in will_list:
                    if(x in possible):
                        return("Yes")
            else:
                return("No")
        else:
            will_final=[]
            try:
                if 'At_will_not' in val.keys():
                    ents=val['At_will_not']
                    for i in range(len(ents)):
                        if ents[i]:
                            will=[(" ".join(x.split())).lower() for x in ents[i]]
                            will_set=set(will)
                            will_list=list(will_set)
                            if(len(will_list)==1 and will_list[0] in possible):
                                will_final.append("yes")
                            else:
                                will_final.append("No")
                    return(will)
                
            except AssertionError as error:
                print(error)

                return([None,None])
                
    
    ## 14. name of employee
    def name_employer(self,doc,val={}):
        names=[]
        if not len(val):    
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="Name_employer":
                        names.append(ent.text)
            if(len(names)!=0):
                names=[(" ".join(x.split())).lower() for x in names]
                names_set=set(names)
                name_list=list(names_set)
                if len(name_list)==1: 
                  
                    return(" ".join(x.title() for x in name_list[0].split()))
                elif len(name_list)==0:
                    
                    return('None')
                else:
                    
                    return(", ".join(x.title() for x in name_list))

            else:
                
                return('None')
        else:
            try:
                if 'Name_employer' in val.keys():
                    ents=val['Name_employer']
                    for i in range(len(ents)):
                        if ents[i]:
                            names.append(" ".join(x.title() for x in (self.format_string(ents[i][0])).split()))
                    return(names)
                
            except AssertionError as error:
                print(error)

                return([None,None])
    ## 15.Name of employee
    def name_employee(self,doc,val={}):
        names=[]
        if not len(val):
            
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="Name_employee":
                        names.append(ent.text)

            if(len(names)!=0):
                names=[(" ".join(x.split())).lower() for x in names]

                names_set=set(names)

                name_list=list(names_set)

                if len(name_list)>=1:
                    return(name_list[0].title())
                elif len(name_list)==0:
                    return(None)
        else:
            try:
                if 'Name_employee' in val.keys():
                    ents=val['Name_employee']
                    for i in range(len(ents)):
                        if ents[i]:
                            names.append(" ".join(x.capitalize() for x in (self.format_string(ents[i][0])).split()))
                    return([ x.title() for x in names])
                
            except AssertionError as error:
                print(error)

                return([None,None])
            
            ## 16.Health
    def health(self,doc,val={}):
        health = []
        if not len(val):
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_ == "Health_insurance":
                        health.append(ent.text)
                if(len(health) != 0):
                    return ("Yes")
                else:
                    return ("No")
        else:
            
            try:
                if 'Health_insurance' in val.keys():
                    ents=val['Health_insurance']
                    for i in range(len(ents)):
                        if ents[i]:
                            if(len(ents[i]) != 0):
                                health.append("Yes")
                            else:
                                health.append("No")
                        return(health)
            except AssertionError as error:
                print(error)

                return([None,None])
                
    ## 17. 401k
    def four_one_k(self,doc,val={}):
        four_one_k = []
        if not len(val):
            
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_ == "401K":
                        four_one_k.append(ent.text)
                if(len(four_one_k) != 0):
                    return ("Yes")
                else:
                    return ("No")
        else:
            try:
                if '401K' in val.keys():
                    
                    ents=val['401K']
                    for i in range(len(ents)):
                        if ents[i]:
                            if(len(ents[i]) != 0):
                                four_one_k.append("Yes")
                            else:
                                four_one_k.append("Yes")
                    return(four_one_k)
            except AssertionError as error:
                print(error)

                return([None,None])
                
    ## 18.date of aggreement
    
    def date_agreement(self,doc,val={}):
        date=[]
        if not len(val):
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_=="Date_aggrement":
                        date.append(ent.text)
            if(len(date)!=0):         
               # date=[(" ".join(x.split())).lower() for x in date]
                date_set=set(date)
                date_list=list(date_set)
                if len(date_list)==1:
                    matches = datefinder.find_dates(date_list[0])
                    for match in matches:
                        return(match.strftime("%m-%d-%Y"))

                elif len(date_list)==0:
                    return(None)
                else:
                    final_date_list=[]
                    for i in range(len(date_list)):
                        matches = datefinder.find_dates(date_list[i])
                        for match in matches:
                            final_date_list.append(match.strftime("%d-%m-%Y"))
                    return(list(set(final_date_list))[0])
        else:
            try:
                dates=[]
                if 'Date_aggrement' in val.keys():
                    ents=val['Date_aggrement']
                    for i in range(len(ents)):
                        if ents[i]:
                            if len(ents[i])==1:
                                matches = datefinder.find_dates(ents[i][0])
                                for match in matches:
                                    dates.append(match.strftime("%d-%m-%Y"))

                            elif len(ents[i])==0:
                                return(None)
                            else: 
                                final_date_list=[]
                                for j in range(len(ents[i])):
                                    matches = datefinder.find_dates(ents[i][j])
                                    for match in matches:
                                        final_date_list.append(match.strftime("%d-%m-%Y"))
                                dates.append(list(set(final_date_list)))
                    return(dates)
            except AssertionError as error:
                print(error)

                return([None,None])

    ##19. Vacation 
    def vacation(self,doc,val={}):
        vacation = []
        if not len(val):
            flag = False
            if doc.ents:
                for ent in doc.ents:
                    if ent.label_ == "Vacation":
                        vacation.append((ent.text).replace("\n"," "))
                vacation = [x.lower() for x in vacation]
                vacation_set = set(vacation)
                vacation_list = set(vacation_set)

                if (len(vacation_list))>0:

                    if "vacation" in vacation_list:
                        flag = True


                    if len(vacation_list) == 1 and flag:
                        return ("Yes")
                    else:
                        vacation_list=[ix.title() for ix in vacation_list]
                        return(vacation_list)

                    

                else:
                    print("here in the vacation")
                    return("None")               
              
        else:
            
            try:
                if 'Vacation' in val.keys():
                
                    ents=val['Vacation']
                    for i in range(len(ents)):
                        if ents[i]:
                       # print("Sup.{}".format(i))
                            vacation.append((self.format_string(ents[i][0])).title())
                    return(vacation)
            
            except AssertionError as error:
                print(error)

                
                return("None")
            
            
        
        
    ## main method 
    # Here the val dictionary is obtained from Class Validate, true_entities()
    def results(self, doc,val={}):
        mapping = {
            "Employee Name": self.name_employee(doc,val),
            "Address of Employee": self.address_employee(doc,val),
            "Company Name": self.name_employer(doc,val),
            "Address of Company": self.address_employer(doc,val),
            "Role": self.roles(doc,val),
            "Base Salary": self.Base_Salary(doc,val),
            "Date of Agreement": self.date_agreement(doc,val),
            "Start Date": self.start_date(doc,val),
            "End Date" : self.end_date(doc,val),
            "Supervisor Information": self.supervisor(doc,val),
            "Bonus": self.bonus(doc,val),
            "Notice Period" : self.Notice(doc,val),                  
            "Other Compensation": self.compensation(doc,val),
            "Non Monetary Benefits": self.non_monetory_benefits(doc,val),
            "Health Insurance": self.health(doc,val),
            "401k": self.four_one_k(doc,val),
            "At will": self.at_will(doc,val),
            "Stock": self.stock(doc,val),
            "Vacation": self.vacation(doc,val)
            }
         
        print(mapping)
        
        return mapping
        
    def results_to_df(self, mapping):
        self.ix = self.ix + 1
        #return pd.DataFrame.from_dict(mapping)
        return pd.DataFrame(mapping,index=[0],copy=True)
        
    
    
    


# In[7]:


#doc = nlp(test[80])


# In[14]:


#doc


# In[8]:


#obj = Entities()


# In[9]:


#mapping = obj.results(doc)


# In[10]:


#df = obj.results_to_df(mapping)


# In[18]:


#df


# In[19]:


#doc = nlp(test[25])


# In[20]:


#doc


# In[21]:


#m = obj.results(doc)


# In[34]:


#m


# In[35]:


#df.append(obj.results_to_df(m))


# In[ ]:





# In[37]:





class display_attributes:
    entities=['NAME_EMPLOYEE','ADDRESS_EMPLOYEE', 'NAME_EMPLOYER',  'ADDRESS_EMPLOYER','ROLE', 'BASE_SALARY','DATE_AGREEMENT','START_DATE', 'END_DATE', 'SUPERVISOR_INFO','BONUS','NOTICE_PERIOD','OTHER_COMPENSATION', 'NON_MONETARY_BENEFITS', 'HEALTH_INSURANCE','401K','AT_WILL_NOT','STOCK_OPTIONS','VACATION']
    def color(self):
        color=["#d6cbd3", "#eca1a6","#bdcebe","#f7786b","#80ced6","#b5e7a0","#f7935f","#c1946a","#c94c4c","#b1cbbb","#80ced6","#c1cfa5","#c1502e","#e06377","#b34f90","#ffcc5c","#588c7e","#738ce3","#f278b9"]
        i=0
        colors={}
        for e in self.entities:
            colors[e] = color[i]
            i=i+1
        return(colors)
    def color_dict(self):
        options = {"ents": self.entities, "colors": self.color()}
        return(options)
    def color_table(self,entities):
        colors=["#d6cbd3", "#eca1a6","#bdcebe","#f7786b","#80ced6","#b5e7a0","#f7935f","#c1946a","#c94c4c","#b1cbbb","#80ced6","#c1cfa5","#c1502e","#e06377","#b34f90","#ffcc5c","#588c7e","#738ce3","#f278b9"]
        i=0
        colors_dict={}
        for e in entities:
            colors_dict[e] = colors[i]
            i=i+1
        return(colors_dict)

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




