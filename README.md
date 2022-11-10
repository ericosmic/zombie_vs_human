# zombie_vs_human
Simulate A battle between zombie and human

# RUN Simulation:
## Command:
python virus-pro.py -ih <human-init-population> -iz <zombie-init-nums> -K <simulate-time> -ii <init_infection_rate>
  
Parameters:
  
  ih: init_health
  iz: init_zombie
  K: simulate_time
  ii: init_infection_rate

## Result:
  This simulation program will simulate zombie vs human until satisfy one of three conditions below.
  1. survival human population or zombie num has arrival dynamic balance more than 10 days.
  2. human or zombie has been elimnated.
  3. simulation running more than 1000 days in program epoch.
  
  Processing will return final human population, zombie nums and end days. 
  Meanwhile program will product two csv file for recording data:
  1. experiment_data.csv:  record final data (include days, human population, zombie nums)
  2. processing_data.csv:  record processing data of each 10 days.
