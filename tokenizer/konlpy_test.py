import jpype
from konlpy.tag import Okt


# OKT 테스트
okt = Okt()
print(okt.morphs("테스트 문장입니다"))

jpype.shutdownJVM()
