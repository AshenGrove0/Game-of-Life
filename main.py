# make display graphically though like ths behind the scenes
import numpy as np
import pprint
import time
# work through this in vscode with a proper debugger
'''
Any live cell with fewer than two live neighbours dies, as if by underpopulation.

Any live cell with two or three live neighbours lives on to the next generation.

Any live cell with more than three live neighbours dies, as if by overpopulation.

Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
'''
# add an option for random noise start
board_diamensions = {
    'x': 5,
    'y': 7
}
alive_coords_to_start = [(3,2),(3,3),(3,4)]
def main():
    board = generate_starting_board()
    pprint.pp(board)
    run(board) # let user choose num2
    #do this recursively

def generate_starting_board():
    board = [[0 for i in range(board_diamensions['x'])] for i in range(board_diamensions['y'])]
    #print(board)
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            if (row, column) in alive_coords_to_start:
                board[row][column] = 1
            else:
                #print(row,column)
                board[row][column] = 0
    return board

def check_if_all_dead(board) -> bool:
    alive = False
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            if board[row][column] == 1:
                alive = True
    return alive
    
def run(board: list):
    ''' FIX ALGORITHM AS CHECKING FOR DEAD CELL DEOSNT WORK PERFECTLY AND TIMESLEEP DOESNT WORK AFTER FIRST RECURSION'''
    time.sleep(2)

    #print(board)
    board = list(board)
    all_cell_neighbour_counts = {
        (range(board_diamensions['x']),range(board_diamensions['y'])): 'neighbour_count'
    }
    #print(all_cell_neighbour_counts)
    all_cell_neighbour_counts = {}
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            all_cell_neighbour_counts.update({(row,column):None})
    #print(all_cell_neighbour_counts)
    adjacent_coords = [ # check if diagonals count
        (+1, 0),
        (-1, 0),
        (0, +1),
        (0,-1),
        (+1,+1),
        (-1,+1),
        (+1,- 1),
        (-1,- 1)
    ]
    for cell,count in all_cell_neighbour_counts:
        neighbour_count = 0
        for relative_coord in adjacent_coords:
            adjacent_coord = tuple(np.add(cell, relative_coord))
            #print(type(board))
            try:  # Try: Except: required here as may go past end of array
                if board[adjacent_coord[0]][adjacent_coord[1]] == 1:
                    neighbour_count+=1
            except:
                pass
        all_cell_neighbour_counts.update({(cell,count):neighbour_count})
    print(all_cell_neighbour_counts)
    #print(all_cell_neighbour_counts)

    new_board = board
    for row in range(board_diamensions['y']):
        for column in range(board_diamensions['x']):
            neighbour_count = all_cell_neighbour_counts.get((row, column))
            
            # good spot to include some tests
            #for live cells
            if board[row][column] == 1:
                if neighbour_count < 2 or neighbour_count > 3:
                    new_board[row][column] = 0
                elif neighbour_count == 2 or neighbour_count == 3:
                    new_board[row][column] = 1
            # for dead cells
            if board[row][column] == 0:
                if neighbour_count == 3:
                    new_board[row][column] = 1
    
    # check if 0-index errors
    pprint.pp(new_board)
    #all_dead: bool = check_if_all_dead(new_board)
    #if all_dead:
    #    pprint.pp([[0 for col in range(board_diamensions['x'])] for row in range(board_diamensions['y'])])
    #    print("All dead")
    #    quit()

    print('new board')
    print(new_board)
    print('foothillsofthehimalayas')
    run(new_board)
        


    # make it stop if all cells dead
if __name__ == '__main__':
    main()