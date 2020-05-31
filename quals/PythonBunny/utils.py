def coords_to_map(pos):
    x = pos[0]-5
    z = pos[1]-2

    grid_x = round((x/480)*64-0.5)
    grid_y = round((1-z/480)*64-0.5)

    return grid_x,grid_y

def map_to_coords(pos):
    x = ((pos[0]+0.5)/64)*480+5
    z = (1-((pos[1]+0.5)/64))*480+2

    return x,z
