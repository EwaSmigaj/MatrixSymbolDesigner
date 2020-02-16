#! python3

import pygame
import sys

pygame.init()

class Program:

    def __init__(self, width=1200, height=700, fields_numb = 7):
        self._board = Board(width, height, fields_numb)
        self._color = (0, 0, 0, 255)

    def play(self):
        while True:
            self.handle_event()
            self._board.display()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if self._board.get_wheel_rect().collidepoint(x, y):
                    self._color = self._board.get_position(x, y)

                self._board.if_field_clicked(x, y, self._color)
                if self._board.OK_button.if_pressed(x, y):
                    self._board.make_matrix_file()
        return False


class Button:
    def __init__(self, width, height, position, color, text):
        self._width = width
        self._height = height
        self._color = color
        self._position = position
        self._text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self._color, pygame.Rect(self._position[0], self._position[1], self._width, self._height))
        pygame.draw.rect(screen, (255,125,240), pygame.Rect(self._position[0], self._position[1], self._width, self._height),4)
        if self._text != '':
            font = pygame.font.SysFont('arial', 60)
            text = font.render(self._text, 1, (0, 0, 0))
            screen.blit(text, (self._position[0] + (self._width / 2 - text.get_width() / 2), self._position[1] +
                               (self._height / 2 - text.get_height() / 2)))

    def if_pressed(self, x_pos, y_pos):
        if self._position[0] < x_pos < self._position[0] + self._width:
            if self._position[1] < y_pos < self._position[1] + self._height:
                return True
        return False


class Board:

    def __init__(self, width, height, field_numb):
        self._width = width
        self._height = height
        self._field_numb = field_numb
        self._fields_data = {} # {number: [color, x_pos, y_pos]}
        self._wheel_img = pygame.image.load("ColorWheel.png")
        self._color_wheel_data = [] # size xpos ypos
        self._field_side = (self._height - 40) // field_numb
        self._screen = pygame.display.set_mode((self._width, self._height))

        for i in range(0, self._field_numb):
            for j in range(0, self._field_numb):
                self._fields_data[j+i*self._field_numb] = [(0, 0, 0), ((self._field_side * j) + 20, (self._field_side * i) + 20)]

        self._color_wheel_data.append(int(self._height*0.4))
        self._color_wheel_data.append(self._height + int(0.5*(self._width - self._height + 20 - self._color_wheel_data[0])) - 20)
        self._color_wheel_data.append(20)

        self._wheel_img = pygame.transform.scale(self._wheel_img,
                                                 (self._color_wheel_data[0], self._color_wheel_data[0]))

        self.OK_button = Button(int(0.5*self._color_wheel_data[0]), int(0.25*self._color_wheel_data[0]), (self._color_wheel_data[1] + (self._color_wheel_data[0]/4),
                                          self._height*0.5), (255, 255, 255), "OK")

    def draw_frame(self):
        for i in range(0, self._field_numb**2):
            pygame.draw.rect(self._screen, (255, 255, 255), pygame.Rect(self._fields_data[i][1], (self._field_side, self._field_side)), 4)

    def draw_fields(self):
        for i in range(0, self._field_numb**2):
            pygame.draw.rect(self._screen, self._fields_data[i][0], pygame.Rect(self._fields_data[i][1], (self._field_side, self._field_side)))

    def draw_wheel(self):
        self._screen.blit(pygame.transform.scale(self._wheel_img, (self._color_wheel_data[0], self._color_wheel_data[0])),
                          (self._color_wheel_data[1], self._color_wheel_data[2]))

    def get_wheel_rect(self):
        return self._wheel_img.get_rect(topleft=(self._color_wheel_data[1], self._color_wheel_data[2]))

    def get_position(self, x, y):
        return self._screen.get_at((x,y))

    def display(self):
        pygame.Surface.fill(self._screen, (0, 0, 0))
        a = (20, 20)
        self.draw_fields()
        self.draw_frame()
        self.draw_wheel()
        self.OK_button.draw(self._screen)
        pygame.display.flip()

    def if_field_clicked(self, pos_x, pos_y, color):
        if pos_x > 20+self._field_numb*self._field_side:
            return False
        x = (pos_x - 20) // self._field_side
        y = (pos_y - 20) // self._field_side
        field_nb = x+y*self._field_numb
        print(f"field numb = {field_nb}")
        if field_nb in self._fields_data:
            self.change_field(field_nb, color[:3])
        else:
            return False

    def get_pixel(self, x, y):
        return self._screen.get_at((x,y))

    def change_field(self, field_nb, color):
        self._fields_data[field_nb][0] = color
        print(f"changed field {field_nb}")

    def make_matrix_file(self):
        matrix_file = open('color_matrix.txt', 'w')
        matrix_file.write('{')
        for field in range(self._field_numb**2-1):
            matrix_file.write(str(self._fields_data[field][0])[1:-1] + ', ')
        matrix_file.write(str(self._fields_data[self._field_numb**2-1][0])[1:-1])
        matrix_file.write('}')


b = Program()
b.play()
