import numpy as np

from mrjob.job import MRJob
from itertools import combinations, permutations
from math import sqrt
import mrjob

from scipy.stats.stats import pearsonr

class RestaurantSimilarities(MRJob):

    def steps(self):
        thesteps = [
            self.mr(mapper=self.line_mapper, reducer=self.users_items_collector),
            self.mr(mapper=self.pair_items_mapper, reducer=self.calc_sim_collector),
            self.mr(mapper=self.ranking_mapper, reducer=self.top_similar_collector)
        ]
        return thesteps

    def line_mapper(self,_,line):
        user_id,business_id,stars,business_avg,user_avg=line.split(',')
        yield user_id, (business_id,stars,business_avg,user_avg)

    def users_items_collector(self, user_id, values):
        ratings=[]
        for business_id,stars,business_avg,user_avg in values:
            ratings.append((business_id,(stars, user_avg)))
        yield user_id, ratings

    def pair_items_mapper(self, user_id, values):
        ratings = values
        for biz1tuple, biz2tuple in combinations(ratings, 2):
            biz1, biz1r=biz1tuple
            biz2, biz2r=biz2tuple
            if biz1 <= biz2 :
                yield (biz1, biz2), (biz1r, biz2r)
            else:
                yield (biz2, biz1), (biz2r, biz1r)

    def calc_sim_collector(self, key, values):
        (rest1, rest2), common_ratings = key, values
        diff1=[]
        diff2=[]
        n_common=0


        for rt1, rt2 in common_ratings:
            diff1.append(float(rt1[0])-float(rt1[1]))
            diff2.append(float(rt2[0])-float(rt2[1]))
            n_common=n_common+1
        if n_common==0:
            rho=0.
        else:
            rho=pearsonr(diff1, diff2)[0]
            if np.isnan(rho):
                rho=0.
        yield (rest1, rest2), (rho, n_common)

    def ranking_mapper(self, restaurants, values):
        sim, n_common = values
        rest1, rest2 = restaurants
        if int(n_common) > 0:
            yield (rest1), (sim, rest2, n_common)

    def top_similar_collector(self, key, values):
        rest1 = key
        for sim, rest2, n_common in sorted(values, reverse=True):
            yield None, (rest1, rest2, sim, n_common)

#Below MUST be there for things to work!
if __name__ == '__main__':
    RestaurantSimilarities.run()
