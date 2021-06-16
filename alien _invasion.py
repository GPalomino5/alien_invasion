import sys
import pygame

class AlienInvasion:
	"""Overall class to manage game assets and behavior"""

	def __init__(self):
		"""Initialize the game and crate game resources"""
		pygame.init() #Initialize a class pygame

		self.screen = pygame.display.set_mode((1200,800))
		pygame.display.set_caption("Alien Invasion")

		# Set the background color.
		self.bg_color = (255,255,255) #Red, Green, Blue

	def run_game(self):
		"""Starting the main loop for the game."""
		while True:
			# Watch for keyboard and mouse events.
			for event in pygame.event.get(): ##Guessing this returns a list
				if event.type == pygame.QUIT:
					print(pygame.QUIT)
					sys.exit()

			# Redraw the screen during each pass through the loop
			self.screen.fill(self.bg_color)

			#Make the most recently drawn screen visible.
			pygame.display.flip()
if __name__ == '__main__':
	# Make a game instance and run the game.
	ai = AlienInvasion()
	ai.run_game()
