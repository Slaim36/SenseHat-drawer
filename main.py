from sense_hat import SenseHat
import pygame
from pygame.locals import *

sense = SenseHat()


class Slider:
	def __init__(self, x, y, w, h, c):
		self.p = 0
		self.rect = pygame.Rect(x, y, w, h)
		self.image = pygame.Surface((w, h))
		self.image.fill((255, 255, 255))
		self.rad = h // 2
		self.pwidth = w - self.rad * 2
		self.c = c
		for i in range(self.pwidth):
			color = self.get_color(i)
			pygame.draw.rect(self.image, color, (i + self.rad, h // 3, 1, h - 2 * h // 3))

	def get_color(self, pos):
		color = pygame.Color(0)
		if self.c == "r":
			color = pygame.Color(int(255 * pos / self.pwidth), 0, 0)
		if self.c == "g":
			color = pygame.Color(0, int(255 * pos / self.pwidth), 0)
		if self.c == "b":
			color = pygame.Color(0, 0, int(255 * pos / self.pwidth))
		return color

	def get_value(self):
		return self.p * 255

	def draw(self, surf):
		surf.blit(self.image, self.rect)
		center = self.rect.left + self.rad + self.p * self.pwidth, self.rect.centery
		pygame.draw.circle(surf, self.get_color(self.p), center, self.rect.height // 2)

	def update(self):
		moude_buttons = pygame.mouse.get_pressed()
		mouse_pos = pygame.mouse.get_pos()
		if moude_buttons[0] and self.rect.collidepoint(mouse_pos):
			self.p = (mouse_pos[0] - self.rect.left - self.rad) / self.pwidth
			self.p = (max(0, min(self.p, 1)))


class DrawingMatrix:
	def __init__(self):
		self.pixels = [[255, 255, 255]] * 64
		self.pixels_rect = [pygame.rect.Rect(0, 0, 1, 1)] * 64
		self.pixels_size = 50
		i = 0
		new_pixels_rect = []
		for rect in self.pixels_rect:
			rect.height = rect.width = self.pixels_size - 2
			y = (int(i / 8) + 1) * self.pixels_size - self.pixels_size * 0.75 + 1
			x = (i - int(i / 8) * 8 + 1) * self.pixels_size - self.pixels_size * 0.75 + 1
			new_pixels_rect.append(rect.move(x, y))
			i += 1
		self.pixels_rect = new_pixels_rect

	def clear(self):
		self.pixels = [[255, 255, 255]] * 64


class App:
	def __init__(self):
		self.red_slider = self.blue_slider = self.green_slider = None
		self.previous_pixels = None
		self.mouse_pressed = False
		self.drawingMatrix = None
		self._running = True
		self._display_surf = None
		self.size = self.width, self.height = 424, 600

	def on_init(self):
		pygame.init()
		self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
		self.drawingMatrix = DrawingMatrix()
		self.red_slider = Slider(12, self.drawingMatrix.pixels_size * 7 + 64, 400, 60, "r")
		self.green_slider = Slider(12, self.drawingMatrix.pixels_size * 7 + 4 + 60*2, 400, 60, "g")
		self.blue_slider = Slider(12, self.drawingMatrix.pixels_size * 7 + 4 + 60*3, 400, 60, "b")
		self._running = True

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self._running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.mouse_pressed = True
		if event.type == pygame.MOUSEBUTTONUP:
			self.mouse_pressed = False

	def on_loop(self):
		self.red_slider.update()
		self.green_slider.update()
		self.blue_slider.update()
		if pygame.key.get_pressed()[K_SPACE]:
			self.drawingMatrix.clear()
		if self.mouse_pressed:
			pos = pygame.mouse.get_pos()
			for i, rect in enumerate(self.drawingMatrix.pixels_rect):
				if rect.collidepoint(pos):
					self.drawingMatrix.pixels[i] = [self.red_slider.get_value(), self.green_slider.get_value(), self.blue_slider.get_value()]

	def on_render(self):
		self._display_surf.fill([self.red_slider.get_value(), self.green_slider.get_value(), self.blue_slider.get_value()])
		for i in range(len(self.drawingMatrix.pixels)):
			pygame.draw.rect(self._display_surf, self.drawingMatrix.pixels[i], self.drawingMatrix.pixels_rect[i])
		self.red_slider.draw(self._display_surf)
		self.green_slider.draw(self._display_surf)
		self.blue_slider.draw(self._display_surf)
		pygame.display.update()

		if self.previous_pixels != self.drawingMatrix.pixels:
			sense.set_pixels(self.drawingMatrix.pixels)
			pass
		self.previous_pixels = self.drawingMatrix.pixels.copy()

	def on_cleanup(self):
		pygame.quit()

	def on_execute(self):
		self.on_init()

		while self._running:
			for event in pygame.event.get():
				self.on_event(event)
			self.on_loop()
			self.on_render()
		self.on_cleanup()


if __name__ == "__main__":
	theApp = App()
	theApp.on_execute()
