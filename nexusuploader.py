####################################################################################
#      Developed by Alireza Khatami Doost                                          #
#      These addresses must be modified according to your Nexus server target.     #
####################################################################################
ADDRESS_REPOSITORY = '/home/alireza/.m2/repository'
NEXUS_REPOSITORY_ID = 'nexus-maven-public'
ADDRESS_NEXUS = 'http://repo.vasit.mcci.local:8081/repository/maven.group'
ADDRESS_NEXUS_UPLOAD = 'http://repo.vasit.mcci.local:8081/repository/maven.central'
ADDRESS_NEXUS_SNAPSHOT = 'http://repo.vasit.mcci.local:8081/repository/maven.group.snapshot'

# Pattern of maven request.
PATTERN = 'mvn deploy:deploy-file -DgroupId={} -DartifactId={} -Dversion={} -Dpackaging=jar -Dfile={} -DgeneratePom=true -Durl={} -Dclassifier=linux-x86-64'

FILTER = ''

import glob, os
from tokenize import group

from click import command

class JarFileInfo:
    
    def __init__(self, address: str, group_id: str, artifact_id: str, version: str) -> None:
        self.address = address
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
    
    def __str__(self) -> str:
        return 'address: {},\ngroupId: {},\nartifactId: {}\n'.format(self.address, self.group_id, self.artifact_id)

def find_group_id(jar_file_address: str) -> str:
    root = jar_file_address.replace(ADDRESS_REPOSITORY, '')
    seps = root.split('/')
    rsp = ''
    for sep in seps[:-3]:
        rsp += sep + '.'
    return rsp[1:-1]

def find_artifact_id(jar_file_address: str) -> str:
    root = jar_file_address.replace(ADDRESS_REPOSITORY, '')
    seps = root.split('/')
    return seps[-3]

def find_version(jar_file_address: str) -> str:
    root = jar_file_address.replace(ADDRESS_REPOSITORY, '')
    seps = root.split('/')
    return seps[-2]

def find_jar_file(address: str) -> list:
    jar_list = []
    search_address = address
    for i in range(15):
        search_address += '/*'
        for name in glob.glob(search_address + ".jar"):
            if '.jar' in name:
                _group_id = find_group_id(name)
                _artifact_id = find_artifact_id(name)
                _version = find_version(name)
                if FILTER in _group_id:
                    jar_file = JarFileInfo(name, _group_id, _artifact_id, _version)
                    jar_list.append(jar_file)
    return jar_list

def upload_into_nexus(file_info: JarFileInfo):
    print('[>>] Upload dependency: {}'.format(file_info.address))
    mvn_commmand = PATTERN.format(file_info.group_id, file_info.artifact_id, file_info.version, file_info.address, ADDRESS_NEXUS_UPLOAD)
    print('[>>] Command: {}'.format(mvn_commmand))
    os.system(mvn_commmand)

all_jar_files = find_jar_file(ADDRESS_REPOSITORY)
print("[+] Start ....")
for jar_file in all_jar_files:
    upload_into_nexus(jar_file)
print("[+] Done.")
