class StateMachine:
    def __init__(self, initial_state, state_table):
        self.current_state = initial_state #시작 상태 설정
        self.rules = state_table #상태 전이 규칙 설정
        self.current_state.enter(('START', None)) #시작 상태로 진입

    def update(self):
        self.current_state.do() #현재 상태의 동작 수행

    def draw(self):
        self.current_state.draw() #현재 상태의 그리기 수행

    def handle_event(self, state_event):
        for check_event in self.rules[self.current_state].keys(): #현재 상태에서 가능한 이벤트 확인
            if check_event(state_event): #이벤트가 발생했는지 확인
                self.next_state = self.rules[self.current_state][check_event] #다음 상태 결정
                self.current_state.exit(state_event) #현재 상태에서 나가기
                self.next_state.enter(state_event) #다음 상태로 진입
                self.current_state = self.next_state
                return