world = [[], [], []]

def add_object(o, depth = 0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            del o
            return

    raise Exception("월드에 존재하지 않는 객체를 삭제하려고 합니다.")

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def clear():
    for layer in world:
        layer.clear()