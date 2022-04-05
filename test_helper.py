
import math
import interactions as it
class League:
    LEAGUES_NAMES=["Yekzer","Panda","Aj"]
    def __init__(self,log,skill):
        self.log = log
        self.members_count = len(log)
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
         return
        
        
        
    def sort_by_avg(self):
        for player in self.log:
            self.players_list[player]=self.log[player][self.skill]
       
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
        self.leagues_names=leagues_obj.LEAGUES_NAMES
        self.members_count=leagues_obj.members_count
        self.xp=leagues_obj.total_xp
        self.avg_xp=leagues_obj.avg_xp
        self.embeded_leagues = []
        
    def make_embeds(self):
        order = 0
        print("0")
        for league in self.leagues: 
            embeds_list = []                 
            fields_list = []
            last_fields_list = []
            embeds_count = math.ceil(len(league)/20)
            total_xp = "{:,}".format(self.xp)
            print("1")
            for i in range(embeds_count-1):
                print("1.0")
                fields_list = []
                for j in range(20):
                    rank = (i*20)+j+1
                    field = it.EmbedField(name=f"Rank#{rank}", value=league[rank-1])
                    fields_list.append(field)
                    print("1.1")
                embed = it.Embed(
                             title="\u200b",
                             description="\u200b",     
                             fields=fields_list,
                             color=0x00ff00)
                embeds_list.append(embed)
                print("1.2")
            start = len(embeds_list)*20
            end = start + (members_count % 20)
            print("2.0")
            for j in range(start,end):
                rank = j+1
                field = it.EmbedField(name=f"Rank#{rank}", value=league[j])
                last_fields_list.append(field)
            print("2.1")
            last_embed = it.Embed(
                            title="\u200b",
                            description="\u200b",       
                            fields=last_fields_list,
                            color=0x00ff00)
            embeds_list.append(last_embed)  
            print("3")
            main_embed = it.Embed(
                              title=f"OwO",
                              description=f"Members Count : {self.members_count}\nTotal Xp : {self.total_xp}\nAverage Xp : {self.avg_xp}\n{self.leagues_names[order]}'s League",       
                              fields=[],
                              color=0x00ff00)   
            self.embeded_leagues.append([main_embed,embeds_list])
            order+=1
        print("4")
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

