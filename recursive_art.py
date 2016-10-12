""" Generates random computational art and sets user's background image to said art """
import random
import math
from PIL import Image
import os

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth 
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
    """
    #List of possible 'building block' functions
    prod = lambda a,b : a*b
    avg = lambda a,b : .5*(a+b)
    cos_pi = lambda a : math.cos(math.pi*a)
    sin_pi = lambda a : math.sin(math.pi*a)
    variableperiod = random.randrange(0,10)
    sin_variableperiod = lambda a : math.cos(math.pi*a*variableperiod)
    cos_variableperiod = lambda a : math.sin(math.pi*a*variableperiod)
    x = lambda a,b : a
    y = lambda a,b : b
    sqrtdiff = lambda a : math.sqrt(1-a**2)
    absolute = lambda a : abs(a)
    #list of building block functions that take 1 argument
    function_list1 = [cos_pi,sin_pi,sqrtdiff,absolute,cos_variableperiod,sin_variableperiod]
    #list of building block functions that take 2 arguments
    function_list2 = [prod,avg,x,y]
    #list of all fucntions
    function_list  = [prod,avg,cos_pi,sin_pi,x,y,sqrtdiff,absolute,cos_variableperiod,sin_variableperiod]
    def generate(depth):
        "recursively generates random function of specified depth."
        if depth <= 0:
            return random.choice([x,y])
        else:
            #pick a function from avaliable functions
            funct = random.choice(function_list)
            #generate inner function recursively and wrap
            if funct in function_list1:
                innerfunc = generate(depth - 1)
                return lambda a,b : funct(innerfunc(a,b))
            if funct in function_list2:
                innerfunc = generate(depth - 1)
                innerfunc2 = generate(depth - 1)
                return lambda a,b : funct(innerfunc(a,b),innerfunc2(a,b))
          
    return generate(random.randrange(min_depth, max_depth))

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    #figure out scaling factor based on range sizes, find appropriate place in output range for input value
    input_range = input_interval_end - input_interval_start
    output_range = output_interval_end - output_interval_start
    scaling_factor = float(output_range) / float(input_range)
    return output_interval_start + (val - input_interval_start) * scaling_factor
    
  

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(1,9)
    green_function = build_random_function(1,9)
    blue_function = build_random_function(1,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(red_function(x, y)),
                    color_map(green_function(x, y)),
                    color_map(blue_function(x, y)),
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

#generate art and place in pictures folder

name = "/home/arpan/Pictures/myart0.png"
generate_art(name,1920,1080)

#set to system background
os.system("/usr/bin/gsettings set org.gnome.desktop.background picture-uri /home/arpan/Pictures/myart0.png")



