import sys

input = sys.stdin.readline

hour = int(input().rstrip())
minute = int(input().rstrip())

front_word = ""
back_word = ""
middle_word = {
    "oclock": "o' clock",

    "past_one_minute": "minute past",
    "past": "minutes past",

    "quarter_past": "quarter past",
    "quarter_to": "quarter to",
    
    "half_past": "half past",
    
    "to_minute": "minute to",
    "to_minutes": "minutes to"
}

num = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "quarter",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
    "twenty",
    "twenty one",
    "twenty two",
    "twenty three",
    "twenty four",
    "twenty five",
    "twenty six",
    "twenty seven",
    "twenty eight",
    "twenty nine",
    "half"
]

if minute == 0:
    print(f"{num[hour - 1]} {middle_word['oclock']}")

elif minute == 1:
    print(f"{num[minute - 1]} {middle_word['past_one_minute']} {num[hour - 1]}")

elif minute == 15:
    print(f"{middle_word['quarter_past']} {num[hour - 1]}")

elif (60 - minute) == 15:
    if hour >= 12:
        hour -= 12
    print(f"{middle_word['quarter_to']} {num[hour]}")

elif minute < 30:
    print(f"{num[minute - 1]} {middle_word['past']} {num[hour - 1]}")

elif minute == 30:
    print(f"{middle_word['half_past']} {num[hour - 1]}")

elif minute == 59:
    if hour >= 12:
        hour -= 12
    print(f"{num[60 - minute - 1]} {middle_word['to_minute']} {num[hour]}")    

elif 30 < minute < 60:
    if hour >= 12:
        hour -= 12
    print(f"{num[60 - minute - 1]} {middle_word['to_minutes']} {num[hour]}")