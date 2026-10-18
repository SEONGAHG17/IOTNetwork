# pdf 01 
# LED

import RPi.GPIO as GPIO        # 라즈베리 파이 GPIO 핀을 제어하기 위한 RPi.GPIO 모듈 임포트
from time import sleep         # 일정 시간(초 단위) 동안 프로그램 지연을 위한 sleep 함수 임포트

GPIO.setmode(GPIO.BCM)         # 핀 번호 지정 방식을 Broadcom SOC 채널 번호(BCM) 기준으로 설정
GPIO.setwarnings(False)        # 핀이 이미 사용 중일 때 발생하는 경고 메시지를 비활성화
GPIO.setup(21, GPIO.OUT)       # 21번 BCM 핀을 디지털 출력(OUT) 모드로 설정 (LED 제어용)

try:                           # 예외 처리 시작 (실행 중 발생할 수 있는 에러 대비)
    while True:                # 무한 루프 시작 (강제로 멈추기 전까지 계속 반복)
        GPIO.output(21, True)  # 21번 핀에 High(3.3V) 신호 출력 -> LED 켜짐
        sleep(0.5)             # 0.5초(500ms) 동안 대기
        # GPIO.output(21, True) # (주석 처리된 코드: 의미 없는 중복 코드)
        GPIO.output(21, False) # 21번 핀에 Low(0V) 신호 출력 -> LED 꺼짐
        sleep(0.5)             # 0.5초(500ms) 동안 대기

except KeyboardInterrupt:      # 사용자가 터미널에서 Ctrl+C를 눌러 강제 종료했을 때
    GPIO.cleanup()             # 사용했던 모든 GPIO 핀 설정 및 상태를 안전하게 초기화


#######################################################################################################################################################################

from flask import Flask, render_template, redirect, url_for  # Flask 클래스 및 템플릿/리다이렉트 함수 임포트
from time import sleep                                         # 지연 함수 임포트
import RPi.GPIO as GPIO                                        # GPIO 모듈 임포트

GPIO.setmode(GPIO.BCM)                                         # BCM 핀 모드 설정
GPIO.setwarnings(False)                                        # 경고 끄기
GPIO.setup(21, GPIO.OUT)                                       # 21번 핀 출력 설정

app = Flask(__name__) # Flask()는 클래스이며, 현재 모듈명을 인자로 전달해 인스턴스 생성

@app.route("/")                                                # 루트 URL('/')로 접속했을 때 실행할 라우터 데코레이터
def home():
    return render_template("index.html")                       # templates 폴더 안의 index.html 웹페이지 렌더링 반환

@app.route("/but")                                             # '/but' 주소로 접속했을 때 실행되는 함수
def button():
    try:
        while True:            # [문제점] 웹 요청 처리 함수 내에 무한 루프가 있어 브라우저 로딩이 끝나지 않고 멈춤
            GPIO.output(21,True)   # LED 켜기
            sleep(0.5)             # 0.5초 대기
            GPIO.output(21, False) # LED 끄기
            sleep(0.5)             # 0.5초 대기
    
    except KeyboardInterrupt:  # 키보드 인터럽트 예외 처리
        GPIO.cleanup()         # 핀 초기화
    
    return redirect(url_for("home")) # (무한 루프 때문에 이 코드까지 도달하지 못함)

if __name__ == "__main__":
    app.run(host="192.168.1.116", port=5000)                    # 지정한 IP와 5000번 포트로 플라스크 개발 서버 실행

#######################################################################################################################################################################

from flask import Flask, render_template, redirect, url_for  # 플라스크 핵심 기능 임포트
import RPi.GPIO as GPIO                                        # GPIO 모듈 임포트

app = Flask(__name__)                                          # 플라스크 앱 인스턴스 생성

# GPIO setting
GPIO.setmode(GPIO.BCM)                                         # BCM 모드 설정
GPIO.setwarnings(False)                                        # 경고 끄기
GPIO.setup(21, GPIO.OUT)                                       # 21번 핀 출력 설정
GPIO.output(21, GPIO.LOW) # 프로그램 시작 시 초기 상태로 LED를 꺼둠(LOW)[cite: 86]

@app.route("/")                                                # 메인 페이지 라우트
def home():
    return render_template("index.html")                       # index.html 렌더링

@app.route("/on")                                              # '/on' 경로 요청이 오면 실행
def led_on():
    GPIO.output(21, GPIO.HIGH) # 21번 핀을 HIGH로 만들어 LED를 켬[cite: 86]
    return redirect(url_for("home")) # 처리가 끝나면 메인('/') 페이지로 강제 이동(새로고침 효과)[cite: 86]

@app.route("/off")                                             # '/off' 경로 요청이 오면 실행
def led_off():
    GPIO.output(21, GPIO.LOW) # 21번 핀을 LOW로 만들어 LED를 끔[cite: 86]
    return redirect(url_for("home")) # 메인('/') 페이지로 리다이렉트[cite: 86]


if __name__ == "__main__":
    try:
        app.run(host="192.168.1.116", port=8000)               # IP와 8000번 포트로 웹 서버 구동
    
    finally:
        GPIO.cleanup()         # 서버가 종료될 때 안전하게 GPIO 설정 정리

#######################################################################################################################################################################

from flask import Flask, render_template, redirect, url_for  # 플라스크 모듈 임포트
import RPi.GPIO as GPIO                                        # GPIO 모듈 임포트
# from time import sleep

GPIO.setmode(GPIO.BCM)                                         # BCM 모드 설정
GPIO.setwarnings(False)                                        # 경고 끄기
GPIO.setup(21, GPIO.OUT)                                       # 21번 핀 출력 설정

pwm = GPIO.PWM(21, 3000) # 21번 핀을 PWM 객체로 생성, 주파수(Frequency)는 3000Hz 설정
pwm.start(0)             # PWM 출력 시작, 초기 듀티비(Duty Cycle)는 0% (완전 소등)
duty = 0                 # 현재 듀티비(밝기 비율, 0~100)를 저장할 전역 변수 선언

app = Flask(__name__)                                          # 플라스크 앱 생성

@app.route("/")                                                # 메인 페이지 라우트
def home():
    return render_template("index.html")                       # index.html 렌더링

@app.route("/on")                                              # 밝게 버튼('/on') 클릭 시
def led_on():
    global duty                # 함수 외부의 전역 변수 duty를 수정하기 위해 global 선언
    pwm.ChangeDutyCycle(duty)  # 현재 듀티비 값으로 PWM 신호 변경
    duty = duty + 20           # 듀티비를 20씩 증가시킴
    if(duty >= 100):           # 만약 100을 넘어가거나 같아지면
        duty = 100             # 최대값인 100으로 고정
    return redirect(url_for("home")) # 메인 페이지로 리다이렉트

@app.route("/off")                                             # 어둡게 버튼('/off') 클릭 시
def led_off():
    global duty                # 전역 변수 duty 사용 선언
    pwm.ChangeDutyCycle(duty)  # 현재 듀티비 적용
    duty = duty - 20           # 듀티비를 20씩 감소시킴
    if(duty <= 0):             # 만약 0보다 작거나 같아지면
        duty = 0               # 최소값인 0으로 고정(완전 소등)
    return redirect(url_for("home")) # 메인 페이지로 리다이렉트

if __name__ == "__main__":
    try:
        app.run(host="192.168.1.116", port=8000)               # 서버 실행
    finally:
        GPIO.cleanup()         # 종료 시 자원 해제
