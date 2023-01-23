import pygame
import random
import time
pygame.init()

class SortWindowData:
    # Colors
    black = (50,50,50)
    white = 255, 255, 255
    green = 83, 194, 77
    red = (233,150,122)
    background_color = black

    block_gradient = [
        (70, 180, 231),
        (137,207,240),
        (28,154,213)
    ]

    # Font
    font = pygame.font.SysFont('timesnewroman', 15)
    large_font = pygame.font.SysFont('timesnewroman', 30)

    # Padding
    horizontalpad = 100
    verticalpad = 150

    def __init__(self, width, height, lst):
        # Define width and height of window
        self.width = width
        self.height = height
        # Creates pygame window with width and height
        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption('Sorting Algorithm Visualizer')

        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        # Defines how large the blocks can be width wise (The more blocks (len) the smaller the amount of pixels for width)
        self.blockwidth = (self.width - self.horizontalpad) // len(lst)
        # Defines how large the blocks can be height wise (The larger the range of the list the smaller the amount of pixels for each number of height)
        self.blockheight = (self.height - self.verticalpad) // (self.max_val - self.min_val)
        # Defines how far into the X axis do the blocks start (After the horizontal padding)
        self.blockstartX = self.horizontalpad // 2

#Writes the text and blocks onto the display

def Displaywindow(SortWindow,sorting_algo_name,ascending,array_size):
    # Fills the window with white // Clears the screen
    SortWindow.window.fill(SortWindowData.background_color)
    # Render the title onto the middle of the widnow screen
    title = SortWindow.large_font.render(f"{sorting_algo_name} - {'Ascending' if ascending else 'Descending'} | [Size] = {array_size}", 1, SortWindow.red)
    # Blits the title  onto the middle of the window screen
    SortWindow.window.blit(title,((SortWindow.width//2 - title.get_width()//2), 5))
    # Render the controls text using the font (SortWindow.(font).render('Text', Antialiasing (Set to 1), color)
    controls = SortWindow.font.render('Controls: SPACE - Start / R - Reset / A - Ascending / D - Descending / Plus - Increase size / Minus - Decrease size', 1, SortWindow.white)
    # Blits the controls onto the middle of the window screen
    SortWindow.window.blit(controls,((SortWindow.width//2 - controls.get_width()//2), 40))
    # Render the sorting text using the font (SortWindow.(font).render('Text', Antialiasing (Set to 1), color)
    sorting_controls = SortWindow.font.render('I - Insertion Sort / B - Bubble Sort / S - Selection Sort / Q - Quick Sort', 1, SortWindow.white)
    # Blits the sorting controls onto the middle of the window screen lower than the normal controls
    SortWindow.window.blit(sorting_controls,((SortWindow.width//2 - sorting_controls.get_width()//2), 60))
    # Draws the list as blocks
    create_blocks(SortWindow)
    # Updates the display
    pygame.display.update()

# Creates the rectangle blocks (pygame top left starts at (0,0) x and y increase as you move towards the right and down respectfully)

def create_blocks(SortWindow, color_position={}, clear_bg = False):
    # Initialize class attribute lst to lst to avoid typing SortWindow.lst
    lst = SortWindow.lst

    if clear_bg:
        clear_rect = (SortWindow.horizontalpad//2,SortWindow.verticalpad,
                      SortWindow.width-SortWindow.horizontalpad,SortWindow.height-SortWindow.verticalpad)
        pygame.draw.rect(SortWindow.window,SortWindow.background_color,clear_rect)
    # Loops through each index and value in list to create the blocks
    for i,val in enumerate(lst):
        # Finds the x value of block by starting at blockstartx adds index and multiplies by block width
        x = SortWindow.blockstartX + i * SortWindow.blockwidth
        # Find the y value of block by taking the height of window (600) - value (ex 100) - minval (ex 20) = 520 * block height
        y = SortWindow.height - (val - SortWindow.min_val) * SortWindow.blockheight
        # Find the color of this rectangle block by choosing between the 3 in the gradient
        color = SortWindow.block_gradient[i % 3]

        if i in color_position:
            color = color_position[i]
        # Draw the rectangle block onto the screen (Window, color, (top left x, y, block width, block height)
        pygame.draw.rect(SortWindow.window, color, (x, y, SortWindow.blockwidth, SortWindow.height))
    if clear_bg:
        pygame.display.update()

# Creates a random unsorted list with n amount of numbers ranging from min_val to max_val

def generate_unsorted_list(n, min_val, max_val):
    lst = []
    for i in range(n):
        random_value = random.randint(min_val, max_val)
        lst.append(random_value)
    return lst

# Bubble sort algorithm

def bubble_sort(SortWindow, ascending=True):
    lst = SortWindow.lst

    for i in range(len(lst) -1):
        for j in range(len(lst) -1 -i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                create_blocks(SortWindow,{j: SortWindow.green, j+1: SortWindow.red}, True)
                yield True
    return lst

# Insertion sort algorithm

def insertion_sort(SortWindow, ascending=True):
    lst = SortWindow.lst

    for i in range(1, len(lst)):
        curr = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i-1] > curr and ascending
            descending_sort = i > 0 and lst[i-1] < curr and not ascending

            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i-1]
            i = i -1
            lst[i] = curr
            create_blocks(SortWindow, {i-1: SortWindow.green, i: SortWindow.red}, True)
            yield True
    return lst

# Quick sort algorithm

def quick_sort(SortWindow, ascending=True):
    lst = SortWindow.lst
    # function to find the partition position
    def partition(array, low, high, ascending):

        # choose the rightmost element as pivot
        pivot = array[high]

        # pointer for greater element
        i = low - 1

        # traverse through all elements
        # compare each element with pivot
        for j in range(low, high):
            if (array[j] <= pivot and ascending) or (array[j] >= pivot and not ascending):
                # if element smaller than pivot is found
                # swap it with the greater element pointed by i
                i = i + 1

                # swapping element at i with element at j
                (array[i], array[j]) = (array[j], array[i])
            time.sleep(0.015)
            create_blocks(SortWindow, {i: SortWindow.red, j: SortWindow.green, pivot: (255,0,255)},True)
        # swap the pivot element with the greater element specified by i
        (array[i + 1], array[high]) = (array[high], array[i + 1])
        # return the position from where partition is done
        return i + 1



    # function to perform quicksort
    def quickSort(array, low, high):
        if low < high:
            # find pivot element such that
            # element smaller than pivot are on the left
            # element greater than pivot are on the right
            pi = partition(array, low, high,ascending)

            # recursive call on the left of pivot
            quickSort(array, low, pi - 1)

            # recursive call on the right of pivot
            quickSort(array, pi + 1, high)
    quickSort(lst, 0, len(lst)-1)
    return lst

# Selection sort algorithm

def selection_sort(SortWindow, ascending=True):
    lst = SortWindow.lst

    for i in range(len(lst)):
        index = i
        for j in range(i+1, len(lst)):
            if (lst[j] < lst[index] and ascending) or (lst[j] > lst[index] and not ascending):
                index = j
        create_blocks(SortWindow, {i: SortWindow.green, index: SortWindow.red}, True)
        yield True
        lst[i],lst[index] = lst[index],lst[i]
    return lst


# Running the main window

def SortingVisualizer():
    run = True

    # Define variable clock to determine how many times per second will this loop check for updated event
    clock = pygame.time.Clock()

    # Define variables for random list
    n = 50
    min_val = 1
    max_val = 200
    speed = 60

    # Create the unsorted list and Create the window object
    lst = generate_unsorted_list(n, min_val, max_val)
    SortWindow = SortWindowData(800, 600, lst)

    doSort = False
    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None


    # Continous loop to keep pygame updating and running
    while run:
        # 60 times per second
        clock.tick(speed)

        if doSort:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                doSort=False
            except TypeError:
                doSort=False
        else:
            Displaywindow(SortWindow,sorting_algo_name,ascending,n)

        # Return a list of all events that have occured since the last iteration of the loop
        for event in pygame.event.get():
            # If user quits by hitting the X then break the loop and jump to pygame.quit()
            if event.type == pygame.QUIT:
                run = False
            # If the user does not press any key then continue
            if event.type != pygame.KEYDOWN:
                continue
            # If the user pressed the key 'R' then remake the list
            if event.key == pygame.K_r:
                # Recreate the list with new random values
                lst = generate_unsorted_list(n, min_val, max_val)
                # Reintialize the new list to the SortWindow object
                SortWindow.set_list(lst)
                # Stop sorting and rerandomize the list
                doSort = False
            # If the user pressed the key 'SPACE' then sort the list
            elif event.key == pygame.K_SPACE and doSort == False:
                # Set doSort to True --> Starting the sorting algorithm
                doSort = True
                sorting_algorithm_generator = sorting_algorithm(SortWindow,ascending)
            elif event.key == pygame.K_a and not doSort:
                ascending = True
            elif event.key == pygame.K_d and not doSort:
                ascending = False
            elif event.key == pygame.K_i and not doSort:
                sorting_algorithm = insertion_sort
                sorting_algo_name = 'Insertion Sort'
            elif event.key == pygame.K_b and not doSort:
                sorting_algorithm = bubble_sort
                sorting_algo_name = 'Bubble Sort'
            elif event.key == pygame.K_q and not doSort:
                sorting_algorithm = quick_sort
                sorting_algo_name = 'Quick sort'
            elif event.key == pygame.K_s and not doSort:
                sorting_algorithm = selection_sort
                sorting_algo_name = 'Selection sort'
                speed = speed // 5
            elif event.key == pygame.K_KP_PLUS and not doSort and n < 100:
                n += 10
                speed += 20
                lst = generate_unsorted_list(n, min_val, max_val)
                SortWindow.set_list(lst)
            elif event.key == pygame.K_KP_MINUS and not doSort and n > 10:
                n -= 10
                speed -= 14.5
                lst = generate_unsorted_list(n, min_val, max_val)
                SortWindow.set_list(lst)

    pygame.quit()

if __name__ == '__main__':
    SortingVisualizer()
