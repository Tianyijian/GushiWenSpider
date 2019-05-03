# _*_ coding:utf8 _*_

"""
定义start_urls、allowed_urls等
"""

start_urls = [
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=1'   # 先秦
     'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=2'   # 两汉
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=3'   # 魏晋 3210
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=4'   # 南北朝	6720
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=5'   # 隋代	2110
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=6'   # 唐   10000->7000->886
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=7'   # 五代    ->493
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=8'   # 宋     ->2656->302
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=9'   # 金       6440->   ->40+
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=10'  # 元   -> 1001
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=11'  # 明 ->
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=12'  # 清 ->
    # 'https://www.gushiwen.org/shiwen/default.aspx?page=1&type=3&id=13'  # 近现代
]

allowed_urls = [
    # 'shiwen/default[\.]*'
]
