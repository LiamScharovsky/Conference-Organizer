#!/usr/bin/env python
# coding: utf-8

# In[11]:


import requests
import json
class Organizer ():
    def __init__(self):
        
        response = requests.get('http://ct-mock-tech-assessment.herokuapp.com/')
        self.res = response.json() # this is the response from the API formatted for python 
        self.partners = self.res["partners"]
        self.countrySet = {}
        for peeps in self.partners:
            if peeps["country"] in self.countrySet:
                self.countrySet[peeps["country"]] =+ 1
            else:
                self.countrySet[peeps["country"]] = 1
        key_iterable = self.countrySet.keys()
        self.countryList = list(key_iterable)
        self.data = {} 

    
    def classify(self):
        for country in self.countryList:
            self.data[country] = []
            
        for peeps in self.partners:
            if peeps["country"] in self.data:
                self.data[peeps["country"]].append(peeps) 
            
        for country in self.data:
            self.countrySet[country] = []
            for i in range (len(self.data[country])):
                for j in range (len(self.data[country][i]["availableDates"])):
                    self.countrySet[country].append(self.data[country][i]["availableDates"][j])
        freq = {}      
        for country in self.data:
            freq[country] = {}
            for item in self.countrySet[country]: 
                if (item in freq[country]): 
                    freq[country][item] += 1
                else: 
                    freq[country][item] = 1
     
        maxValues = {}
        for country in self.data:
            keyList = list(freq[country].keys())
            valList = list(freq[country].values())
            allValues = freq[country].values()
            maxValue = max(allValues)
            position = valList.index(maxValue)
            maxValues[country] = keyList[position]         #got the most popular date. Missing the second most popular date
        myList = {}
        for country in self.data:
            myList[country] = sorted(freq[country].items(), key=lambda x: x[1], reverse=True)

        dates = {}
        for country in self.data:
            i= 0
            while True:
                if int(myList[country][0][0][-3:]) == int(myList[country][1][0][-3:]) + 1:
                    dates[country] = [myList[country][i][0], myList[country][i+1][0]]
                    break
                else: 
                    date = int(myList[country][i][0][-2:]) + 1
                    fullDate = myList[country][i][0][:-2] + str(date)
                    dates[country] = [myList[country][i][0], fullDate]
                    break
        peopleGoing = {}
        for country in self.data:
            for people in self.data[country]:
                if dates[country][0] in people["availableDates"] and dates[country][0] in people["availableDates"]:
                    if country in peopleGoing:
                        peopleGoing[country].append(people)
                    else:
                        peopleGoing[country] = [people]

        data = []
        for country in self.data:
            email = []
            for i in range (len(peopleGoing[country])):
                email.append(peopleGoing[country][i]['email'])
            data.append({'attendeeCount':len(peopleGoing[country]), 'attendees' : email, 'name' : country, 'startDate' : dates[country][0]})
        
        data = json.dumps(data)
    
        print(data)
     
        req = requests.post('http://ct-mock-tech-assessment.herokuapp.com/', json = {'data':data})
        print(req.text)
        print(req.status_code)
            
org = Organizer()
org.classify()


# In[ ]:





# In[ ]:





# In[ ]:




