#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd

#attatch files

School_data= '/Users/miguelvelez/Desktop/schools_complete.csv'

student_data= '/Users/miguelvelez/Desktop/students_complete.csv'

#read them in
school= pd.read_csv(School_data)
student= pd.read_csv(student_data)

#now combine the two data sets in to a single set

school_data_complete= pd.merge(student,school, how="left", on=["school_name","school_name"])

school_data_complete.head(10)


# In[42]:


#calculate total number of schools
Total_schools= len(school_data_complete["school_name"].unique())
#print(Total_schools)
Total_students= len(school_data_complete["Student ID"].unique())
#print(Total_students)

Total_budget= float(school_data_complete["budget"].sum())
#print(Total_budget)

#find the averages now.

#average math score

average_math_score= round(float(school_data_complete["math_score"].mean()),3)
#print(average_math_score)

average_reading_score= round(float(school_data_complete["reading_score"].mean()),3)
#print(average_reading_score)

pass_math= len(school_data_complete.loc[school_data_complete["math_score"]>=70]["Student ID"])
#print(pass_math)  now change this into a percent

per_pass_math= float(round(pass_math / Total_students *100, 2))
#print(per_pass_math)

#now do the same for reading, start with making a list using .loc() to find all the passing reading scores

pass_reading= len(school_data_complete.loc[school_data_complete["reading_score"]>=70]["Student ID"])
#check it out using print() if it works then change it into a percent.
#print(pass_reading)

per_pass_reading= float(round(pass_reading / Total_students *100, 2))
#print(per_pass_reading)

overall_pass= round((per_pass_reading + per_pass_math)/ 2, 2)
#print(overall_pass)

#great! it all works! now lets create a NEW data frame! start by making a dictionary


district_data= pd.DataFrame({"Total Schools":Total_schools, "Total Students":Total_students,"Total Budget":Total_budget,
                             "Average Math Score":average_math_score, "Average Reading Score":average_reading_score, 
                             "Percent Passing Math":per_pass_math, "Percent Passing Reading":per_pass_reading, "Overall Passing":overall_pass},index=[0])

#print(district_data)


#Time to clean this up...

district_data["Total Students"]= district_data["Total Students"].map('{:,}'.format)
district_data["Total Budget"]= district_data["Total Budget"].map('${:,}'.format)
district_data["Percent Passing Math"]= district_data["Percent Passing Math"].map('{}%'.format)
district_data["Percent Passing Reading"]= district_data["Percent Passing Reading"].map('{}%'.format)
district_data["Overall Passing"]= district_data["Overall Passing"].map('{}%'.format)
#print(district_data) notice the addition of '%' and '$'

district_data.head()












# In[101]:


Grouped_schools= school_data_complete.groupby("school_name")

school_summary = pd.DataFrame({"School Name":school["school_name"], "School Type":school["type"],
                             "Total Budget":school["budget"]})
#print(school_summary)

school_summary = school_summary.set_index("School Name")
school_summary = school_summary.sort_values("School Name")
#print(school_summary)

#calcualte data from groupedby df
school_summary["Total Students"]= Grouped_schools["Student ID"].count()
school_summary["Budget Per Student"]=school_summary["Total Budget"] / school_summary["Total Students"]
school_summary["Average Math Score"]= round(Grouped_schools["math_score"].mean(), 2)
school_summary["Average Reading Score"]= round(Grouped_schools["reading_score"].mean(), 2)

#calculate now the percentage

school_summary["Percent Passing Math"] = round((Grouped_schools.apply(lambda x: (x["math_score"] >= 70).sum()) / 
                                          school_summary["Total Students"]) * 100, 2)
school_summary["Percent Passing Reading"] = round((Grouped_schools.apply(lambda x: (x["reading_score"] >= 70).sum()) / 
                                          school_summary["Total Students"]) * 100, 2)
school_summary["Overall Passing Rate"] = round((school_summary["Percent Passing Math"] + 
                                               school_summary["Percent Passing Reading"]) / 2, 2)

school_summary = school_summary.sort_values("Overall Passing Rate", ascending=False)

#Now lets format the above...

school_summary["Total Budget"] = school_summary["Total Budget"].map('${:,}'.format)
#school_summary["Budget Per Students"]= school_summary["Budget Per Student"].map('${:,}'.format)

#School_summary= pd.DataFrame({"School Type": school["school_type"], "Total Budget": "budget", "Total Students": "Total_students", "Budget Per Student":"school"})

#check it out using .head

school_summary.head(10)


# In[102]:



#top preforming school
school_summary= school_summary.sort_values("Overall Passing Rate", ascending=False)
school_summary.head()


# In[103]:


#Bottom preforming school

school_summary= school_summary.sort_values("Overall Passing Rate", ascending=True)

school_summary.head()


# In[104]:


#math scores by grade

ninth= school_data_complete.loc[school_data_complete["grade"] == "9th"]
tenth= school_data_complete.loc[school_data_complete["grade"] == "10th"]
eleventh= school_data_complete.loc[school_data_complete["grade"] == "11th"]
twelfth= school_data_complete.loc[school_data_complete["grade"] == "12th"]

#here we are combining the data sets

math_ninth = ninth.groupby("school_name")["math_score"].mean()
math_tenth = tenth.groupby("school_name")["math_score"].mean()
math_eleventh = eleventh.groupby("school_name")["math_score"].mean()
math_twelfth = twelfth.groupby("school_name")["math_score"].mean()

math_grades = pd.DataFrame({"9th":math_ninth, "10th":math_tenth, 
                             "11th":math_eleventh, "12th":math_twelfth})

math_grades = round(math_grades, 1)

print(math_grades)



# In[105]:


# Reading Scores by Grade just copy the above, and change it around.
ninth= school_data_complete.loc[school_data_complete["grade"] == "9th"]
tenth= school_data_complete.loc[school_data_complete["grade"] == "10th"]
eleventh= school_data_complete.loc[school_data_complete["grade"] == "11th"]
twelfth= school_data_complete.loc[school_data_complete["grade"] == "12th"]


reading_ninth = ninth.groupby("school_name")["reading_score"].mean()
reading_tenth = tenth.groupby("school_name")["reading_score"].mean()
reading_eleventh = eleventh.groupby("school_name")["reading_score"].mean()
reading_twelfth = twelfth.groupby("school_name")["reading_score"].mean()

reading_grades = pd.DataFrame({"9th":reading_ninth, "10th":reading_tenth, 
                             "11th":reading_eleventh, "12th":reading_twelfth})

reading_grades = round(reading_grades, 1)
print(reading_grades)


# In[116]:


#Scores by School spending

spending_bins = [0,585, 615, 645, 675]


group_names = ["<$585", "$585-629", "$630-644", "$645-675"]
#the group names will be acting as a bucket to refrence the table


# In[117]:


#now were building the table

school_summary["Spending Ranges Per Student"]= pd.cut(school_summary["Budget Per Student"], spending_bins , labels=group_names).head()
    


spending_groups = school_summary.loc[:, ["Spending Ranges Per Student","Average Math Score", "Average Reading Score",
                                     "Percent Passing Math", "Percent Passing Reading",
                                     "Overall Passing Rate"]].groupby("Spending Ranges Per Student")

spending_groups.mean()




# In[118]:


school_summary.dtypes


# In[120]:


size_bins = [0, 1000, 3000, 5000]
group_names = ["Small (<1000)", "Medium (1000-3000)", "Large (3000-5000)"]

school_summary["Size Ranges"] = pd.cut(school_summary["Total Students"], size_bins, labels=group_names)

size_groups = school_summary.loc[:, ["Size Ranges","Average Math Score", "Average Reading Score",
                                     "Percent Passing Math", "Percent Passing Reading",
                                     "Overall Passing Rate"]].groupby("Size Ranges")

size_groups.mean()


# In[121]:


#sources by type

district_groups = school_summary.loc[:, ["School Type", "Average Math Score", "Average Reading Score",
                                     "Percent Passing Math", "Percent Passing Reading",
                                     "Overall Passing Rate"]].groupby("School Type")

district_groups.mean()


# In[ ]:




