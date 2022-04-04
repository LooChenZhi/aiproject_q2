#!/usr/bin/env python
# coding: utf-8

# # Question 2: Vaccine Distribution Modelling

import streamlit as st
import constraint
import math 

st.title("Question 2: Vaccine Distribution Modelling")
st.markdown("Constraint Satisfaction Problem is used to assign the right vaccine types and amounts to the vaccination centres.")
st.markdown("We will give priority to people under 35 years old, after that people between 35 to 60 years old. And lastly, people over 60 years old.")
st.markdown("""---""")

#predefine data for every state
max_capacity = [5000,10000,7500,8500,9500]
total_citizen = [565790,514544,889038,1153093,690884 ]
citizen_smaller_35 = [115900,100450,223400,269300,221100]
citizen_between_35_60 = [434890,378860,643320,859900,450500]
citizen_greater_60 = [15000,35234,22318,23893,19284]
total_CR1 = [20,30,22,16,19]
total_CR2 = [15,16,15,16,10]
total_CR3 = [10,15,11,16,20]
total_CR4 = [21,10,12,15,15]
total_CR5 = [5,2,3,1,1]
state = 1

for i in range(5): 

    #Get the number of days it will take to vaccinate everybody
    vac_a_day = math.ceil(citizen_greater_60[i]/max_capacity[i])
    vac_b_day = math.ceil(citizen_between_35_60[i]/max_capacity[i])
    vac_c_day = math.ceil(citizen_smaller_35[i]/max_capacity[i])
    total_day = vac_a_day + vac_b_day + vac_c_day

    problem = constraint.Problem()

    problem.addVariable('CR1', range(total_CR1[i]+1))  
    problem.addVariable('CR2', range(total_CR2[i]+1))  
    problem.addVariable('CR3', range(total_CR3[i]+1)) 
    problem.addVariable('CR4', range(total_CR4[i]+1)) 
    problem.addVariable('CR5', range(total_CR5[i]+1))  


    # We have different number of maximum vaccine for each state per day
    def capacity_constraint(a, b, c, d, e):  
        if (a*200 + b*500 + c*1000 + d*2500 + e*4000) >= max_capacity[i]:
            return True


    problem.addConstraint(capacity_constraint,['CR1','CR2','CR3','CR4','CR5'])

    rental = 999999999999999 
    solution_found = {}  
    solutions = problem.getSolutions()

    # Get the conditions for the minimum rental

    for s in solutions:
       current_rental = s['CR1']*100 + s['CR2']*250 + s['CR3']*500 + s['CR4']*800 + s['CR5']*1200
       current_capacity = s['CR1']*200 + s['CR2']*500 + s['CR3']*1000 + s['CR4']*2500 + s['CR5']*4000
       if current_rental < rental and current_capacity == max_capacity[i]:
            rental = current_rental
            solution_found = s

    #Print output
    subheader = "In State {}".format(state)
    st.header(subheader)
    
    info = "Minimum Rental for maximum capacity per day of {} is RM{}".format(max_capacity[i], rental)
    st.info(info)

    st.write(" ")

    st.write("""    
    Everyday, we'll rent:  
    {} CR-1 \n
    {} CR-2 \n
    {} CR-3 \n
    {} CR-4 \n 
    {} CR-5 \n

    All citizen will be vaccinated in {} days.

    By priotizing citizen age < 35, followed by 35 < age < 65, then age > 65\n
    We will only distribute Vaccine C for the first {} days\n
    We will only distribute Vaccine B for the next {} days\n
    We will only distribute Vaccine A for the next {} days
    """.format(solution_found['CR1'], solution_found['CR2'], solution_found['CR3'], solution_found['CR4'],solution_found['CR5'],total_day,vac_c_day,vac_b_day,vac_a_day))
    st.markdown("""---""")
    state += 1 


