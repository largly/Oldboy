import json

from django.test import TestCase
from DBUtils import PooledDB
# Create your tests here.
a = {
  "1": {
    "course_type": "course",
    "id": "1",
    "name": "21天学会python",
    "img": "python.png",
    "selected_policy": 1
  },
  "price_policy_dict": {
    30: {
      "period_name": "1个月",
      "price": 6666.0
    },
    60: {
      "period_name": "2个月",
      "price": 3000.0
    },
    180: {
      "period_name": "6个月",
      "price": 19999.0
    }
  }
}
c = '{"1": {"course_type": "course", "id": "1", "name": "21\u5929\u5b66\u4f1apython", "img": "python.png", "selected_policy": 1}, "price_policy_dict": {"30": {"period_name": "1\u4e2a\u6708", "price": 6666.0}, "60": {"period_name": "2\u4e2a\u6708", "price": 3000.0}, "180": {"period_name": "6\u4e2a\u6708", "price": 19999.0}}}'

d = b'{"1": {"course_type": "course", "id": "1", "name": "21\xe5\xa4\xa9\xe5\xad\xa6\xe4\xbc\x9apython", "img": "python.png", "selected_policy": 1}, "price_policy_dict": {30: {"period_name": "1\xe4\xb8\xaa\xe6\x9c\x88", "price": 6666.0}, 60: {"period_name": "2\xe4\xb8\xaa\xe6\x9c\x88", "price": 3000.0}, 180: {"period_name": "6\xe4\xb8\xaa\xe6\x9c\x88", "price": 19999.0}}}'
print(json.loads(d))
# print(json.loads(c))