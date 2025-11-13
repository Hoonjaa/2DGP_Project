from pico2d import load_image

class Brute:
    image = None
    def __init__(self):
        self.x, self.y = 940, 90
        self.hp = 300

        self.current_state = 'IDLE'

        # 애니메이션 관련 변수
        self.frame = 0
        self.anim_progress = 0.0
        if Brute.image is None:
            Brute.image = load_image('Sprite/Brute.png')

        # 방향 변수
        self.face_dir = 1
        self.dir = 0