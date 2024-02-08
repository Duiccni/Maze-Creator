from typing import Literal
import pygame
import random

WHITE = 0xACA293
GREEN = 0x2D3D10
RED = 0x3D102D
BLACK = 0x181A1B

TILE_SIZE = 50
TILE_AMOUNT = 4
EXTRA = 60
RRES = TILE_SIZE * TILE_AMOUNT
RES = RRES + EXTRA

n_TILE_SIZE = TILE_SIZE - 1

FPS = 10

cells = [[y * TILE_AMOUNT + x for x in range(TILE_AMOUNT)] for y in range(TILE_AMOUNT)]
EDGE_AMOUNT = TILE_AMOUNT - 1
edges = [[[1] * EDGE_AMOUNT for _ in range(TILE_AMOUNT)] for _ in range(2)]
# edges[0][y][x], edges[1][x][y]


def deleteEdge(cell: tuple[int, int], slope: int):
	edges[slope][cell[slope ^ 1]][cell[slope]] = 0


def findNextCell(cell: tuple[int, int], slope: int) -> tuple[int, int]:
	return ((cell[0] + (slope ^ 1)), (cell[1] + slope))


connections = []


def connThread(cell: tuple[int, int], val: int):
	if cells[cell[1]][cell[0]] == val:
		return
	cells[cell[1]][cell[0]] = val
	for conn in connections:
		if conn[0] == cell:
			connThread(conn[1], val)
		elif conn[1] == cell:
			connThread(conn[0], val)


def connect(cell: tuple[int, int], slope: int, data: None | tuple[int, int] = None) -> bool:
	if data == None:
		data = findNextCell(cell, slope)
	if data[0] >= TILE_AMOUNT or data[1] >= TILE_AMOUNT:
		print("Overflow", cell, data, slope)
		return True
	if cells[data[1]][data[0]] == cells[cell[1]][cell[0]]:
		print("Same ID")
		return True
	print(cells[cell[1]][cell[0]], cells[data[1]][data[0]], slope)
	connThread(data, cells[cell[1]][cell[0]])
	connections.append((data, cell))
	print((data, cell))
	deleteEdge(cell, slope)
	return False


pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((RES, RES))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 21)

running = True

last_cell = (0, 0)
last_slope = -1
err = False

while True:
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			running = False
			break
		if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
			last_cell = (random.randint(0, EDGE_AMOUNT), random.randint(0, EDGE_AMOUNT))
			last_slope = random.randint(0, 1)
			err = connect(last_cell, last_slope)
	if running == False:
		break
	screen.fill(BLACK)

	# draw grid
	for y in range(TILE_AMOUNT):
		for x in range(EDGE_AMOUNT):
			x2 = (x + 1) * TILE_SIZE
			y2 = y * TILE_SIZE
			if edges[0][y][x]:
				pygame.draw.line(
					screen,
					WHITE,
					(x2, y2),
					(x2, y2 + TILE_SIZE),
				)
			if edges[1][y][x]:
				pygame.draw.line(
					screen,
					WHITE,
					(y2, x2),
					(y2 + TILE_SIZE, x2),
				)

	if last_slope != -1:
		pygame.draw.rect(
			screen,
			RED if err else GREEN,
			(
				last_cell[0] * TILE_SIZE + 1,
				last_cell[1] * TILE_SIZE + 1,
				n_TILE_SIZE + (last_slope ^ 1) * TILE_SIZE,
				n_TILE_SIZE + last_slope * TILE_SIZE,
			),
		)

	pygame.draw.line(
		screen,
		WHITE,
		(RRES, RRES),
		(RRES, 0),
	)
	pygame.draw.line(
		screen,
		WHITE,
		(0, RRES),
		(RRES, RRES),
	)

	for y in range(TILE_AMOUNT):
		for x in range(TILE_AMOUNT):
			surface = font.render(str(cells[y][x]), 0, WHITE)
			screen.blit(surface, (x * TILE_SIZE + 5, y * TILE_SIZE + 5))

	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()
