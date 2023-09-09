# Writer: Muhammed Firat Ozturk
# To load the required python packages run "pip install -r .\requirements.txt" command in your terminal in this  directory (ideally with a python virtual environment)


# below will be my algorithm:
# 1 First copy all the files to a new folder, then:
# 2 resize the image (so that longest dimension is 1500 px)
# 3 convert to webp
# 4 Compress image (compress until the image file size is below 200kb or close enough to 200 kb)
# 5 Save image
# 6 Create and save thumbnail image that is 800x800 pixels
# 7 Check and print any unoptimized images

# Operating System package for python. This enables us to make changes in our files (like creating, deleting, altering) on our computer
import os
# Similar to os, but has newer features
import pathlib

# PIL stands for Python Imaging Library, and it's the original library that enabled Python to deal with images.
# We will also use ImageOps to prevent the image being rotated while we change (reduce) its dimensions
from PIL import Image, ImageOps

# Below package is for copying files from one directory to another
import shutil

# Below package is used for rounding numbers up
import math

# Below is used to exit the code if any error happens (like not having an already existing input file)
import sys



# Webp image file format has almost 30% less size on disk as jpeg even though it provides the same quality. So it is a better choice for web
def image_change_format(image_name, image_folder, format):
    image = Image.open(pathlib.Path(image_folder,image_name))
    # get the image path
    image_directory = pathlib.Path(image_folder, image_name)
    # change its file extension to the input format
    image_directory = pathlib.PureWindowsPath(image_directory)
    image_directory = image_directory.with_suffix('.'+format)
    # get the new image name with its new extension
    new_image_name = pathlib.Path(image_directory).name
    # save the image
    image.save(pathlib.Path(image_folder,image_directory), format=format)
    # If the image was already created before, and we now changed it's name (extension), then delete the old one inside the folder
    if new_image_name != image_name:
        pathlib.Path(image_folder,image_name).unlink()
    # Return the file size (in kb) and the new image name for reference. Deleted by 1024 because 1024 bytes is equal to 1 kb. And st_size gives the output in bytes
    return math.ceil(pathlib.Path(image_folder,new_image_name).stat().st_size/1024), new_image_name




# This resizes the image dimensions (while keeping aspect ratio) in pixels where the largest dimension (width or height) will not exceed dim_threshold (in pixels) provided
def image_resize(image_destination, dim_treshold):
    image = Image.open(image_destination)
    width = image.size[0]
    height = image.size[1]
    if width > dim_treshold or height > dim_treshold:
        if width > height:
            new_width = dim_treshold
            new_height = int((dim_treshold / width) * height)
        elif height > width:
            new_height = dim_treshold
            new_width = int((dim_treshold / height) * width)
        elif width == height and width > dim_treshold:
            new_height = dim_treshold
            new_width = dim_treshold

        # When you use Image.convert('RGB') it just converts each pixel to the triple 8-bit value. So it fundamentally changes the mode of how image is represented and stored.
        image.convert("RGB")

        # Now let's resize the image according to the new height and width
        # There are 6 resample options: 0,1,2,3,4,5. See below
        # Image.NEAREST (0)
        # Image.LANCZOS (1)
        # Image.BILINEAR (2)
        # Image.BICUBIC (3)
        # Image.BOX (4)
        # Image.HAMMING (5)

        # One gives the most preserved with highest quality, (says the internet ekke)
        image = image.resize((new_width, new_height), resample=1)
        # Below keeps the image in its original orientation (NOT ROTATED RIGHT OR LEFT) - We do this because for some reason the image can get rotated during optimization
        image = ImageOps.exif_transpose(image)
        image.save(image_destination)
        # return the file size in kbs, also its final dimensions in pixels
        return (
            math.ceil(pathlib.Path(image_destination).stat().st_size / 1024),
            new_width,
            new_height,
        )
    else:
        # If the operation was not needed and not performed, then return False
        return False


# Lowering the image quality by resaving it using a custom quality. 
def image_lower_quality(image_directory, quality):
    image = Image.open(image_directory)
    # Change the quality to the input quality and save
    image.save(image_directory, optimize=True, quality=quality)
    # returns the new image file size value in kbs
    return math.ceil(pathlib.Path(image_directory).stat().st_size / 1024)

#  Compresses image, and returns the final size of the image file in kbs
def compress_image(image_directory, compress_level):
    image = Image.open(image_directory)
    # save the image with its inputted compress level
    image.save(image_directory, compress_level = compress_level, optimize=True,)
    return math.ceil(pathlib.Path(image_directory).stat().st_size / 1024)

# Now let's see if we have any images that are not optimized (processed) to the output folder
def failed_to_optimize_images(origin_directory, copy_directory, image_format):
    # Initialize an empty array to store the non-processed images
    array = []
    # bring the list of original image names
    original_image_names = os.listdir(origin_directory)
    # bring the list of copied image names
    copy_image_names = os.listdir(copy_directory)

    # iterate through every original_image name
    for image_name in original_image_names:
        # change the name to include the new extension it would have (such as webp)
        image_directory = pathlib.Path(origin_directory,image_name)
        image_directory = pathlib.PureWindowsPath(image_directory)
        image_directory = image_directory.with_suffix('.'+image_format)
        image_name = image_directory.name
        # If original image name is not inside the copied image name then append the original image name string to the array for later display
        if (image_name not in copy_image_names):
            array.append(image_name)
    return array

# Creating thumbnails that of size 800x800 pixels
def create_thumbnail(image_directory,thumbnail_directory):
    image = Image.open(image_directory)
    image.thumbnail((800,800),resample=3,reducing_gap=2.0)
    image.save(thumbnail_directory)


# Below function copies the file and saves it at the copy_destination, and returns the size of the file copied in kbs
def copy_file(original_destination, copy_destination):
    shutil.copy(original_destination, copy_destination)
    return math.ceil(pathlib.Path(copy_destination).stat().st_size / 1024)

def optimize():
    # Let's get the current directory and store it in path variable
    path = pathlib.Path.cwd()
    # First tell the program where the input images are located.
    input_folder_name = 'input'
    input_folder = pathlib.Path(path,input_folder_name)
    # Now let's define where to save our optimized output images
    output_folder_name = 'output'
    output_folder = pathlib.Path(path,output_folder_name)
    thumbnail_folder_name = 'thumbnail'
    thumbnail_folder = pathlib.Path(output_folder,thumbnail_folder_name)

    # If there are no files inside the input folder, exit the application with a warning
    try:
        if len(os.listdir('input')) == 0:
            sys.exit('You have not provided any images in the input folder that I can optimize. Please add your images in the input folder')
    # If the input folder does not exists
    except(FileNotFoundError):
        os.mkdir(input_folder)
        sys.exit('An input folder is now created for you. Please add files to the input folder to optimize')

    # If the output_folder and thumbnail_folders do not already exists, add them. If they already exists, do not do anything.
    try:
        os.mkdir(output_folder)
    except(FileExistsError):
        pass

    # Similarly
    try:
        os.mkdir(thumbnail_folder)
    except(FileExistsError):
        pass

    # assign image names to the array raw_images
    input_image_names = os.listdir(input_folder)
    # Let's also check how many images we need to optimize
    number_of_images = len(input_image_names)
    # We will count how many images we optimized, so let's initialize the integer to 0 and iterate then
    optimized_image_counter = 0
    # Do below operations for every image
    for input_image_name in input_image_names:
        # initialize to change later and save
        output_image_name = input_image_name
        optimized_image_counter += 1
        # below is to know how many images are left to optimize and what is being currently optimized, and what percentage has been completed.
        print(f"-------- Image: {input_image_name} ---------: {optimized_image_counter}/{number_of_images} ({math.floor(optimized_image_counter/number_of_images*100)}%)")

        #Now we will need to copy all the images before we work on them.
        # Define original file destination
        original_destination = pathlib.Path(input_folder,input_image_name)
        # Define where to copy the file
        copy_destination = pathlib.Path(output_folder,input_image_name)

        # ---- OPERATION 1 ------> IMAGE COPYING
        # Copy the file and get its file size so we can compare
        # Check to see if the file already exists first to avoid errors
        if os.path.isfile(copy_destination)==False:
            file_size = copy_file(original_destination, copy_destination)

        # ---- OPERATION 2 ------> IMAGE RESIZING
        # now let's resize the image if it needs it (one or two of its dimensions is above 1500 pixels)
        # set a limit the largest dimension the image can have and store it in the dim_thresold variable 
        dim_treshold = 1500
        # below variable, image_resize_output is equal to false if the image does not need resizing, or equal to three different variables: file_size, new_width, new_height if it went thru resizing
        image_resize_output = image_resize(copy_destination,dim_treshold)
        # If it needs resizing
        if image_resize_output!=False:
            # reside the image and get the output values
            file_size, new_width, new_height = image_resize_output
            print(
                f"Image needed dimension resizing. The new size is: {file_size} KB; The New Width: {new_width} pixels, and The New Height: {new_height} pixels"
            )

        # ---- OPERATION 3 ------> CONVERT TO WEBP
        # lets convert it to webp for further optimization
        image_format = 'webp'
        if(original_destination.suffix!= image_format):
            file_size, output_image_name = image_change_format(image_name = input_image_name,image_folder = output_folder, format = image_format)
            print(f'The file size after converting to webp has been reduced to: {file_size}')

        # ---- OPERATION 4 ------> COMPRESS IMAGE
        # The compression level is a measure of the compression quality. It is expressed as an integer in the range 1 - 9. 
        # Compression quality and performance are conflicting goals. 
        # Compression level 1 provides best performance at the expense of quality.
        file_size = compress_image(pathlib.Path(output_folder, output_image_name), compress_level=2)
        print(f'The file size after compressing the image has been reduced to: {file_size}')

        # If file size is still above 200 kb then, optimize iteratively with image_lower_quality function
        quality = 100
        while(file_size>200 and quality>40):
            quality -= 10
            file_size = image_lower_quality(output_folder+output_image_name, quality)
            print(f'Image is compressed again,\nfinal size is {file_size}')

        # --------- Operation 5 - Creating Thumbnail -----------
        # first input is the location of non-thumbnail image. Second is the destination where it will be saved (includes the file name too).
        create_thumbnail(pathlib.Path(output_folder, output_image_name), pathlib.Path(thumbnail_folder,output_image_name))

    # Below function returns an array of names of the failed to optimize images, if any.
    failed_to_optimize = failed_to_optimize_images(input_folder,output_folder, image_format)
    if (len(failed_to_optimize)!=0):
        print(f'below images are not copied')
        print(failed_to_optimize)


optimize()

