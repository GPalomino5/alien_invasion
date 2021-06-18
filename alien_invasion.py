import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
	"""Overall class to manage game assets and behavior"""

	def __init__(self):
		"""Initialize the game and crate game resources"""
		pygame.init() #Initialize a class pygame
		self.settings = Settings()

		"""
		self.screen = pygame.display.set_mode(
			(self.settings.screen_width, self.settings.screen_height))
		"""

		self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height

		pygame.display.set_caption("Alien Invasion")

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()

	def run_game(self):
		"""Starting the main loop for the game."""
		while True:
			self._check_events()
			self.ship.update()
			self._update_bullets()
			self._update_screen()
			
	def _update_bullets(self):
		"""Update bullets and get rid of old bullets """
		# Update bullets position.
		self.bullets.update()

		#get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

	def _check_events(self):
		"""Respond to keypresses and mouse events."""
		for event in pygame.event.get(): ##Guessing this returns a list
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)

			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_keydown_events(self, event):
		""" Checks keydown events."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True 	#Set ships moving_right flag to True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True 	#Set Ships movinf_left flag to true
		elif event.key == pygame.K_q:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		""" Checks keyup events."""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False	#Set ships moving_right flag to False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False	#Set ships moving_right flag to False

	def _fire_bullet(self):
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_screen(self):
		"""Update images on the screen and flic to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		pygame.display.flip()

if __name__ == '__main__':
	# Make a game instance and run the game.
	ai = AlienInvasion()
	ai.run_game()
