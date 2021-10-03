# 25/09/21 - snake.py
# snake game made in pygame

import pygame
import random

#initialise game
pygame.init()
pygame.display.set_caption("Snake")

#clock
clock = pygame.time.Clock()

# screen
SCREEN_SIZE = 400
GRID_WIDTH = 15
GRID_HEIGHT = 10
CELL_SIZE = SCREEN_SIZE//GRID_WIDTH

screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))

class Snake:
	def __init__(self):
		self.x = 0
		self.y = 0

		self.xspeed = 1
		self.yspeed = 0
		
		self.dead = False
		self.color = (0,255,0)

		self.tail = [(self.x,self.y)]
		self.length = 3
		
	# input handling
	def up(self):
		try:
			if self.tail[-2] != (self.x, self.y-1):
				self.yspeed = -1
				self.xspeed = 0
		except IndexError:
			self.yspeed = -1
			self.xspeed = 0

	def down(self):
		try:
			if self.tail[-2] != (self.x, self.y+1):
				self.yspeed = 1
				self.xspeed = 0
		except IndexError:
			self.yspeed = 1
			self.xspeed = 0

	def right(self):
		try:
			if self.tail[-2] != (self.x+1, self.y):
				self.yspeed = 0
				self.xspeed = 1	
		except IndexError:
			self.yspeed = 0
			self.xspeed = 1

	def left(self):
		try:
			if self.tail[-2] != (self.x-1, self.y):
				self.yspeed = 0
				self.xspeed = -1
		except IndexError:
			self.yspeed = 0
			self.xspeed = -1

	def eat(self):
		self.length += 1

	def death(self):
		self.dead = True
		self.color = (255,0,0)
		self.length = 0
		
	def reset(self):
		self.x = 0
		self.y = 0

		self.xspeed = 1
		self.yspeed = 0
		
		self.dead = False
		self.color = (0,255,0)

		self.tail = [(self.x,self.y)]
		self.length = 3

	def update(self):
		self.x = self.x + self.xspeed
		self.y = self.y + self.yspeed

		if (self.x, self.y) in self.tail[:-1]:
			self.death()

		if self.x < 0 or self.x > GRID_WIDTH-1 or self.y < 0 or self.y > GRID_HEIGHT-1:
			self.death()

		if len(self.tail)-1 == 0:
			self.reset()

		if len(self.tail)-1 < self.length:
			self.tail.append((self.x, self.y))

		if not (len(self.tail)-1 < self.length):
			self.tail.pop(0)

	def is_dead(self):
		return self.dead

	def get_pos(self):
		return (self.x, self.y)

	def get_tail(self):
		return self.tail

	def get_col(self):
		return self.color

class Food:
	def __init__(self):
		self.x = random.randint(0, GRID_WIDTH-1)
		self.y = random.randint(0, GRID_HEIGHT-1)

	def get_pos(self):
		return (self.x, self.y)

	def reset(self, tail):
		while (self.x,self.y) in tail:
			self.x = random.randint(0, GRID_WIDTH-1)
			self.y = random.randint(0, GRID_HEIGHT-1)

def main():

	s = Snake()
	f = Food()

	running = True

	while running:		

		if s.is_dead():
			clock.tick(10)
		else:
			clock.tick(7)

		screen.fill((0,0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					s.up()
				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					s.down()
				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					s.right()
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					s.left()
				# cheat for testing
				# if event.key == pygame.K_SPACE:
				# 	s.eat()

		s.update()

		food_x, food_y = f.get_pos()
		snake_tail = s.get_tail()
		snake_color = s.get_col()
		snake_x, snake_y = snake_tail[-1]

		# eat
		if food_x == snake_x and food_y == snake_y:
			s.eat()
			f.reset(snake_tail)

		# draw food
		pygame.draw.rect(screen, (255,0,0), pygame.Rect(food_x*CELL_SIZE, food_y*CELL_SIZE, CELL_SIZE, CELL_SIZE))		

		# draw snake
		for x,y in snake_tail:
			pygame.draw.rect(screen, snake_color, pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))	

		pygame.display.flip()

if __name__ == "__main__":
	main()
	