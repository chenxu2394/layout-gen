import os
import sys
import itertools

def generate_base_grid(width, height):
    grid = []
    for row in range(height):
        line = []
        if row % 2 == 0:
            # Even rows: all 'r's
            line = ['r'] * width
        else:
            # Odd rows: 'rQ' pattern
            for col in range(width):
                if col % 2 == 0:
                    line.append('r')
                else:
                    line.append('Q')
            # Adjust the line length if width is odd
            if len(line) < width:
                line.append('r')
        grid.append(line)
    return grid

def apply_patches(grid, patch_positions, patch_width, patch_height):
    # Create a deep copy of the grid
    new_grid = [row.copy() for row in grid]
    patch_num = 1
    for (start_row, start_col) in patch_positions:
        for i in range(start_row, start_row + patch_height):
            for j in range(start_col, start_col + patch_width):
                new_grid[i][j] = str(patch_num)
        patch_num += 1
    return new_grid

def save_grid_to_file(grid, filename):
    with open(filename, 'w') as f:
        for row in grid:
            f.write(''.join(row) + '\n')

def main():
    # Check command-line arguments
    if len(sys.argv) != 6:
        print("Usage: python gen.py grid_width grid_height number_of_patches patch_width patch_height")
        sys.exit(1)
    
    # Parse command-line arguments
    try:
        grid_width = int(sys.argv[1])
        grid_height = int(sys.argv[2])
        number_of_patches = int(sys.argv[3])
        patch_width = int(sys.argv[4])
        patch_height = int(sys.argv[5])
    except ValueError:
        print("All arguments must be integers.")
        sys.exit(1)
    
    # Validate dimensions
    if not (1 <= grid_width <= 16 and 1 <= grid_height <= 16):
        print("Grid width and height must be integers between 1 and 16.")
        sys.exit(1)
    if not (1 <= patch_width <= grid_width and 1 <= patch_height <= grid_height):
        print("Patch dimensions must be positive integers within the grid dimensions.")
        sys.exit(1)
    if not (1 <= number_of_patches <= (grid_width * grid_height) // (patch_width * patch_height)):
        print("Number of patches is too large for the grid size.")
        sys.exit(1)
    
    base_grid = generate_base_grid(grid_width, grid_height)
    
    # Create 'layouts' directory if it doesn't exist
    output_dir = 'layouts'+str(grid_width)+'x'+str(grid_height)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    layout_num = 1  # To number the layout files
    
    # Calculate all possible positions for one patch
    max_row_position = grid_height - patch_height + 1
    max_col_position = grid_width - patch_width + 1
    all_positions = [
        (row, col)
        for row in range(max_row_position)
        for col in range(max_col_position)
    ]
    
    # Generate all combinations of patch positions without overlap
    # For multiple patches, we need to select combinations of positions where patches do not overlap
    possible_combinations = itertools.combinations(all_positions, number_of_patches)
    
    for patch_positions in possible_combinations:
        # Check for overlapping patches
        occupied_cells = set()
        overlap = False
        for (start_row, start_col) in patch_positions:
            for i in range(start_row, start_row + patch_height):
                for j in range(start_col, start_col + patch_width):
                    if (i, j) in occupied_cells:
                        overlap = True
                        break
                    occupied_cells.add((i, j))
                if overlap:
                    break
            if overlap:
                break
        if overlap:
            continue  # Skip combinations with overlapping patches
        
        # Apply the patches to the base grid
        patched_grid = apply_patches(base_grid, patch_positions, patch_width, patch_height)
        
        # Construct the filename
        filename = f'layout_{grid_width}x{grid_height}_{layout_num}_{number_of_patches}_{patch_width}x{patch_height}.txt'
        filepath = os.path.join(output_dir, filename)
        
        # Save the new grid layout to a file
        save_grid_to_file(patched_grid, filepath)
        layout_num += 1

    print(f"Generated {layout_num - 1} layouts.")

if __name__ == "__main__":
    main()