from flask import Flask, render_template
import random
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

def get_last_lotto_numbers():
    """로또 최신 회차 + 번호 가져오기 (공식 API, SSL 오류 없음)"""

    # 1) 가장 최신 회차 번호를 가져오기 위한 요청
    latest_info = requests.get(
        "https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=1", verify=False
    ).json()

    # 위 URL로는 최신 회차를 알 수 없어서,
    # 높은 숫자를 조회했을 때 없는 회차라면 'returnValue=fail'
    # 존재하는 가장 최신 회차를 찾는 방식 사용
    low, high = 1, 12000  # 2025년 기준 최대 약 1200회
    last_round = 0

    while low <= high:
        mid = (low + high) // 2
        res = requests.get(
            f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={mid}", verify=False
        ).json()

        if res["returnValue"] == "success":
            last_round = mid
            low = mid + 1
        else:
            high = mid - 1

    # 2) 최종 최신 회차 번호로 실제 번호 조회
    data = requests.get(
        f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={last_round}", verify=False
    ).json()

    numbers = [
        data["drwtNo1"],
        data["drwtNo2"],
        data["drwtNo3"],
        data["drwtNo4"],
        data["drwtNo5"],
        data["drwtNo6"],
    ]
    bonus = data["bnusNo"]

    return last_round, numbers, bonus


@app.route("/")
def index():
    today_numbers = sorted(random.sample(range(1, 46), 6))

    last_round, last_numbers, bonus = get_last_lotto_numbers()

    return render_template(
        "index.html",
        numbers=today_numbers,
        last_round=last_round,
        last_numbers=last_numbers,
        bonus=bonus
    )


if __name__ == "__main__":
    app.run(debug=True)
