import argparse
from apiclient.discovery import build
from apiclient.http import BatchHttpRequest
import httplib2
from oauth2client import client
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import file
from oauth2client import tools
import datetime
import pandas as pd
import json 
import pickle as pickle
import string
import urllib.request
import numpy as np
import time     
import re
import abc
from abc import ABCMeta, abstractmethod




class Product(object):
    ## Version and Name Product
    def __init__(self):
        
        self.__settings_products = pd.DataFrame([])
        self.__schema_product_name = ['analytics']
        self.__schema_product_value = ['v3']
        self.__product_api = 'product_api'
        self.__product_version = 'product_version'
        self.set_settings_products(**{'analytics':'v3'})
        
    def set_settings_products(self,**settings_products):
        
        obj={}
        self.selected = 'Select'
        self.format = 'Format'
        self.formatlang = 'DataFrame'

        self.__error_key = [key for key in settings_products.keys() if key in self.__schema_product_name]
        self.__error_value = [key for key in settings_products.values() if key in self.__schema_product_value]
        self.new_settings_product = dict(zip(self.__error_key,self.__error_value))

        for key in self.new_settings_product:
            obj[self.__product_api]=key
            obj[self.__product_version]=self.new_settings_product[key]
            self.__settings_products = self.__settings_products.append(obj,ignore_index=True)
            self.__settings_products.index.name = 'ID'
            Product.select_products(self,0)
            self.choose_output()
        return self
        
    def del_products(self,index):
        self.__settings_products = self.__settings_products[self.__settings_products.index.values!=index]
        return self
        
    def select_products(self,index):
        self.__settings_products[self.selected] = ''
        self.__settings_products[self.selected][self.__settings_products.index.values==index]=self.selected
        return self.__settings_products

    def choose_output(self,format='DataFrame'):
        self.__settings_products[self.format] = ''
        self.__settings_products[self.format][self.__settings_products[self.selected]==self.selected] = format
        return self.__settings_products


    def get_all_products(self,clarify=None):
        if clarify:
            return self.__settings_products[clarify][0]
        else:
            return self.__settings_products

    def get_select_products(self):
        return self.__settings_products[self.__settings_products['Selected']=='Select']
    


class Connection(object):
    
    def __init__(self,key_file_location,type_of_connection):

        self.__settings_connection = pd.DataFrame([])
        self.__scopes = ['https://www.googleapis.com/auth/analytics.readonly']
        self.__discovery_uri = ('https://analyticsreporting.googleapis.com/$discovery/rest')
        self.__filestorage = 'analyticsreporting.dat'
        self.__analytics_connect = ''

        self.set_settings_connect(type_of_connection,key_file_location)
    
    def set_settings_connect(self,type_of_connection,key_file_location):
        self.__settings_connection = pd.DataFrame([{
                    'type_of_connection':type_of_connection,
                    'key_file_location':key_file_location,
                    'scopes':self.__scopes
                }])        
        return self
    
    def get_settings_connect(self,clarify=None):
        if clarify:
            return self.__settings_connection[clarify][0]
        else:
            return self.__settings_connection
            
    def _execute_settings_connect(self):
        
        # credintials for server or client 

        if self.get_settings_connect('key_file_location') != None and self.get_settings_connect('type_of_connection') != None:
            if self.get_settings_connect('type_of_connection')=='Server':
                credentials = ServiceAccountCredentials.from_json_keyfile_name(self.get_settings_connect('key_file_location'), self.get_settings_connect('scopes'))
            if self.get_settings_connect('type_of_connection')=='Client':
                parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,parents=[tools.argparser])
                flags = parser.parse_args([])
                flow = client.flow_from_clientsecrets(self.get_settings_connect('key_file_location'),scope=self.get_settings_connect('scopes'),message=tools.message_if_missing(self.get_settings_connect('key_file_location')))
                storage = file.Storage(self.__filestorage)
                credentials = storage.get()
                if credentials is None or credentials.invalid:
                    credentials = tools.run_flow(flow, storage, flags)

        # Аутентификация и создание службы.
        
        http = credentials.authorize(http=httplib2.Http())
        self.__analytics_connect = build(self.get_all_products('product_api'), self.get_all_products('product_version'), http=http)
        return self
    
    def _get_analytics_connect(self):
        return self.__analytics_connect



class Batch(object):
    
    def __init__(self):
        
        self.__raw_request = []
        
        self.__header_columns_name = []
        self.__dimension_gua_name = []
        self._metric_gua_name = []

        self.__obj = {}
        self.__frame = []
        self.__flag = 0

    
    def get_dmh_name(self,clarify=None):
        if clarify == 'DIMENSION':
            return self.__dimension_gua_name
        if clarify == 'METRIC':
            return self._metric_gua_name
        if clarify == 'HEADER':
            return self.__header_columns_name

    def get_raw_request(self):
        return self.__raw_request

    def call_back_bathing_all_day(self,request_id, response, exception):
        if response == None:
            print(exception)
            return False
        self.set_total_raw(request_id,response.get('totalResults'))
        return self.add_frame(request_id,response)

    def call_back_bathing_all_day_all_page(self,request_id, response, exception):
        if response == None:
            print(exception)
            return False
        # print('Exception call_back_bathing_all_day_all_page =',exception)
        # print('Request id call_back_bathing_all_day_all_page',request_id)
        return self.add_frame(request_id,response)


    def add_frame(self,rid,response):
        try:
            for header in response.get('columnHeaders'):
                self.__header_columns_name.append(header.get('name'))
                
                if header.get('columnType')=='DIMENSION' and self.__flag==0:
                    self.__dimension_gua_name.append(header.get('name'))

                if header.get('columnType')=='METRIC' and self.__flag==0:
                    self._metric_gua_name.append([header.get('name'),header.get('dataType')])
                    print(self._metric_gua_name)

            if response.get('rows', []):
                for row in response.get('rows'):
                    self.__obj = {}
                    for i,cell in enumerate(row):
                        self.__obj[self.__header_columns_name[i]]=cell
                        # self.__obj['count_day_slice']=rid
                    self.__frame.append(self.__obj)
                self.__flag = 1
                return self.__frame
        except AttributeError:
            print('No Data Gua')


    def _get_main_frame_object(self):
        return self.__frame

    def create_batching(self,system):
        self.bathing = system.new_batch_http_request()
        return self

    def add_batching(self,cb,request,request_id):
        # print('add_batching')
        self.bathing.add(callback=cb,request=request,request_id=request_id)
        return self

    def execute_batching(self):
        time.sleep(0.5)
        self.bathing.execute(http=httplib2.Http())
        return self

    def get_bathing(self):
        return self.bathing

    def _main_alogrithm_batching(self,dayall,analytics):
        day_chunk = self.split_numpy(dayall)      
        # start_time = time.clock()
        for day_chunk_split in day_chunk:
            self.create_batching(analytics)
            print(day_chunk_split)
            for day in day_chunk_split:
                day['pagetoken']=0
                # print(day)
                self.add_settings_request(**day)
                self.add_batching(cb=self.call_back_bathing_all_day,request=self.fill_raw_request(analytics),request_id=day['start_date']+'_'+day['end_date'])
            # print('This<--------------------')
            self.execute_batching()
            # elapsed = (time.clock() - start_time)
            # print('Tinme this Query',elapsed)
        if self.get_total_raw():
            print('Total row is TRUE')
            self.create_batching(analytics)    
            day_and_pagetoken_all = self.get_numpy_list_day_with_over_row(self.get_total_raw())
            day_and_pagetoken_chunk = self.split_numpy(day_and_pagetoken_all)
            for day_and_pagetoken_chunk_split in day_and_pagetoken_chunk:
                self.create_batching(analytics)
                for day_pagetoken in day_and_pagetoken_chunk_split:
                    print(day_pagetoken)
                    day = {
                        'start_date':day_pagetoken.split('__')[0].split('_')[0],
                        'end_date':day_pagetoken.split('__')[0].split('_')[1],
                        'pagetoken':day_pagetoken.split('__')[1]
                    }
                    self.add_settings_request(**day)
                    self.add_batching(cb=self.call_back_bathing_all_day_all_page,request=self.fill_raw_request(analytics),request_id=None)
                # print('That<--------------------')
                self.execute_batching()






class ExtraAppsMetaCdm(object):
    
    __metaclass__ = abc.ABCMeta

    def __init__(self,metacdm=None):
        
        self.__settings_meta_cdcm = metacdm or pd.DataFrame([])
        self.__url_metadataapi = 'https://www.googleapis.com/analytics/v3/metadata/ga/columns'
    
    @abstractmethod
    def get_list_cdcm(self,clarify=None):
        pass 

    
    def get_url(self,url):
        self.url_request = urllib.request.urlopen(url).read()
        return self.url_request
        
    def __get_now_schema(self):
        obj = []
        resp = json.loads(self.get_url(self.__url_metadataapi).decode('utf8')).get("items")
        for i in resp:
            obj.append({
                'name':i.get('id'),
                'type':i.get('attributes').get('type'),
                'status':i.get('attributes').get('status'),
                'description':i.get('attributes').get('description')
                })
        return obj
    
    



class ExtraAppsManagementApi(object):
    
    def __init__(self,management=None):
        
        self.__settings_managment_api = management or pd.DataFrame([])
        self.analytics = self._execute_settings_connect()._get_analytics_connect()
        self.accounts = self.analytics.management().accounts().list().execute()
    
        
    def __get_now_schema(self):
        obj = []
        for i in self.accounts.get('items'):
            print(i)
            # obj.append({
            #     'name':i.get('id'),
            #     'type':i.get('attributes').get('type'),
            #     'status':i.get('attributes').get('status'),
            #     'description':i.get('attributes').get('description')
            #     })
        # return obj

    
    def get_all_property(self,clarify=None):
        print(self.__get_now_schema())
        # self.clarify=clarify
        # self.__settings_meta_cdcm = pd.DataFrame(self.__get_now_schema())
        # # print(self.__settings_meta_cdcm)
        # if not self.clarify:
        #     return self.__settings_meta_cdcm[['name','description','status','type']]
        # else:
        #     return self.__settings_meta_cdcm[['name','description','status','type']][self.__settings_meta_cdcm['name'].str.contains(self.clarify,regex=True)]





class Request(Batch):


    __metaclass__ = abc.ABCMeta

    def __init__(self,facet_chunk,count_day_slice,pagesize=10000,pagetoken=0):
    
        self.__settings_request = pd.DataFrame([])
        self.__settings_meta_cdcm = pd.DataFrame([])
        self.__settings_raw_request = pd.DataFrame([])
        
        
        self.set_settings_request(**{
            'ids':'',
            'start_date':'',
            'end_date':'',
            'filters':'',
            'facet_chunk':facet_chunk,
            'pagesize':pagesize,
            'count_day_slice':count_day_slice,
            'pagetoken':pagetoken,
            'segment':'',
            'samplingLevel':'',
            'sort':'',
            'include-empty-rows':'',
            'output':'',
            'fields':'',
            'prettyPrint':'',
            'userIp':'',
            'quotaUser':'',
            'access_token':'',
            'quotaUser':'',
            'metrics':'',
            'dimensions':''
            })
        
        self.obj = []
        self.day = {}
        self.day_with_over_row = []

        
        self.total_raw = []
        self.verify = 0
        
    

    def add_settings_request(self,**settings_products):
        if self.get_settings_request().empty:
            raise NameError('First of all, you need set settings request')  
        else:
            self.get_settings_request().update([settings_products])
            return self
    
    def set_settings_request(self,**settings_products):
        self.__settings_request = pd.DataFrame([settings_products])
        return self 


    def get_settings_request(self,clarify =None):
        if(not clarify):
            return self.__settings_request
        else:
            return self.__settings_request[clarify][0]

    def fill_raw_request(self,analytics):
        return analytics.data().ga().get(
                  ids=self.get_settings_request('ids') or None,
                  start_date=self.get_settings_request('start_date') or None,
                  end_date=self.get_settings_request('end_date') or None,
                  metrics=self.get_settings_request('metrics') or None, 
                  dimensions=self.get_settings_request('dimensions')or None,
                  samplingLevel=self.get_settings_request('samplingLevel') or None,
                  filters=self.get_settings_request('filters') or None,
                  segment=self.get_settings_request('segment') or None,
                  max_results=self.get_settings_request('pagesize') or None,
                  start_index=int(self.get_settings_request('pagetoken')) + 1,
                  sort=self.get_settings_request('sort') or None,
                  output=self.get_settings_request('output') or None,
                  fields=self.get_settings_request('fields') or None,
                  prettyPrint=self.get_settings_request('prettyPrint') or None,
                  userIp=self.get_settings_request('userIp') or None,
                  quotaUser=self.get_settings_request('quotaUser') or None
                )

    def get_total_raw(self):
        return self.total_raw

    def set_total_raw(self,day,total):
        self.verify+=total
        print(self.verify)
        if total > self.get_settings_request('pagesize'):
            self.total_raw.append({'day':day,'total':[element for element in range(self.get_settings_request('pagesize'),total,self.get_settings_request('pagesize'))]})
        return self

        
    def split_numpy(self,numpy_list,facet_chunk=None):
        facet_chunk = facet_chunk or self.get_settings_request('facet_chunk')
        full = numpy_list.size // facet_chunk
        short = numpy_list.size % facet_chunk
        if short > 0:
            full += 1 
        numpy_list = np.array_split(numpy_list,full)
        return numpy_list


    def convert_str_to_datetime(self,sd=None,ed=None):
        sd = sd or self.get_settings_request('start_date').split('-')
        ed = ed or self.get_settings_request('end_date').split('-') 
        range_day = [[int(x) for x in sd],[int(x) for x in ed]]
        range_day = [datetime.date(range_day[0][0],range_day[0][1],range_day[0][2]),datetime.date(range_day[1][0],range_day[1][1],range_day[1][2])]
        return range_day



    def generate_range_datetime(self,count_day_sum=None,range_day=None):
        convertday = []
        count_day_sum = count_day_sum or 1
        range_day = range_day or self.convert_str_to_datetime()

        while range_day[1] >= range_day[0]:    
            convertday.append(range_day[0].strftime('%Y-%m-%d'))
            range_day[0] = range_day[0] + datetime.timedelta(days=int(count_day_sum))
        return np.array(convertday) 



    def _split_by_count_day_range_datetime(self,count_day_slice):
        convertdaystartend = []
        range_day = self.generate_range_datetime()        
        if count_day_slice > 1:
            for s,e in zip(range_day[0::count_day_slice],range_day[count_day_slice-1::count_day_slice]):
                convertdaystartend.append({'start_date':s,'end_date':e})
            short = range_day.size % count_day_slice
            if not not short:
                convertdaystartend.append({'start_date':range_day[-short],'end_date':range_day[len(range_day)-1]})
        else:
            for s,e in zip(range_day[0:],range_day[0:]):
                convertdaystartend.append({'start_date':s,'end_date':e})   

        return np.array(convertdaystartend)

    def get_numpy_list_day_with_over_row(self,total):
        day_with_over_row = []
        for day_with_over_row_total in total:
            for row_size in day_with_over_row_total['total']:
                day_with_over_row.append(str(day_with_over_row_total['day'])+'__'+str(row_size))
        return np.array(day_with_over_row)


class PandasEvents(object):

    
    def __init__(self,metric,dimension,groupby,cv3_main_frame_object=None):
        
        
        self.__groupby = groupby
        self.__cv3_main_frame_object = cv3_main_frame_object
        self.__metric_gua_name = metric
        self.__dimension_gua_name = dimension

        if len(self.get_cv3_pandas_data_frame()):
            self.__cv3_main_frame_object = self.__set_list_type_df(self.get_cv3_pandas_data_frame())
        
        if groupby:
            self.__cv3_main_frame_object = self.__groupby_cv3_df(self.get_cv3_pandas_data_frame())

    def get_cv3_pandas_data_frame(self):
        return pd.DataFrame(self.__cv3_main_frame_object)

    def _get_cv3_main_frame_object(self):
        return self.__cv3_main_frame_object

    def __set_list_type_df(self,df):
        for i_,q_ in enumerate(self.__metric_gua_name):
            for i__,q__ in enumerate(q_):
                if q__ in ('INTEGER'):
                    self.__metric_gua_name[i_].append('int')
                    df[self.__metric_gua_name[i_][0]] = df[self.__metric_gua_name[i_][0]].astype('int')
                if q__ in ('FLOAT','PERCENT','CURRENCY','TIME'):
                    self.__metric_gua_name[i_].append('double')
                    df[self.__metric_gua_name[i_][0]] = df[self.__metric_gua_name[i_][0]].astype('double')
        return df

    def __groupby_cv3_df(self,df):
        # df = df.set_index(self.__dimension_gua_name)
        df = df.groupby(self.__dimension_gua_name).agg(['sum','mean'])
        return df.reset_index()









class PGA(Product,PandasEvents,Connection,Request,ExtraAppsMetaCdm,ExtraAppsManagementApi):
    
    __metaclass__ = ABCMeta

    def __init__(self,key_file_location=None,type_of_connection=None,facet_chunk=9,count_day_slice=1):
        


        '''
        Main Class 
        
        '''
        # ExtraAppsMetaCdm.register(PGA)

        # ExtraAppsMetaCdm.__init__(self)
        if not not (key_file_location and type_of_connection):
            Product.__init__(self)
            Connection.__init__(self,key_file_location,type_of_connection)
            ExtraAppsManagementApi.__init__(self)
            Request.__init__(self,facet_chunk,count_day_slice)
            Batch.__init__(self)
        

    def get_all_settings(self):
        return pd.concat([self.get_settings_request(),self.get_settings_connect(),self.get_all_products()],axis=1)


    def get_list_cdcm(self,clarify=None):
        self.clarify=clarify
        self.__settings_meta_cdcm = pd.DataFrame(self.__get_now_schema())
        if not self.clarify:
            return self.__settings_meta_cdcm[['name','description','status','type']]
        else:
            return self.__settings_meta_cdcm[['name','description','status','type']][self.__settings_meta_cdcm['name'].str.contains(self.clarify,regex=True)]


    def execute_dataframe(self):
        analytics = self._execute_settings_connect()._get_analytics_connect()
#         print(analytics.management().accounts().list().execute())
        countday = self.get_settings_request('count_day_slice')
        dayall = self._split_by_count_day_range_datetime(countday)
        self._main_alogrithm_batching(dayall,analytics)
        cv3_main_frame_object = self._get_main_frame_object()
        return pd.DataFrame([cv3_main_frame_object])

    def group_cv3_data_frame(self,groupby):
        cv3_pandas_data_frame = PandasEvents.__init__(self,self.get_dmh_name('METRIC'),self.get_dmh_name('DIMENSION'),groupby,PandasEvents._get_cv3_main_frame_object(self))
        cv3_pandas_data_frame = self.get_cv3_pandas_data_frame()
        return cv3_pandas_data_frame


# pga = PGA('/home/akulbasov/Desktop/client_secret_963693226661-vhh41ngqrs9u2v70umi8oh70njtslqph.apps.googleusercontent.com.json','Client',10,5)
# # pga = PGA('./My Project-554752157a4c.json','Server',9,3)
# pga.add_settings_request(**{'ids':'ga:54989285',
#                             'start_date' : '2016-12-01',
#                             'end_date' : '2016-12-01',
#                             'metrics' : 'ga:pageviews',
#                             # 'filters':'ga:source=@google',
#                             'dimensions' : 'ga:pageDepth'})
# # pga = PGA()
# # pga.execute_dataframe()
# # a = PGA()
# # a.get_list_cdcm('transaction')
# # pga.get_all_settings()
# # pga.get_list_cdcm('page')
# t = pga.execute_dataframe()
# b = pga.group_cv3_data_frame(True)
# b = pga.groupby
