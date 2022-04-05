
from data_log import log
import math
import interactions as it
class League:
    LEAGUES_NAMES=["Yekzer","Panda","Aj"]
    def __init__(self,log,skill):
        self.log = log
        self.skill = skill
        self.players_list = {}
        self.total_xp = 0
        self.avg_xp = 0
        self.players_sorted = []
        self.ranking = [[],[],[]]
        self.leagues = [[],[],[]]
        self.leagues_d = {"Yekzer":{},
                          "Panda":{},
                          "Aj":{}
                          }
        

    def pick_total(self,skill):
        for player in self.log:
            self.players_list[player]=self.log[player][skill]
        return
        
        
        
    def sort_by_avg(self):
        pick_total(self.skill) 
        #get total/avg xp
        for i in self.players_list:
            self.total_xp+=self.players_list[i]
        self.avg_xp = math.ceil(self.total_xp/len(self.players_list))

        #sort players to leagues
        for i in self.players_list:
            if self.players_list[i] > 5000000000:
                self.leagues_d["Yekzer"][i]=self.players_list[i]
            elif self.players_list[i] < self.avg_xp:
                self.leagues_d["Aj"][i]=self.players_list[i]
            else:
                self.leagues_d["Panda"][i]=self.players_list[i]
        #listify leagues_d
        league_order = 0
        for league in self.leagues_d:
            temp_dict=self.leagues_d[league]
            temp_dict = {k: v for k, v in sorted(temp_dict.items(), key=lambda item: item[1],reverse=True)}
            for key, value in temp_dict.items():
                player = key + " -- " + "{:,}".format(value)
                self.leagues[league_order].append(player)
            league_order+=1
        for leag in range(3):
            for i in range(len(self.leagues[leag])):
                rank= f"Rank#{i+1} \n" + self.leagues[leag][i]
                self.ranking[leag].append(rank)
        return
class LeagueHelper:
    def __init__(self,leagues_obj):
        self.leagues=leagues_obj.leagues
        self.league_name=leagues_obj.LEAGUES_NAMES
        self.members_count=leagues_obj.members_count
        self.xp=league_obj.total_xp
        self.avg_xp=leagues_obj.avg_xp
        self.embeded_leagues = []
        
    def make_embeds(self):
        for league in self.leagues: 
            embeds_list = []                 
            fields_list = []
            last_fields_list = []
            embeds_count = math.ceil(len(self.league)/20)
            total_xp = "{:,}".format(self.xp)
            for i in range(embeds_count-1):
                fields_list = []
                for j in range(20):
                    rank = (i*20)+j+1
                    field = it.EmbedField(name=f"Rank#{rank}", value=self.league[rank-1])
                    fields_list.append(field)
                embed = it.Embed(
                             title="\u200b",
                             description="\u200b",     
                             fields=fields_list,
                             color=0x00ff00)
                embeds_list.append(embed)
            start = len(embeds_list)*20
            end = start + (members_count % 20)
            for j in range(start,end):
                rank = j+1
                field = it.EmbedField(name=f"Rank#{rank}", value=self.league[j])
                last_fields_list.append(field)
            last_embed = it.Embed(
                            title="\u200b",
                            description="\u200b",       
                            fields=last_fields_list,
                            color=0x00ff00)
            embeds_list.append(last_embed)   	   
            main_embed = it.Embed(
                              title=f"OwO",
                              description=f"Members Count : {members_count}\nTotal Xp : {total_xp}\nAverage Xp : {avg_xp}\n{league_name}'s League",       
                              fields=[],
                              color=0x00ff00)   
            self.embeded_leagues.append([main_embed,embeds_list])

        return self.embeded_leagues
    
    def leagues_pager(self,id):
        options_list = []
        for i in range(len(self.leagues_names)):
            option = SelectOption(
                                  label=f"{self.leagues_names[i]}",
                                  value=str(i),
                                  )
            options_list.append(option)
        pager_menu = SelectMenu(
        	                       options=options_list,
        	                       placeholder=f"Leagues",
        	                       custom_id=id, )
        return pager_menu  



l1 = League(log,"total")
leagues_names = l1.LEAGUES_NAMES
l1.sort_by_avg()
print(l1.total_xp)
print(l1.avg_xp)
print("------------------------")
embeded_leag = LeagueHelper(l1)
embededs = embeded_leag.make_embeds()
l_pager = embeded_leag.leagues_pager()





