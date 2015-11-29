"""
	Project Bluebox
	2015, University of Stuttgart, IPVS/AS
"""
from itertools import count
""" 
	Project Bluebox 
	
	Copyright (C) <2015> <University of Stuttgart>
	
	This software may be modified and distributed under the terms
	of the MIT license.  See the LICENSE file for details.
"""

import base64
import requests
from swiftclient import client
import logging


# initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(module)s - %(levelname)s ##\t  %(message)s')
log = logging.getLogger()


#Function to connect to swift object store
class SwiftConnect:
		def __init__(self, swift_type, swift_url, swift_user, swift_pw):
			self.swift_url = swift_url
			self.swift_user = swift_user
			self.swift_pw = swift_pw
			
			if "BluemixV1Auth" == swift_type:
				self.doBluemixV1Auth()
			else:
				self.doRegularSwiftAuth()

			
		def doRegularSwiftAuth(self):
			log.debug("Connecting to regular swift at: {}".format(self.swift_url))
			self.conn = client.Connection(authurl=self.swift_url, user=self.swift_user, key=self.swift_pw)
			
		def doBluemixV1Auth(self):
			log.debug("Connecting to Bluemix V1 swift at: {}".format(self.swift_url))
			authEncoded = base64.b64encode(bytes('{}:{}'.format(self.swift_user, self.swift_pw),"utf-8"))
			authEncoded = "Basic "+ authEncoded.decode("utf-8")
			response =  requests.get(self.swift_url, 
			headers  =  {"Authorization": authEncoded})
			log.debug(response.headers['x-auth-token'])
			log.debug(response.headers['x-storage-url'])			
			self.conn = client.Connection(
				preauthtoken=response.headers['x-auth-token'],
				preauthurl=response.headers['x-storage-url']
				
		)

#####################################################################################################################################################################################

#Creating a Container
		def createContainer(self,folderName):
			log.debug("Inside create container")
			self.container_name = folderName
			self.conn.put_container(self.container_name)
			return True
			
			
#####################################################################################################################################################################################

#Creating an object
		def createObject(self,fileName,fileContent,folderName,metadataDict,content_length,chunk_size):
			log.debug(fileName)
			log.debug("Inside create Object")
			test=self.conn.put_object(container=folderName, obj= fileName, contents= fileContent,headers=metadataDict,chunk_size=10)
			log.debug=(test)
			
			
			
			
#####################################################################################################################################################################################                                        

#Retrieving an object 
		def retrieveObject(self,folderName,fileName):
			log.debug("Inside retrieve object")
			obj_tuple = self.conn.get_object(folderName,fileName)
			log.debug(obj_tuple[1])
			return obj_tuple[1]
		
#####################################################################################################################################################################################        
#Retrieving an object 
		def getObject(self,containernames,filename,resp_chunk_size):
			log.debug("Inside get object")
			log.debug(containernames)
			log.debug(filename)
			obj_tuple, body = self.conn.get_object(containernames,filename,resp_chunk_size)
			
			downloaded_contents=b''
			while True:
				try:
					chunk = next(body)
					log.debug(chunk)
				except StopIteration:
					break
				downloaded_contents=downloaded_contents+chunk
				log.debug(len(downloaded_contents))
# 			log.debug(obj_tuple[1]) # index [1] returns the file
# 			metadata=obj_tuple[0]
# 			log.debug("Content Length is:{}".format(metadata["content-length"]))
# 			log.debug(obj_tuple[0])
			return downloaded_contents[1]
################################################################################################       

#deleting an object 
		def delObject(self,containernames,filename):
			log.debug("Inside del object")
			log.debug(containernames)
			log.debug(filename)
			self.conn.delete_object(containernames, filename)

################################################################################################       

#deleting objects 
		def delObjects(self,containernames,filenames):
			log.debug("Inside del object")
			log.debug(containernames)
			for filename in filenames:        # Second Example
   				print ('Current file :', filename)
			   	log.debug(filename)
			   	self.conn.delete_object(containernames, filename)

####################################################################################################################################################
#Creating an container list
		def containerList(self, limit=8, marker=""):
 			
			log.debug("container List")
			containers = self.conn.get_account(marker=marker, limit=limit)[1]
			for container  in containers:
				log.debug(container ['name'])
 				
			return containers                    
#####################################################################################################################################################################################                                        

####################################################################################################################################################
#Creating an container list
		def containerListLimit(self,list,n):
 			#swift.conn.get_account(marker="Ali",limit=3)
			log.debug("container List")
			
			s = self.conn.get_account()[1][n]
			toString = str(s)
			toString.split(sep="name")
			x1=toString.split(sep="name")[1]
			inx1=x1.index(":")
			inx2=x1.index(",")
			mark=x1[inx1+3:inx2-1]
			
			containers = self.conn.get_account(limit=list,marker=mark)[1]
			
			for container  in containers:
				log.debug(container ['name'])
 				
			return containers                    
#####################################################################################################################################################################################                                        

####################################################################################################################################################
#Creating an container list
# 		def containerList(self):
#  			#swift.conn.get_account(marker="Ali",limit=3)
# 			log.debug("container List")
# 			containers = self.conn.get_account()[1]
# 			for container  in containers:
# 				log.debug(container ['name'])
#   				
# 			return containers                    
#####################################################################################################################################################################################                                        




#Creating an container list
		def fileList(self,containername , limit=6, marker=""):
			
			log.debug("Files in a container")
			files = self.conn.get_container(containername,full_listing=False ,limit=limit,marker=marker)[1]
			for file  in files:
				log.debug('{0}\t{1}\t{2}'.format(file['name'], file['bytes'], file['last_modified']))   
			return files                    
#####################################################################################################################################################################################                                        
#####################################################################################################################################################################################        

#Get
		def ObjectList(self,containername):
			
			log.debug("Files in a container")
			objects = self.conn.get_container(containername)[1]
			for object  in objects:
				log.debug('t{1}'.format( object['bytes']))  
				
				 
			return objects  



########################################### #####################################################    

#Retrieving an object Metadata 
		def getObjMetaData(self,containernames,filename):
			log.debug("Inside get object")
			log.debug(containernames)
			log.debug(filename)
			obj_tuple = self.conn.head_object(containernames,filename)
			log.debug(obj_tuple)  # index [0] returns the Headers of the file
			return obj_tuple
########################################### #####################################################    

						
#Closing the connection 
		def closeConnection(self):
			self.conn.close()
		
