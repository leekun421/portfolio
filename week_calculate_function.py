from isoweek import Week
#주 차이 구하기
def weekCal (inputYrWk, inputMinusWk):
    """
    #inputYrWk은 str타입으로 입력. ex)"201710"
    #inputMinusWk은 str, int타입 둘다 가능. ex)"200"
    #result는 최종적으로 주어진 값에 뺄 주차를 계산한 최종 결과가 담긴다.(str형태로 담긴다.)
    """
    #inputYrWk(201710)에서 맨앞에서 인덱스 3번까지 값을 year에 넣는다.
    year = inputYrWk[:4] 
    #inputYrWk(201710)에서 인덱스 4번부터 맨끝까지 값을 week에 넣는다.
    week = inputYrWk[4:]
    #값 계산을 위해 int 타입으로 변환한다.
    castYr = int(year)
    #값 계산을 위해 int 타입으로 변환한다.
    castWk = int(week)
    #inputMinusWk이 str값으로 들어올 경우를 대비해 int타입으로 변환하는 코드 추가.
    castMiWk = int(inputMinusWk)
    #입력 후 추출한 주차 값과 뺄 주차 값을 뺀 값을 resultWk에 넣는다.
    resultWk = int(castWk - castMiWk)
    
    #52주차, 53주차의 경우를 계산하기 위해 무한루프를 돌린다.
    for i in range (0,9999):
        #조건1. 주차를 뺀 결과가 0보다 클 경우
        if resultWk>0:
            #result 안에 현재 연도와 주차 계산 결과를 str타입으로 변환해서 담는다.
            #변환을 안하면 int값으로 둘이 더해지기 때문에 변환한다.
            #zfill은 뒤부터 괄호안에 숫자만큼 빈 공간에 0을 넣어준다.
            result =  str(castYr) + str(resultWk).zfill(2)
            # result값을 리턴한다.
            return result
            #값을 도출 했으니 무한루프를 종료한다.
            break
        #조건2. 주차를 뺀 결과가 0보다 작거나 같을 경우 (0주차는 없기 때문에 0과 같을 경우 포함)
        else:
            #현재 주차가 0보다 크거나 작기때문에 연도에 1년을 빼고 다시 castYr에 담는다.
            castYr -= 1
            #resultWk와 1년을 뺀 castYr의 주차를 더한 값을 다시 resultWk에 담는다. 
            resultWk += Week.last_week_of_year(castYr).week

weekCal("201710" , 271)