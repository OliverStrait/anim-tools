from manim import *



def rotating_angle(angle:Angle, text:Mobject, tracker: ValueTracker,buffer = 4 * SMALL_BUFF):
    '''Creates a group of angle and it's lines, that can be updated by changing ValueTrackers value.'''
    def move_text(center):
        dir_vect = angle.point_from_proportion(0.5) - center
        offset_vect = ( angle.radius + buffer) * (dir_vect / np.linalg.norm(dir_vect))
        text.move_to(center + offset_vect)

    static_l, mov_line = angle.lines
    group = VGroup(static_l, mov_line,text,angle)
    move_text(mov_line.get_start())
    def closure(x:VGroup):
        center = mov_line.get_start()
        mov_line.rotate(
            tracker.get_value() * DEGREES - mov_line.get_angle(),
            about_point=center
            )
        angle.become(Angle(static_l, mov_line, radius= angle.radius, other_angle=False))
        move_text(center)

    group.add_updater(closure)
    return group


class MovingAngle(Scene):
    def construct(self):
        trc = ValueTracker(110)
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT*4)
        line_moving.rotate(trc.get_value() * DEGREES, about_point=line_moving.get_start())

        angle_obj = Angle(line1, line_moving, radius=0.5, other_angle=False)
        number = DecimalNumber(trc.get_value(), num_decimal_places=0)
        number.add_updater(lambda o: DecimalNumber.set_value(o, trc.get_value()))

        angle_group = rotating_angle(angle_obj,number,trc,)

        self.wait()
        self.add(angle_group)
        
        for a in range(1,40,10):
            self.play(trc.animate.set_value(a))
        line_moving.set_color(BLUE)
        for a in [50,30,60,180]:
            self.play(trc.animate.set_value(a))
            self.wait(.5)
        line_moving.set_color(RED)
        for _ in range(4):
            self.play(trc.animate.increment_value(10))
            self.wait(.5)
        a = trc.get_value()
        line_moving.set_color(YELLOW)
        angle_obj.radius = 1
        while a < 360:
            a += 35
            self.play(trc.animate.set_value(a))
            self.wait(.5)
        line_moving.set_color(TEAL)

        self.play(angle_obj.animate.set(radius= 0.5))
        self.play(angle_group.animate.move_to(RIGHT*3))
        for a in np.linspace(1.9*PI,0.5*PI,5):
            self.play(trc.animate.set_value(a/DEGREES))
            self.wait(.5)