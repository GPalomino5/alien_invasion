import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

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

		# Create an instance to store game statistics,
		# 	and create a scoreboard
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.ship = Ship(self)
		self.bullets = pygame.sprite.Group()
		self.aliens = pygame.sprite.Group()

		self._create_fleet()

		# Make the play button.
		self.play_button = Button(self,"play")

	def run_game(self):
		"""Starting the main loop for the game."""
		while True:

			self._check_events()

			if self.stats.game_active:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen()
			
	def _update_bullets(self):
		"""Update bullets and get rid of old bullets """
		# Update bullets position.
		self.bullets.update()

		#get rid of bullets that have disappeared.
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		# Check for any bullets that have hit aliens.
		#  If so, get rid of the bullet and the alien.
		
		collisions = pygame.sprite.groupcollide(
				self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points * len(aliens)
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.aliens:
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			# Increase level.
			self.stats.level += 1
			self.sb.prep_level()

	def _update_aliens(self):
		"Update the positions of all aliens in the fleet."""
		"""
		Check if the fleeet is at an edge, 
			then udpate the positions of all aliens in the fleet.
		"""
		self._check_fleet_edges()
		self.aliens.update()

		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		# Check for aliens hitting the bottom of the screen.
		self._check_aliens_bottom()

	def _check_aliens_bottom(self):
		"""Checks if any alien has hit bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				# Treah this the same as if the ship got hit.
				self._ship_hit()
				break

	def _ship_hit(self):
		"""Responde to the ship being hit by an alien."""
		if self.stats.ships_left > 0:
			#Decrement ships left by 1 
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			#Get rid of any remaining bullets and ships
			self.bullets.empty()
			self.aliens.empty()

			# Create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#pause.
			sleep(3)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_fleet_edges(self):
		"""Respond appropieately if any aliens have reached an edge."""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""Drop the entire fleet and change the fleets direction."""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.fleet_drop_speed
		self.settings.fleet_direction *= -1

	def _check_events(self):
		"""Respond to keypresses and mouse events."""
		for event in pygame.event.get(): ##Guessing this returns a list
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)

			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_play_button(self, mouse_pos):
		""""Start a new game when the player hits play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		
		if button_clicked and not self.stats.game_active:
			# Reset game settings
			self.settings.initialize_dynamic_settings()

			# Reset the game statistics.
			self.stats.reset_stats()
			self.stats.game_active = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			# Get rid of any remaining alien and bullets.
			self.aliens.empty()
			self.bullets.empty()

			# Create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			pygame.mouse.set_visible(False)

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

	def _create_fleet(self):
		"""Create the fleet of aliens."""
		# Create an alien and find the number of aliens in a row.
		# Spacing between each alien is equal to one alien width.
			
			# Make an Alien
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size # tuple respectively
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = available_space_x // (2 * alien_width)

		# Determine the number of rows of alien that fit on the screen.
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - 
			(3 * alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		# Create the full fleet of aliens
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				# Create the first row of aliens
				self._create_alien(alien_number, row_number)

	def _create_alien(self, alien_number, row_number):
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		alien.x = alien_width + 2 * alien_width * alien_number
		alien.rect.x = alien.x
		if row_number != 0:
			alien.rect.y = alien_height + 2 * alien.rect.height * row_number
		self.aliens.add(alien)


	def _update_screen(self):
		"""Update images on the screen and flic to the new screen."""
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		#Draw the score information.
		self.sb.show_score()

		# Draw the play button if the game is inactive.
		if self.stats.game_active == False:
			self.play_button.draw_button()

		pygame.display.flip()

if __name__ == '__main__':
	# Make a game instance and run the game.
	ai = AlienInvasion()
	ai.run_game()
