import time
import argparse
import numpy as np
import random
import psutil
import queue, multiprocessing


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

    def eat(self, food_num):
        '''
        :param company_num: zombie companies num
        :param person_num:  captured health person num
        :return:
        '''

        feed_weight = food_num
        if feed_weight==0:
            self.vitality-=30
        elif 0<self.vitality<150:
            self.vitality+=feed_weight*30
            if self.vitality>150:
                self.vitality=150

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
        # mean 110, std 30 , limit=150
        self.vitality = np.random.normal(110, 30)
        self.learning_ability = np.random.normal(110, 30)

    def learning_survival(self):
        '''

        :param survival_time:
        :return:
        '''
        self.vitality *= 1.09
        self.learning_ability *= 1.12
        if self.vitality > 150:
            self.vitality = 150
        if self.learning_ability > 150:
            self.learning_ability = 150
        #self.contact_chance = 1/(1+np.exp(args.total_health/args.total_zombie))  # sigmod function


def random_group(population):
    '''
    every day cluster zombie and health to random num group with random population
    :param population:  zombie or health population
    :return: group_list
    '''
    total = 0
    cap = 0
    group_list = []
    #n = random.randint(10)
    #print('n: {}'.format(n))
    while 1:
        group_population = random.randint(1, 50)
        total += group_population
        if total < len(population):
            group_list.append(population[cap: cap+group_population])
            cap = total
        else:
            group_list.append(population[cap:])
            break

    return group_list


def bite_result_pro(sp:float, hg:list, zg:list):
    '''
    when happen bit , hg and zg change result
    :param sp: survival probability
    :param hg: health-group list
    :return: hg, zg
    '''
    import math

    hg_loss_num = math.ceil(len(hg) * (1 - sp))
    hg_sur = hg[:int(len(hg)*sp)]
    hg_loss = hg[int(len(hg)*sp):]

    if hg_loss_num / len(zg) > 1:
        bit_h_num = math.ceil(hg_loss_num / len(zg))
        zg_list = zg * bit_h_num
    else:
        zg_list = zg

    hg_transform = []
    for idx, h in enumerate(hg_loss):
        if random.randint(1, 1000) <= zg_list[idx].mutation_rate * 1000:
            hg_transform.append(idx)
        else:
            hg_sur.append(h)

    for h in hg_sur:
        h.learning_survival()

    zg_gain = [Zombie(zg_list[lid].mutation_rate) for lid in hg_transform]
    zg_loss = math.ceil(len(zg)*sp)

    per_zombie_eat = round(hg_loss_num/len(zg), 2)
    zg_sur = zg[zg_loss:]
    for z in zg_sur:
        z.eat(per_zombie_eat)
    zg_sur += zg_gain

    print(f'hg_loss_num: {len(hg_transform)}, zg_loss: {zg_loss} zg_gain: {len(zg_gain)}, hg: {len(hg_sur)}, zg: {len(zg_sur)}')
    return hg_sur, zg_sur



def Contact(hg_zg):
    '''
    dest: simulate one group health attacked by one group zombie
    return: result health group and zombie group
    contact result: 1 health kill zombie,
                    2 zombie bit health and has chance transform health to zombie,
                    3 health kill zombie but be bit then still has chance be transformed to zombie.

    '''

    health_new = []
    zombie_new = []

    hg = hg_zg[0]
    zg = hg_zg[1]
    total = hg_zg[2]
    zombie_num = hg_zg[3]

    #print(f' health_group: {len(health_group)}, \n every health_group pop:{each_health_group_pop}')
    #print(f' zombie_group: {len(zombie_group)}, \n every zombie_group pop:{each_zombie_group_pop}')

    zombie_new_group = []
    health_new_group = []
    if random.randint(1, total) >= zombie_num: #Contact happen
        #print(f'h.vitality : {h.vitality} ,  h.learning_ability: {h.learning_ability}')
        lucky = np.random.normal(110, 30)
        '''
        if h.vitality > 150:
            h.vitality = 150
        if h.learning_ability > 150:
            h.learning_ability = 150
        '''
        total_health_vitality = sum([h.vitality for h in hg])
        total_health_learning_ability = sum([h.learning_ability for h in hg])
        avg_hg_vitality = total_health_vitality/len(hg)
        avg_hg_learning_ability = total_health_learning_ability/len(hg)
        total_zg_vitality = sum([z.vitality for z in zg])
        print('avg_hg_vitality: {} and avg_hg_learing_ability: {}'.format(avg_hg_vitality, avg_hg_learning_ability))

        zombie_id = np.random.choice(range(len(zg)), len(hg))

        #print(f'zombie_id: {zombie_id}')
        if avg_hg_vitality < 100 or avg_hg_learning_ability < 100:

            zombie_new_group.extend([Zombie(zg[zid].mutation_rate) for zid in zombie_id])
            print('hg_vitality lower than 100, health trasnfer to zombie {}'.format(len(zombie_new_group)))

            for z in zg:
                z.eat(round(len(hg)/len(zg)))


        else:
            total_coff = total_health_learning_ability+total_health_vitality+lucky
            survival_probability = np.exp(1.5*((0.4*total_health_vitality + 0.5*total_health_learning_ability+0.1*lucky - total_zg_vitality) / total_coff - 1)) # survival probability
            bit_probability = (1 - survival_probability)*0.6 # be transformed probability
            #bited_by_zombie = (1 - survival_probability)*0.7
            print(f'survival_prob : {survival_probability}, {survival_probability+bit_probability}')


            print('health-group will be attack and maybe some ot them will transfer to zombie, meanwhile zombie also\
                be partly eliminated.')
            health_new_group, zombie_new_group = bite_result_pro(survival_probability, hg, zg)

    else: #Contact no happen
        print('this group no contact with zombie')
        health_new_group = hg
        zombie_new_group = zg

        for z in zombie_new_group:
            z.eat(0)


    print(f'health_new: {len(health_new_group)}, zombie_new: {len(zombie_new_group)}')

    #print(f'Act {act}')
    return health_new_group, zombie_new_group

def health_init(init_health):
    for x in range(init_health):
        yield health_Person()

def zombie_init(init_zombie):
    for x in range(init_zombie):
        yield Zombie()


def beginSim(init_health, init_zombie, infection_rate):
    healthDictionary = []
    zombieDictionary = []
    for x in range(init_health):
        healthDictionary.append(health_Person())
    for x in range(init_zombie):
        zombieDictionary.append(Zombie(infection_rate))
    print(f'Health population: {len(healthDictionary)}, day: 0 ')
    print(f'Zombie population: {len(zombieDictionary)}, day: 0 ,zombie_mutation: {[z.mutation_rate for z in zombieDictionary]} \n')
    return healthDictionary, zombieDictionary

from tuplex import *

def zombie_vs_health():
    days = 1
    c = Context()
    healthDictionary, zombieDictionary = beginSim(args.init_health, args.init_zombie, args.init_infection)

    last_health_num = args.init_health
    last_zombie_num = args.init_zombie
    balance_days = 0
    while 1:
        # health meet zombie
        #healthDictionary, zombieDictionary = Contact(healthDictionary, zombieDictionary)
        total = len(healthDictionary) + len(zombieDictionary)
        # print(f'total: {total}, health: {len(health)}, zombie: {len(zombie)}')

        health_group = random_group(healthDictionary)
        zombie_group = random_group(zombieDictionary)
        hg_zg = list(zip(health_group, zombie_group, [total]*len(zombie_group), [len(zombieDictionary)]*len(zombie_group)))

        hg_zg_new = c.parallelize(hg_zg).map(Contact).collect() #each group of health and zombie every day after contact result
        print('hg_zg_new:{}'.format(hg_zg_new))
        res_hg = health_group[len(hg_zg):]
        res_zg = zombie_group[len(hg_zg):]

        for hg in res_hg:
            healthDictionary += hg
        for zg in res_zg:
            zombieDictionary += zg
        for h, z in hg_zg_new:
            healthDictionary += h
            zombieDictionary += z

        if len(health_group) > len(zombie_group):
            for hg in health_group[len(zombie_group):]:
                healthDictionary.extend(hg)
        else:
            for zg in zombie_group[len(health_group):]:
                zombieDictionary.extend(zg)

        health_population_change = len(healthDictionary) - last_health_num
        zombie_num_change = len(zombieDictionary) - last_zombie_num
        last_health_num = len(healthDictionary)
        last_zombie_num = len(zombieDictionary)

        #zombie_mutation = [z.mutation_rate for z in zombieDictionary]
        print(f'Health population: {len(healthDictionary)}, day: {days} ')
        print(f'Zombie population: {len(zombieDictionary)}, day: {days} \n')  # , {zombie_mutation}

        days += 1
        if health_population_change == 0 and zombie_num_change == 0:
            balance_days += 1

        import csv
        if days % 10 == 0:
            csv_columns = ['health', 'zombie']
            with open('processing_data.csv', 'a+') as f:
                per10_data = {'Health_Population': len(healthDictionary), 'Zombie_Population': len(zombieDictionary)}
                writer = csv.DictWriter(f, fieldnames=per10_data.keys())
                writer.writeheader()
                writer.writerow(per10_data)

        if balance_days > 10 or len(zombieDictionary) == 0 or len(healthDictionary) == 0:
            print('Health and Zombie population has trend to balance')
            break
        if days > 1000:
            print('Days has more than 1000, simulate shut down')
            break

    data = {'exp_K': e, 'days': days, 'health': len(healthDictionary), 'zombie': len(zombieDictionary)}

    return data

import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--init_health', '-ih', type=int, default=100000)
    parser.add_argument('--init_zombie', '-iz', type=int, default=1)
    parser.add_argument('--K', type=int, default=100)
    parser.add_argument('--init_infection', '-ii', type=float, default=0.999)
    parser.add_argument('--init_death_rate', '-idr', type=float, default=0.5)
    args = parser.parse_args()

    cpu_num = psutil.cpu_count()
    print(f'CPU Nums: {cpu_num}')

    experiment_data = []

    #random.seed(10)
    st = time.time()
    for e in range(args.K):
        print(f'\n {e}th simulation')
        ed = zombie_vs_health()
        experiment_data.append(ed)

    sp = time.time() - st
    print(f'Finish ! time span {sp}')

    import pandas as pd

    df = pd.DataFrame(experiment_data)
    df.to_csv('experiment_data.csv', index=False)
    '''
    csv_columns = ['exp_K', 'days', 'health', 'zombie']
    with open('experiment_data.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        init_params = {'init_health': args.init_health, 'init_zombie': args.init_zombie, 'init_infection': args.init_infection}
        writer.writeheader(init_params)
        for e in experiment_data:
            writer.writerow(e)'''
