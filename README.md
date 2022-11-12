# Zombie_vs_Human
Simulate A battle between Zombie and Human

# Start Simulation:
## Command:
```shell
python virus-pro.py -ih <human-init-population> -iz <zombie-init-nums> -K <simulate-time> -ii <init_infection_rate>
```
hyper-parameters:
  
  ih: init_health  
  iz: init_zombie  
  K: simulate_iterate  
  ii: init_infection_rate

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


  
