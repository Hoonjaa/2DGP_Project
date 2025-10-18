class StateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state #시작 상태 설정
        self.current_state.enter() #시작 상태로 진입

    def update(self):
        self.current_state.do() #현재 상태의 동작 수행

    def draw(self):
        self.current_state.draw() #현재 상태의 그리기 수행

