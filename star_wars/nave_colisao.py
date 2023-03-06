from config import Config


def collision_nave_or_bullet(nave_x, nave_y, speed_ast_x, speed_ast_y, speed_nave_x, speed_nave_y, pos_x, pos_y, w, h, bt):
    side_right = pos_x + w
    side_left = pos_x
    side_up = pos_y
    side_down = pos_y + h
    if (
            (nave_x > side_right and side_up < nave_y < side_down) or
            (nave_x > side_right and (abs(nave_x - side_right) > abs(nave_y - side_up))) or
            (nave_x > side_right and (abs(nave_x - side_right) > abs(nave_y - side_down)))
    ):
        nave_x += abs(speed_nave_x)
        #if abs(speed_ast_x) > abs(speed_nave_x):
        #    speed_nave_x = abs(speed_ast_x)
        #else:
        speed_nave_x = 2

    if (
            (side_left < nave_x < side_right and nave_y > side_down) or
            (nave_y > side_down and (abs(nave_y - side_down) > abs(nave_x - side_right))) or
            (nave_y > side_down and (abs(nave_y - side_down) > abs(nave_x - side_left)))
    ):
        nave_y += abs(speed_nave_y)
        #if abs(speed_ast_y) > abs(speed_nave_y):
        #    speed_nave_y = abs(speed_ast_y)
        #else:
        speed_nave_y = 2

    if (
            (nave_x < side_left and side_up < nave_y < side_down) or
            (nave_x < side_left and (abs(nave_x - side_left) > abs(nave_y - side_up))) or
            (nave_x < side_left and (abs(nave_x - side_left) > abs(nave_y - side_down)))
    ):
        nave_x += -(abs(speed_nave_x))
        #if abs(speed_ast_x) > abs(speed_nave_x):
        #    speed_nave_x = -abs(speed_ast_x)
        #else:
        speed_nave_x = -2

    if (
            (side_left < nave_x < side_right and nave_y < side_up) or
            (nave_y < side_up and (abs(nave_y - side_up) > abs(nave_x - side_left))) or
            (nave_y < side_up and (abs(nave_y - side_up) > abs(nave_x - side_right)))
    ):
        nave_y += -(abs(speed_nave_y))
        #if abs(speed_ast_y) > abs(speed_nave_y):
        #    speed_nave_y = -abs(speed_ast_y)
        #else:
        speed_nave_y = -2

    pos = [nave_x, nave_y]
    velo = [speed_nave_x, speed_nave_y]
    var = (pos, velo)
    return var

