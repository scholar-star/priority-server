
# DB에서 데이터를 찾지 못했을 때 발생하는 예외 클래스
class DBNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message