from flask import Flask, render_template, jsonify, request
import random
import requests

app = Flask(__name__)

# 캐싱: 최신 회차 번호 저장
last_round_cache = None

def find_latest_round():
    """최신 회차 번호를 빠르게 탐색(이진 탐색)"""
    low, high = 1000, 2000
    latest = 0

    while low <= high:
        mid = (low + high) // 2
        res = requests.get(
            f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={mid}",
            verify=False
        ).json()

        if res["returnValue"] == "success":
            latest = mid
            low = mid + 1
        else:
            high = mid - 1

    return latest


def get_last_lotto_numbers():
    """최신 회차 + 번호 가져오기"""

    global last_round_cache

    # 1) 캐시가 있으면 그대로 사용
    if last_round_cache:
        last_round = last_round_cache
    else:
        # 2) 최신 회차 번호 찾기
        last_round = find_latest_round()
        last_round_cache = last_round

    # 3) 최신 회차 번호 조회
    data = requests.get(
        f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={last_round}",
        verify=False
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


def get_round_numbers(round_no):
    """특정 회차 번호 조회"""
    data = requests.get(
        f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={round_no}",
        verify=False
    ).json()

    if data["returnValue"] == "fail":
        return None

    numbers = [
        data["drwtNo1"],
        data["drwtNo2"],
        data["drwtNo3"],
        data["drwtNo4"],
        data["drwtNo5"],
        data["drwtNo6"],
    ]
    bonus = data["bnusNo"]

    return numbers, bonus

def get_color(n):
    if n <= 10:
        return "yellow"
    elif n <= 20:
        return "blue"
    elif n <= 30:
        return "red"
    elif n <= 40:
        return "green"
    else:
        return "orange"


@app.route("/")
def index():
    today_nums = sorted(random.sample(range(1, 46), 6))
    last_round, last_nums, bonus = get_last_lotto_numbers()

    return render_template(
        "index.html",
        today=today_nums,
        last_round=last_round,
        last_nums=last_nums,
        bonus=bonus,
        get_color=get_color
    )


# AJAX: 새 번호 생성
@app.route("/generate")
def generate():
    nums = sorted(random.sample(range(1, 46), 6))
    return jsonify(nums)


# AJAX: 원하는 회차 조회
@app.route("/get_round")
def get_round():
    n = int(request.args.get("round"))
    res = get_round_numbers(n)
    return jsonify(res if res else {"error": "not found"})


if __name__ == "__main__":
    app.run(debug=True)
