from operator import inv
from bs4 import BeautifulSoup
import os
import glob

class XMLFile:
  def __init__(self, filename, filecontent, soup):
    self.filename = filename
    self.filecontent = filecontent
    self.soup = soup


def parse_xml(xml):
    with open(xml, 'r') as f:
        data = f.read()
        base = os.path.basename(xml)
        soup = BeautifulSoup(data, "xml")
        return XMLFile(base, data, soup)

def get_xmls(files):
    xmls = []
    for file in files:
        xml = parse_xml(file)
        xmls.append(xml)
    return xmls

def get_seller_org(xml):
    return xml.soup.find("SellerOrganisationName").text


def sanitize_org(org):
    """
    Add rules to sanitize the orgs here
    """
    sanitized = org.replace("?", "x") 
    return sanitized


def cluster_with_seller_org(xmls):
    dict = {}
    for xml in xmls:
        seller_org = sanitize_org(get_seller_org(xml))
        if seller_org not in dict:
            dict[seller_org] = []
        dict[seller_org].append(xml)    
    return dict

def join_with_cwd(*paths):
    return os.path.join(os.getcwd(), *paths) 


def create_dirs(path, dirs):
    for dir in dirs:
        dir_p = join_with_cwd(path, dir) 
        if(os.path.exists(dir_p)):
            continue
        else:
            os.makedirs(dir_p)

def write_xmls(path, dict):
    for key, value in dict.items():
        for xml in value:
            fp = join_with_cwd(path, key, xml.filename)
            with open(fp, 'w') as f:
                f.write(xml.filecontent)

def main():
    folder = ".data"
    running_dir = join_with_cwd(folder)
    files = glob.glob(f'{running_dir}/*')
    #files =  os.listdir(running_dir)
    xmls = get_xmls(files) #  
    dict = cluster_with_seller_org(xmls)
    dirs = [key for key in dict]
    create_dirs(".out", dirs)
    write_xmls(".out", dict)


if __name__ == "__main__":
    main()