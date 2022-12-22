#encoding:utf8
import os
import re
import json
import codecs
import threading
from py2neo import Graph
import pandas as pd 
import numpy as np 
from tqdm import tqdm 

def print_data_info(data_path):
    triples = []
    i = 0
    with open(data_path,'r',encoding='utf8') as f:
        file = json.loads(f.read())
        # print(file)
        for line in file:
            # data = json.loads(line)
            print(json.dumps(line, sort_keys=True, indent=4, separators=(', ', ': '),ensure_ascii=False))
            i += 1
            if i >=5:
                break
    return triples

class MedicalExtractor(object):
    def __init__(self):
        super(MedicalExtractor, self).__init__()

        self.graph = Graph(
            host="localhost",
            http_port=7474,
            user="neo4j",
            password="123456")

        # 共8类节点
        self.city = [] # 城市
        self.district = [] #区
        self.scenery = [] #　景点 属性：开放时间、级别、设施项目
        # self.level = [] # 等级
        # self.ticket = [] #门票
        # self.season = [] #季节
        # self.opentime = [] #开放时间
        self.hotel = []#酒店
        self.food = []#特色美食
        # self.score = []#评分
        self.history = []#历史事件/人物
        self.detail = [] #景区特色
        self.scenery_info = [] #景区特色


        # 构建节点实体关系
        self.rels_sceCity = []
        self.rels_notdistrict = [] # 景区－区域关系
        self.rels_dolevel = [] # 景区－等级关系
        self.rels_sceticket = [] # 景区－门票关系
        self.rels_season = [] # 景区－季节关系
        self.rels_opening = [] # 景区－开放时间关系
        self.rels_food = [] # 景区－特色美食关系
        self.rels_city_hotel = [] # 城市－酒店关系
        self.rels_history = [] # 景区—历史事件/历史人物关系
        self.rels_notscore=[]#景区和得分之间的关系
        # self.rels_scenery = [] #景区之间的关系
        # self.rels_city = [] #　城市－景区关系
        self.rels_detail = [] #　景区与特色之间的关系
        
    def extract_triples(self,data_path):
        print("从json文件中转换抽取三元组")
        with open(data_path,'r',encoding='utf8') as f:
            file = json.loads(f.read())
            for data_json in file:      #tqdm(f.readlines(),ncols=80)
                # data_json = json.loads(line)
                scenery_dict = {}
                scenery = data_json['name']
                scenery_dict['name'] = scenery
                district = data_json['area']
                city = data_json['city']
                self.scenery.append(scenery)
                scenery_dict['score'] = ''
                scenery_dict['season'] = ''
                scenery_dict['opentime'] = ''
                scenery_dict['level'] = ''
                if 'city' in data_json:
                    if city != '':
                        self.city.append(city)
                        self.rels_sceCity.append([scenery,'sceIn',city])
                # if 'city' in data_json:
                #     city = data_json['city']
                #     self.city.append(city)
                #     # for _city in city:
                #     self.rels_city.append([scenery,'in_city',city])
                if 'area' in data_json:

                    # for area in data_json['area']:
                    if district != '':
                        self.district.append(district)
                        self.rels_notdistrict.append([scenery,'in_area',district])
                    # for city in data_json['city']:

                # #景区的属性
                if 'detail' in data_json:
                    detail = data_json['detail']
                    # print(list(detail))
                    if detail!='':
                        detail_list=detail.replace("[","").replace("]","").replace("'","").replace("'","").replace("/","").split(",")

                    for item in detail_list:
                        if item != '':
                            # for item in detail[i]:
                            # _detail=re.sub(u'([^\u4e00-\u9fa5])','',detail[i])
                            # print(item)
                            self.detail.append(item)
                            self.rels_detail.append([scenery,'is_detail', item])



                if 'score' in data_json:
                    scenery_dict['score'] = data_json['score']

                if 'level' in data_json:
                    scenery_dict['level'] = data_json['level']

                if 'season' in data_json:
                    scenery_dict['season'] = data_json['season']

                if 'ticket' in data_json:
                    scenery_dict['ticket'] = data_json['ticket']




                if 'level' in data_json:
                    level = data_json['level']
                    for _level in level:
                        self.rels_dolevel.append([scenery,'has_level', _level])
                    # self.level += level

                if 'score' in data_json:
                    score = data_json['score']
                    # self.score += score
                    for _score in score:
                        self.rels_notscore.append([scenery,'has_score', _score])
                    # self.score += score

                if 'famous' in data_json:
                    famous = data_json['famous']
                    if famous != '':
                        famous_list=famous.replace("[","").replace("]","").replace("'","").replace("'","").replace("/","").split(",")

                    for _famous in  famous_list:
                        # _famous=re.sub(u'([^\u4e00-\u9fa5])','',famous[i])
                        if _famous!='':
                            # print(_famous)
                            self.history.append(_famous)
                            self.rels_history.append([scenery,'is_related', _famous])


                if 'food' in data_json:
                    food = data_json['food']
                    if food != '':
                        # print(food)
                        food= food.split('、')
                        for _food in food:
                            self.food.append(_food)
                            self.rels_food.append([scenery,'recommand_food', _food])

                if 'opentime' in data_json:
                    opentime = data_json['opentime']
                    for _opentime in opentime:
                        self.rels_opening.append([scenery, 'open_time', _opentime])
                    # self.opentime += opentime

                if 'ticket' in data_json:
                    ticket = data_json['ticket']
                    for _ticket in ticket:
                        self.rels_sceticket.append([scenery, 'ticket_price', _ticket])
                    # self.ticket += ticket

                if 'season' in data_json:
                    season = data_json['season']
                    for _season in season:
                        self.rels_season.append([scenery, 'fit_season', season])
                    # self.season += season

                # district = data_json['area']
                # if 'city' in data_json:
                #     city = data_json['city']
                #     for _season in season:
                #         self.rels_season.append([district, 'in_city', city])
                #     self.city += city

                # if 'drug_detail' in data_json:
                #     for det in data_json['drug_detail']:
                #         det_spilt = det.split('(')
                #         if len(det_spilt) == 2:
                #             p,d = det_spilt
                #             d = d.rstrip(')')
                #             if p.find(d) > 0:
                #                 p = p.rstrip(d)
                #             self.producers.append(p)
                #             self.drugs.append(d)
                #             self.rels_drug_producer.append([p,'production',d])
                #         else:
                #             d = det_spilt[0]
                #             self.drugs.append(d)
                #
                self.scenery_info.append(scenery_dict)
            print(self.rels_sceCity)
            print(self.rels_notdistrict)

    def write_nodes(self,entitys,entity_type):
        # print("写入 {0} 实体".format(entity_type))
        for node in tqdm(set(entitys),ncols=80):
            cql = """MERGE(n:{label}{{name:'{entity_name}'}})""".format(
                label=entity_type,entity_name=node.replace("'",""))
            # print(cql)
            try:
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)

    def write_edges(self,triples,head_type,tail_type,name_type):

        for head,relation,tail in tqdm(triples,ncols=80):
            cql = """MATCH(p:{head_type}),(q:{tail_type})
                    WHERE p.name='{head}' AND q.name='{tail}'
                    MERGE (p)-[r:{relation} {{name:'{name_type}'}}]->(q)""".format(
                        head_type=head_type,tail_type=tail_type,name_type=name_type,head=head.replace("'",""),
                        tail=tail.replace("'",""),relation=relation)
            # print(cql)
            try:
                self.graph.run(cql)
            except Exception as e:
                print(e)
                print(cql)

    def set_attributes(self,entity_infos,etype):
        print("写入 {0} 实体的属性".format(etype))
        for e_dict in tqdm(entity_infos,ncols=80):
            name = e_dict['name']
            del e_dict['name']
            for k,v in e_dict.items():
            #     if k in ['cure_department','cure_way']:
            #         cql = """MATCH (n:{label})
            #             WHERE n.name='{name}'
            #             set n.{k}={v}""".format(label=etype,name=name.replace("'",""),k=k,v=v)
            #     else:
                cql = """MATCH (n:{label})
                    WHERE n.name='{name}'
                    set n.{k}='{v}'""".format(label=etype,name=name.replace("'",""),k=k,v=v.replace("'","").replace("\n",""))
                try:
                    self.graph.run(cql)
                except Exception as e:
                    print('失败')
                    # print(cql)


    def create_entitys(self):
        self.write_nodes(self.city,'城市')
        self.write_nodes(self.district,'区域')
        # self.write_nodes(self.level,'等级')
        # self.write_nodes(self.score,'评分')
        self.write_nodes(self.food,'特色美食')
        self.write_nodes(self.history,'历史事件')
        # self.write_nodes(self.ticket,'门票')
        # self.write_nodes(self.opentime,'开放时间')
        # self.write_nodes(self.season,'适宜季节')
        self.write_nodes(self.detail,'景区特色')
        self.write_nodes(self.scenery,'景区')

    def create_relations(self):
        self.write_edges(self.rels_sceCity,'景区','城市','所在城市')
        self.write_edges(self.rels_notdistrict,'景区','区域','所在地区')
        # self.write_edges(self.rels_dolevel,'景区','等级')
        # self.write_edges(self.rels_sceticket,'景区','门票')
        # self.write_edges(self.rels_season,'景区','适宜季节')
        # self.write_edges(self.rels_opening,'景区','开放时间')
        self.write_edges(self.rels_detail,'景区','景区特色','推荐游玩')
        self.write_edges(self.rels_food,'景区','特色美食','推荐美食')
        self.write_edges(self.rels_history,'景区','历史事件','历史相关')
        # self.write_edges(self.rels_notscore,'景区','评分','')

    # self.write_edges(self.rels_city_hotel,'疾病','科室')

    def set_diseases_attributes(self): 
        self.set_attributes(self.scenery_info,"景区")
        # t=threading.Thread(target=self.set_attributes,args=(self.scenery_info,"景区"))
        # t.setDaemon(False)
        # t.start()


    # def create_relationship(self,start_node,end_node,edges,rel_type,rel_name):
    #     count=0
    #     set_edges = []
    #     for edge in edges:
    #         set_edges.append('###'.join(edge))
    #     all = len(set(set_edges))
    #     for edge in set(set_edges):
    #         edge = edge.split('###')
    #         p = edge[0]
    #         q = edge[1]
    #         query = "match(p:%s),(q:%s) where p.name='s%s' and q.name='s%s' create(p)-[rel:%s{name:'s%ds'}]->(q)"%(start_node,end_node,p,q,rel_type,rel_name)
    #         try:
    #             self.graph.run(query)
    #             count +=1
    #             print(rel_type,count,all)
    #         except Exception as e:
    #             print(e)


    def export_data(self,data,path):
        if isinstance(data[0],str):
            data = sorted([d.strip("...") for d in set(data)])
        with codecs.open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def export_entitys_relations(self):
        self.export_data(self.city,'./graph_data/city.json')
        self.export_data(self.district,'./graph_data/district.json')
        # self.export_data(self.level,'./graph_data/level.json')
        # self.export_data(self.score,'./graph_data/score.json')
        self.export_data(self.food,'./graph_data/food.json')
        self.export_data(self.history,'./graph_data/history.json')
        # self.export_data(self.ticket,'./graph_data/ticket.json')
        # self.export_data(self.opentime,'./graph_data/opentime.json')
        # self.export_data(self.season,'./graph_data/season.json')
        self.export_data(self.scenery,'./scenery.json')

        self.export_data(self.rels_notdistrict,'./graph_data/rels_notdistrict.json')
        self.export_data(self.rels_dolevel,'./graph_data/rels_dolevel.json')
        self.export_data(self.rels_sceticket,'./graph_data/rels_sceticket.json')
        self.export_data(self.rels_season,'./graph_data/rels_season.json')
        self.export_data(self.rels_opening,'./graph_data/rels_opening.json')
        self.export_data(self.rels_detail,'./graph_data/rels_food.json')
        self.export_data(self.rels_food,'./graph_data/rels_food.json')
        self.export_data(self.rels_history,'./graph_data/rels_history.json')
        self.export_data(self.rels_notscore,'./graph_data/rels_notscore.json')





if __name__ == '__main__':
    path = "new.json"
    # print(print_data_info(path))
    extractor = MedicalExtractor()
    extractor.extract_triples(path)
    extractor.create_entitys()
    extractor.create_relations()
    extractor.set_diseases_attributes()
    # extractor.export_entitys_relations()
