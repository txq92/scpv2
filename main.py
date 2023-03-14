import requests, json , os ,shutil
import scpevn as evn
#from os import path
from zipfile import ZipFile

### Login
def login(username = "nghiais009", password = "15091994"):
    print("########### begin authen ###########")
    data = evn.API.authen(username, password)
    #print(data)
    print("########### done authen ###########")
    return data

def get_file(tokeni='xx', makkh='PB09010005862', nam='2023', thang='1' , idhd='1195292325'):

    print('Downloading started')

    #url = 'https://api.cskh.evnspc.vn/api/NghiepVu/TaiHoaDon?LoaiHoaDon=TD&strMaKhang=PB09010005862&iNam=2023&iThang=1&iKy=1&lIdHDon=1195292325'
    url = f'https://api.cskh.evnspc.vn/api/NghiepVu/TaiHoaDon?LoaiHoaDon=TD&strMaKhang={makkh}&iNam={nam}&iThang={thang}&iKy=1&lIdHDon={idhd}'
    headers = {
        'authorization': tokeni,
        'Content-Type': 'application/octet-stream',
    }

    req = requests.get(url, headers=headers)
    #print(req.text)
    # Split URL to get the file name
    namefomat = f"{makkh}_{nam}_{thang}_{idhd}"
    filename = namefomat+".zip"
    #PB09010005862_2023_1_1195292325
    # Writing the file to the local file system
    with open(filename,'wb') as output_file:
        output_file.write(req.content)

    print('Downloading OK')
    directory = os.getcwd()
    print(directory)

    ### unzip
    # loading the temp.zip and creating a zip object
    with ZipFile(filename, 'r') as zObject:
        zObject.extractall(path=directory)


    zObject.close()
    
    #xoa file zip
    os.remove(filename)
    os.remove('HoaDon.pdf')

    ####dich
    toopath = os.path.dirname(os.path.abspath(__file__))+'/store_data/'+ namefomat + '.xml'

    print(toopath)

    #move to foder store
    shutil.move('ChuKy.xml', toopath)

    print(f"Downloading Completed : {toopath}")
    return toopath

### Lay thong tin hoa don
def get_hoa_don(username="nghiais009", password="15091994",tuThang='1', tuNam='2023'):
    
    print("########### Begin get_hoa_don ###########")
    #data = authen(username, password)
    data = login(username, password)
    data = json.loads(data) # conver to json 
    tokeni = 'Bearer '+data['token']

    headers = {
        'authorization': tokeni,
        'accept': 'application/json',
        'Host': 'api.cskh.evnspc.vn',
    }

    #param
    strMaKH = data['maKH']
    params = {
        'strMaKH': strMaKH,
        'iTuThang': tuThang,
        'iTuNam': tuNam,
        'iDenNam': tuNam,
        'iDenThang': tuThang,
    }

    response = requests.get('https://api.cskh.evnspc.vn/api/NghiepVu/TraCuuHoaDon', params=params, headers=headers)

    data2 = response.text
    print(f"Ket qua hoa don thang {tuThang} - nam {tuNam}")
    #print(data2)
    jsondata = {}
        
    dataid = json.loads(data2)[0]
    rsp = get_file(tokeni,strMaKH, tuNam, tuThang , dataid['lId_HDon'])
    jsondata['result'] = "OK"
    jsondata['msg'] = f"Hoa Don Thang {tuThang} - {tuNam} Ghi File Thanh Cong"
    jsondata['path']= rsp
    jsondata['id_hoadon']=dataid['lId_HDon']
    '''
    try:
        dataid = json.loads(data2)[0]
        rsp = get_file(tokeni,strMaKH, tuNam, tuThang , dataid['lId_HDon'])
        jsondata['result'] = "OK"
        jsondata['msg'] = f"Hoa Don Thang {tuThang} - {tuNam} Ghi File Thanh Cong"
        jsondata['path']= rsp
        jsondata['id_hoadon']=dataid['lId_HDon']
    except Exception as ex:
        print(ex)
        jsondata['result'] = "ERROR"
        jsondata['msg'] = 'Exception'
        jsondata['id_hoadon']='NOT FOUND'
        jsondata['path']= f'Hoa Don Thang {tuThang} - {tuNam} Khong The Lay Data'
    '''
    print("########### End get_hoa_don ###########")
    #print(jsondata[0])
    #xml =  dicttoxml(jsondata)
    #print(xml)
    #print(type(jsondata))
    return jsondata

#get_file()
#print(get_hoa_don(username="nghiais009", password="15091994",tuThang='1', tuNam='2023'))