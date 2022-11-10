import time
import argparse
import numpy as np
import random

class zombie_virus(object):
    '''
    infection_rate : infection possibly when contact
    death_rate: death possibly after infect one person

    '''
    def __init__(self, args):
        self.infection_rate = args.infection_rate
        self.death_rate = args.death_rate
        self.gen_mutation_possible = args.gen_mutation_possible

    def gen_mutation(self):
        if self.gen_mutation_possible:
            self.infection_rate = self.infection_rate * np.exp(1)
            self.death_rate = self.death_rate * np.exp(-1)


class Zombie(object):
    '''
    vitality
    '''
    def __init__(self, init_mutatioin_rate=0):

        self.vitality = 150
        #self.IQ = 0
        #self.acitvate_days = 2
        if init_mutatioin_rate:
            self.mutation_rate = init_mutatioin_rate
        else:
            self.mutation_rate = 0.999
        #self.ture_death = False

    def eat(self, company_num, person_num):
        '''
        :param company_num: zombie companies num
        :param person_num:  captured health person num
        :return:
        '''

        feed_weight = person_num/company_num
        if feed_weight==0:
            self.vitality-=30
        elif 0<self.vitality<150:
            self.vitality+=feed_weight*30
            if self.vitality>150:
                self.vitality=150

        return self.vitality

    def mutation(self):
        if_mutation = random.randint(1, 300)
        '''
        1: virus transform health_person to zombie possible lower        
        2: virus transform possible raise
        other: virus without mutation
        '''

        if 2 < if_mutation <= 10:
            self.mutation_rate *= 0.6
        elif 1 <= if_mutation <= 2:
            self.mutation_rate *= 1.5
            if self.mutation_rate > 1:
                self.mutation_rate = 1


class health_Person(object):
    '''
    vitality: 100 represent total health, 0 represent death
    IQ:
    survival_poss
    kill_zombie
    contant_chance: health person contact with zombie_virus chance
    '''
    def __init__(self):
        ''' unique distribution
        self.vitality = random.randint(50, 100)
        self.learning_ability = random.randint(50, 100)
        '''
        # mean 110, std 40
        self.vitality = np.random.normal(110, 30)
        self.learning_ability = np.random.normal(110, 30)


        #self.contact_chance = 1/(1+np.exp(args.total_health/args.total_zombie))  # sigmod function


def random_cluster(population):
    '''
    every day cluster zombie and health to random num group with random population
    :param group:  zombie or health population
    :return:
    '''
    group_num = random.randint(1, population)
    sub_group_total = 0
    cap = 0
    sub_group_list = []
    average_num = population//group_num
    for g in group_num:
        sub_group = random.randint(1, average_num)
        if g == len(group_num)-1:
            sub_group = population - sub_group_total
        sub_group_total += sub_group

        sub_group_list.append(population[cap:cap+sub_group])
        cap = sub_group

    return sub_group_list

def contact(health, zombie):
    '''
    contact result: 1 health kill zombie,
                    2 zombie bit health and has chance transform health to zombie,
                    3 health kill zombie but be bit then still has chance be transformed to zombie.
    '''
    total = len(health) + len(zombie)
    act=0
    from copy import deepcopy
    zombie_gen = [z for z in zombie]
    health_gen = [h for h in health]
    for h, z in zip(health_gen, zombie_gen):
        act +=1
        if random.randint(1, total) >= len(zombie): #contact possible
            #print(f'h.vitality : {h.vitality} ,  h.learning_ability: {h.learning_ability}')
            lucky = np.random.normal(110, 30)
            if h.vitality > 150:
                h.vitality = 150
            if h.learning_ability > 150:
                h.learning_ability = 150

            if h.vitality < 80 or h.learning_ability < 80:
                health.remove(h)
                zombie.append(Zombie(z.mutation_rate))
                #print('health trasnfer to zombie')

            else:
                survival_probability = np.exp(1.5*((0.4*h.vitality + 0.5*h.learning_ability+0.1*lucky) / 180 - 1)) # survival probability
                bit_probability = (1 - survival_probability)*0.3 # be transformed probability
                #bited_by_zombie = (1 - survival_probability)*0.7
                #print(f'survival_prob : {survival_probability}, {survival_probability+bit_probability}')

                P = random.randint(1, 1000)
                #print(f'P :{P}')
                if P <= survival_probability*1000:
                    zombie.remove(z)
                    #print('health people survival and eliminate zombie')

                elif P <= (survival_probability+bit_probability)*1000:
                    if random.randint(1, 1000)<=z.mutation_rate*1000:
                        health.remove(h)
                        zombie.append(Zombie(z.mutation_rate))
                        #print('health transfer to zombie')
                    #else:
                        #print('health be bite but not transfer and zombie also survival')
                else:
                    if random.randint(1, 1000) <= z.mutation_rate*1000:
                        health.remove(h)
                        zombie.append(Zombie(z.mutation_rate))
                        #print('health transfer to zombie and zombie died')
                    zombie.remove(z)



    #print(f'Act {act}')
    return health, zombie

def health_init(init_health):
    for x in range(init_health):
        yield health_Person()

def zombie_init(init_zombie):
    for x in range(init_zombie):
        yield Zombie()

def beginSim(init_health, init_zombie):

    for x in range(init_health):
        healthDictionary.append(health_Person())
    for x in range(init_zombie):
        zombieDictionary.append(Zombie())

    print(f'Health population: {len(healthDictionary)}, day: 0 ')
    print(f'Zombie population: {len(zombieDictionary)}, day: 0 \n')

import csv
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--init_health', '-it', type=int, default=100000)
    parser.add_argument('--init_zombie', '-iz', type=int, default=1)
    parser.add_argument('--K', type=int, default=100)
    parser.add_argument('--init_death_rate', '-idr', type=float, default=0.5)
    parser.add_argument('--init_gen_mutation', '-igm', type=float, default=0.3, dest='virus init gen mutation rate')

    args = parser.parse_args()
    experiment_data = []

    for e in range(args.K):
        print(f'\n {e}th simulation')
        healthDictionary = []
        zombieDictionary = []
        days = 1
        beginSim(args.init_health, args.init_zombie)
        last_health_num = args.init_health
        last_zombie_num = args.init_zombie
        balance_days = 0
        while 1:
             # health meet zombie
            healthDictionary, zombieDictionary = contact(healthDictionary, zombieDictionary)

            for z in zombieDictionary:
                z.mutation()


            health_population_change = len(healthDictionary) - last_health_num
            zombie_num_change = len(zombieDictionary) - last_zombie_num
            last_health_num = len(healthDictionary)
            last_zombie_num = len(zombieDictionary)

            zombie_mutation = [z.mutation_rate for z in zombieDictionary]
            print(f'Health population: {len(healthDictionary)}, day: {days} ')
            print(f'Zombie population: {len(zombieDictionary)}, day: {days} \n')
            days += 1
            if health_population_change==0 and zombie_num_change==0:
                balance_days += 1
            if days%10==0:
                with open('processing_data.csv', 'a+', newline='') as f:
                    per10_data = {'Health_Population': len(healthDictionary), 'Zombie_Population':len(zombieDictionary)}
                    writer = csv.DictWriter(f, fieldnames=per10_data.keys())
                    writer.writerow(per10_data)

            if balance_days>10 or len(zombieDictionary)==0 or len(healthDictionary)==0:
                print('Health and Zombie population has trend to balance')
                break
            if days>1000:
                print('Days has more than 1000, simulate shut down')
                break

        data = {'days': days, 'health': len(healthDictionary), 'zombie': len(zombieDictionary)}
        experiment_data.append(data)

    print('Finish !')

    import json
    import csv

    csv_columns = ['days', 'health', 'zombie']
    with open('experiment_data.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        for e in experiment_data:
            writer.writerow(e)
