#크롤링에 필요한 라이브러리 불러오기
import pandas as pd
import bs4 as bs
import requests
import re
#mariadb접속 라이브러리 불러오기
#pip install pymysql 필요
import pymysql
from sqlalchemy import create_engine,types

#크롤링 할 웹 사이트 선언
targetUrl = "https://www.musinsa.com/brands/musinsastandard?category3DepthCodes=&category2DepthCodes=&category1DepthCode=&colorCodes=&startPrice=&endPrice=&exclusiveYn=&includeSoldOut=&saleGoods=&timeSale=&includeKeywords=&sortCode=SALE_ONE_YEAR&tags=&page=1&size=90&listViewType=small&campaignCode=&groupSale=&outletGoods=&plusDelivery="

#오류로 인해 시스템이 뻗지 않게 try-except 명령어 실행
try:
    #크롤링 속도를 높이기 위한 user_agent 설정
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/5'
    resp = requests.get(targetUrl, headers={'User-Agent': user_agent})
    #정상값이 들어간 경우
    if resp.status_code == 200:
        html = resp.text
        soup = bs.BeautifulSoup(html, "html.parser")
        #찾고싶은 정보가 담긴 태그를 찾아 div라는 변수에 저장
        divs = soup.findAll("div",{"class" : "li_inner"})
    else:
        pass
except Exception as e:
    print(e)

#값이 잘 들어갔나 확인
len(divs)

#제품명, 가격, 좋아요 갯수 추출
productName_list = []
price_list = []
like_list = []

#값 처리를 위한 변수 선언
lenNum = 10
indexNum = 6
for i in range(0, len(divs)):
    #제품명 주출
    productName = divs[i].find("p", {"class" : "list_info"}).text
    productName_list.append(productName)
    #정규표현식을 사용한 전처리
    productName_list[i] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", productName_list[i])
    productName_list[i] = re.sub(" ","", productName_list[i])
    productName_list[i] = re.sub("\n","", productName_list[i])
    #가격 주출
    price = divs[i].find("p", {"class" : "price"}).text
    price_list.append(price)
    #정규표현식을 사용한 전처리
    price_list[i] = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", price_list[i])
    price_list[i] = re.sub(" ","", price_list[i])
    price_list[i] = re.sub("\n","", price_list[i])
    #값이 두개가 들어오는 경우를 대비해 기준을 잡고 원하는 값만 추출
    if len(price_list[i]) > lenNum:
        price_list[i] = price_list[i][indexNum:]
    #좋아요 갯수 주출
    like = divs[i].find("span", {"class" : "count"}).text
    like_list.append(like)

#값이 잘 들어갔나 확인
print(len(productName_list))
print(len(price_list))
print(len(like_list))

#데이터 프레임으로 씌우기
resultDf = pd.DataFrame(zip(productName_list,price_list,like_list))
#컬럼명 설정
resultDf.columns = (["product","price", "likeCount"])
resultDf

#데이터를 저장할 DB 접속 정보 기입
id = "root"
pw = "0000"
ip = "127.0.0.1"
port = "3306"
dbName = "web"

#DB 커넥션 열기
engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(id,pw,ip,port,dbName))

#생성할 테이블명 작성
tableName = "resultData"

#문자컬럼에 대해서 varchar (100) 적용 _ 사용시 속도 SpeedUp 50배
objectColumns = list(resultDf.columns[resultDf.dtypes == 'object'])
typeDict={}
maxLen = 100

for i in range(0, len(objectColumns)):
    # resultDf[i].str.len().max() 최대치 사용할 경우
    typeDict[objectColumns[i]] = types.VARCHAR(100)
#문자컬럼에 대해서 varchar (100) 적용 _ 사용시 속도 SpeedUp 50배

resultDf.to_sql(name=tableName, if_exists="replace", con=engine,dtype=typeDict, index=False)
