# Zombie_vs_Human
When you watch a zombie movie, have you ever doubt about whether zombie will totally die due to starve, espcially survival human population decline with time. This curious derive this project, I consider as many factors as I can in a zombie apocalypse. So you can change parameter like: zombie-init-num,  health-human-init-population,  zombie-virus-infection-rate,  zombie-virus-gen-mutation-rate etc for different scence.  So finally,  we can get a different result with classic zombie movie, for most situations, zombie will be cleared and samll group human survival , whcih most zombie actually die for hungry. 
Of course, I have clear some base set in my simulation,   
1 there no any zombie-virus-cure be developed ever.   
2 zombie will died if they dont eat human for a long time(this number can be set for youself).  
3 human survival probability is decided by their physical condition and learning-ability and some lucky. For example, Higher learning-ability will have higher survival probability in the next time after survival from one time zombie-attack. Other example, even you are smart and strong, but you still will be kill and transfer since your bad lucky.  
4 huamn and zombie will be seperated by several groups in every day. You can consider this set as different population density in differnet area.  


# Start Simulation:
## Command:
```shell
python virus-pro.py -ih <human-init-population> -iz <zombie-init-nums> -K <simulate-time> -ii <init_infection_rate>
```
hyper-parameters:
  
  ih: init_health  
  iz: init_zombie    
  K: simulate_iterate , default=1  
  ii: init_infection_rate, default=0.99. 

If you want to change math function of virus gen-mutation, you can change mutation function of zombie class in your opinion.
## Result:
  This simulation program will simulate zombie vs human until satisfy one of three conditions below.
  1. survival human population or zombie num has arrival dynamic balance more than 10 days.
  2. human or zombie has been eliminated.
  3. simulation running more than 1000 days in program epoch.
  
  Processing will return final human population, zombie nums and stopping days. 
  Meanwhile program will product two csv file for recording data:
  1. experiment_data.csv:  record final data (include days, human population, zombie nums)
  <img width="236" alt="image" src="https://user-images.githubusercontent.com/35327931/201452198-6a0a9272-9320-4c0a-8b17-f915a0737d0a.png">
  2. processing_data.csv:  record processing data every 10 days.
  <img width="290" alt="image" src="https://user-images.githubusercontent.com/35327931/201452367-addc9640-3add-44fd-8fda-186974f3d882.png">


  
