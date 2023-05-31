//해당 폴더 경로에 npm install express,  npm install mysql 실행
var express = require('express');
var http = require('http');
var app = express();
var server = http.createServer(app).listen(80);

var mysql      = require('mysql');
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : '0000',
  database : 'web'
});

connection.connect(function(error) {
  if (error) {
    console.error('DB 연결 오류:', error);
  } else {
    console.log('DB 연결 성공!');
  }
});

//외부 프로그램을 실행 하게 해주는 명령어
//같은 디렉토리에 파일을 두어 경로 설정 불필요하게 만듦
//파일이 다른 디렉토리에 있다면 경로 설정을 해주어야 함.('crawling_ETL' 앞에)
const { spawn } = require('child_process');
const pythonProcess = spawn('python', ['crawling_ETL.py']);

//정상 실행 됐는지 log로 확인
console.log("크롤링 및 db저장 성공!")

//menu로 요청이 들어오면 동작을 실현하게 명령어 작성
app.get('/menu', function (req, res) {
  res.sendFile(__dirname + '/crawling_ETL.html');
});

//요청이 들어오면 조건에 맞는 쿼리를 이용해 데이터를 출력
app.get('/getDblist', function (req, res) {
  let query = `select * from resultdata`
  connection.query(query, function (error, results, fields) {
     if (error) throw error
     res.send(results)
  });
});

app.get('/getListPriceDesc', function (req, res) {
  //object형태인 price의 value값을 추출해 정렬하는 방법
  let query = `SELECT product,
                      CAST(replace(price, "원", "") AS integer) as price,
                      likeCount
               FROM resultdata
               ORDER BY price DESC`;
  connection.query(query, function (error, results, fields) {
     if (error) throw error
     res.send(results)
  });
});

app.get('/getListLikeDesc', function (req, res) {
  let query = `SELECT product,
                      CAST(likeCount AS integer) as likeCount,
                      likeCount
               FROM resultdata
               ORDER BY likeCount DESC;`
  connection.query(query, function (error, results, fields) {
     if (error) throw error
     res.send(results)
  });
});
