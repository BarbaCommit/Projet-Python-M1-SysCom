import pygame
import math
from constants import (
    CAR_ACCELERATION, CAR_WIDTH, CAR_HEIGHT, TILE_SIZE, CAR_ANGULAR_ACCELERATION, CAR_FRICTION, CAR_ANGULAR_FRICTION, CAR_MAX_ANGULAR_SPEED
  
)


class Car:

    def __init__(self, start_col: int, start_row: int, color:tuple[int]):
        
        self.x = start_col * TILE_SIZE + TILE_SIZE // 2
        self.y = start_row * TILE_SIZE + TILE_SIZE // 2

        #self.speed: float = 0.0
        self.vx:float = 0.0
        self.vy:float = 0.0

        self.angle: float = 90.0
        self.angular_speed: float = 0.0
        self.color = color
        self.sprite = self.build_sprite()

    def accelerate(self) -> None:
        rad = math.radians(self.angle - 90)
        self.vx += math.cos(rad) * CAR_ACCELERATION
        self.vy += math.sin(rad) * CAR_ACCELERATION

    def decelerate(self) -> None:
        rad = math.radians(self.angle - 90)
        self.vx -= math.cos(rad) * CAR_ACCELERATION
        self.vy -= math.sin(rad) * CAR_ACCELERATION

    def turn_left(self) -> None:
        rad = math.radians(self.angle - 90)
        forward_speed = self.vx * math.cos(rad) + self.vy * math.sin(rad)
        factor = -1.0 if forward_speed < -0.1 else 1.0

        self.angular_speed -= CAR_ANGULAR_ACCELERATION * factor
        self.angular_speed = max(self.angular_speed,-CAR_MAX_ANGULAR_SPEED)

    def turn_right(self) -> None:
        rad = math.radians(self.angle - 90)
        forward_speed = self.vx * math.cos(rad) + self.vy * math.sin(rad)
        factor = -1.0 if forward_speed < -0.1 else 1.0

        self.angular_speed += CAR_ANGULAR_ACCELERATION * factor
        self.angular_speed = min(self.angular_speed,CAR_MAX_ANGULAR_SPEED)

    def update_position(self,tile_friction:float = 0.9) -> None:
        self.angle += self.angular_speed
        self.angular_speed *= CAR_ANGULAR_FRICTION

        rad = math.radians(self.angle - 90)
        forward_x, forward_y = math.cos(rad),math.sin(rad)
        right_x, right_y = -forward_y, forward_x

        forward_speed = self.vx * forward_x + self.vy * forward_y
        lateral_speed = self.vx * right_x + self.vy * right_y

        lateral_speed *= tile_friction
        forward_speed *= 0.98

        self.vx = forward_x * forward_speed + right_x * lateral_speed
        self.vy = forward_y * forward_speed + right_y * lateral_speed
    
        self.x += self.vx
        self.y += self.vy

    def build_sprite(self) -> pygame.Surface:

        surf = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, CAR_WIDTH,
                         CAR_HEIGHT), border_radius=5)

        front_color = (150,220,255,200)
        front_rect = (3,5,CAR_WIDTH - 6,12)
        pygame.draw.rect(surf,front_color,front_rect,border_radius=3)
        
        return surf

    def get_rotated_sprite(self) -> tuple[pygame.Surface, pygame.Rect]:
        rotated = pygame.transform.rotate(self.sprite, -self.angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        return rotated, rect
    
    def respawn(self,x:float,y:float,angle:float = 90.0) -> None:
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.angle = angle
        self.angular_speed = 0.0

    def get_hitbox(self) -> list[tuple[float,float,float]]:
        rad = math.radians(self.angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        width,height = CAR_WIDTH/2, CAR_HEIGHT/2
        corners = []
        gaps = [(-width,-height),(width,-height),(width,height),(-width,height)]

        for x,y in gaps:
            rot_x = self.x + (x*cos_a - y*sin_a)
            rot_y = self.y + (x*sin_a + y*cos_a)
            corners.append((rot_x,rot_y))
        return corners