# Writer: Muhammed Firat Ozturk

# Image SEO tips:
# #1 Rename your images, they should be descriptive
#   rename your images (it affects your seo!) use keywords!
#   keyword reasearch: select and use one "focus" keyword and Supporting keywords for Each page and Blog post (The focus keyword is simply the search term you want your post or page to be ranked for in the search engines. So when the audience looks out for that specific phrase or keyword in the search engines, they should probably locate you.)
#   Use hyphens, not underscores, to separate words—for example, query-data.html. Search engines interpret hyphens in file and directory names as spaces between words. Underscores are generally not recognized, meaning that their presence can negatively affect SEO. (Source: https://developers.google.com/style/filenames#:~:text=Use%20hyphens%2C%20not%20underscores%2C%20to,presence%20can%20negatively%20affect%20SEO.)
# #2 Write seo friendly alt text -> search engines, screen readers, and people with disabilities
#   Do not forget to set the alt text for the image (you can just take the image and remove its hyphens conveniently)
# #3 Use jpg or jpeg (I will go with jpeg)
# Ideally images should be less than 100 kb. But I will keep it below 200 kb for now. Should be fine. (Amazon images are around 150 kbs)
# for actual image keep the longest side below 1500 px (That's what amazon does)
# for thumbnails keep the longest side below 800 px, also use the webp format for them. Their file size should be less than 72 kb (That's also how amazon does)
# for any images that span the entire width of the browser, images should be 2560 pixels in width,

# below will be my algorithm:
# 1 First copy all the files to a new folder, then:
# 2 convert to jpeg, and change its name
# 3 resize the image and check its size again. If its above 200 kbs then:
# 4 optimize the image
# 5 optimize the image another way

# Operating System package for python. This enables us to make changes in our files (like creating, deleting, altering) on our computer
import os

# PIL stands for Python Imaging Library, and it's the original library that enabled Python to deal with images.
# We will also use ImageOps to prevent the image being rotated while we change (reduce) its dimensions
from PIL import Image, ImageOps

# Below package is for copying files from one directory to another
import shutil

# Below is for converting png to jpg. (OpenCV) It actually does very other things like machine learning. But we will use it simply in here.
import cv2

# Below package is used for rounding numbers up
import math


# ------------------ Ignore below code, it is for my reference only. -----------------
# state the path of the image(s)
# image_path = os.getcwd()+"/images/"
# state the name of the image
# image_name = "1056.jpg"
# write down the image destination
# image_destination = image_path + image_name
# Save the image in a variable
# image = Image.open(image_destination)
# Print out image information
# print(image.format, #shows the file type of the image
#        image.size, #shows the dimensions if the image in pixels, width x height
#          image.mode, #shows the color model/system (rgb etc)
#            os.stat(image_destination).st_size) #shows the size of the image in bytes
# ------------------ Ignore above code, it is for my reference only. -----------------


# You can resize the image to lower its size but I will not do that.
# new_image = image.resize((500,469),resample=1) #There are 6 resample options: 0,1,2,3,4,5. See below
# Image.NEAREST (0)
# Image.LANCZOS (1)
# Image.BILINEAR (2)
# Image.BICUBIC (3)
# Image.BOX (4)
# Image.HAMMING (5)

# Converting image to the jpeg format.
# This also reduces the sizes of already jpeg files as well.
# This function is not used.
def image_to_jpeg(image_name, images_folder):
    # read the file using the cv2 package
    image = cv2.imread(images_folder + image_name)
    # new file name
    new_image_name = image_name.split(".")[0] + ".jpeg"
    # new path string
    new_image_path = images_folder + new_image_name
    # Note with .jpg or .jpeg format, to maintain the highest quality, you must specify the quality value from [0..100] (default value is 94 _ same as the file itself). Simply do this:
    cv2.imwrite(
        # Path where to save the image
        new_image_path,
        # What image to save
        image,
        # Assigning the quality for jpeg image
        # The number represents the quality from scale 0-100
        [int(cv2.IMWRITE_JPEG_QUALITY), 30],
    )
    # If the image already created before, and we now changed it's name (extension), then delete the old one
    if new_image_path != images_folder + image_name:
        os.remove(images_folder + image_name)
    # Return the file size and the new image name for reference
    return math.ceil(os.path.getsize(new_image_path) / 1024), new_image_name


# Webp image file format has almost 30% less size on disk as jpeg even though it provides the same quality. So it is a better choice for web
def image_change_format(image_name, image_folder, format):
    # Open the image
    image = Image.open(image_folder + image_name)
    # Define its new name for reference
    new_image_name = image_name.split(".")[0] + "." + format
    # save the image with its new name, and new format
    image.save(image_folder + new_image_name, format=format)
    # If the image already created before, and we now changed it's name (extension), then delete the old one
    if new_image_name != image_name:
        os.remove(image_folder + image_name)
    # Return the file size (in kb) and the new image name for reference
    return math.ceil(os.path.getsize(image_folder + new_image_name)/1024), new_image_name

    # next time try below
    # cv2.imwrite("myfile.webp", cv2image, [int(cv2.IMWRITE_WEBP_QUALITY), 20])


# This resizes the image dimensions in pixels where the largest dimension (width or height) will not exceed dim_threshold (in pixels) provided
def image_resize(image_destination, dim_treshold):
    # Open the image you want to make changes to
    image = Image.open(image_destination)
    # get image width
    width = image.size[0]
    # get image height
    height = image.size[1]
    # If the width or height is higher than the maximum longest dimension allowed, then make changes
    if width > dim_treshold or height > dim_treshold:
        if width > height:
            new_width = dim_treshold
            # Below keeps the ratio and height to be the same as the original.
            new_height = int((dim_treshold / width) * height)
        elif height > width:
            new_height = dim_treshold
            # Below keeps the ratio and height to be the same as the original.
            new_width = int((dim_treshold / height) * width)
        # If the width and height of the image is the same, then make them both equal to the maximum dimension allowed (dim_thresold)
        elif width == height and width > dim_treshold:
            new_height = dim_treshold
            new_width = dim_treshold

        # Convert image to RGB
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
        # One gives the most preserved with highest quality, they say
        image = image.resize((new_width, new_height), resample=1)
        # Below keeps the image in its original orientation (NOT ROTATED RIGHT OR LEFT)
        image = ImageOps.exif_transpose(image)
        # Save the image to the destination provided
        image.save(image_destination)
        # return the file size in kbs
        return (
            # return the file size in kbs (without /1024, it would give it in bytes)
            math.ceil(os.path.getsize(image_destination) / 1024),
            # return width
            new_width,
            # return height
            new_height,
        )
    else:
        # If the operations did not have be performed, then return False
        return False
    # also later rotate the image to the correct way by looking at the previous dimensions


# Lowering the image quality by saving it again using a custom quality value. I need this to use it repetitively for files not giving up to be over 200kbs
def image_lower_quality(image_directory, quality):
    # Open image
    image = Image.open(image_directory)
    # Change the quality and save
    image.save(image_directory, optimize=True, quality=quality)
    # return the new size value in kbs
    return math.ceil(os.path.getsize(image_directory) / 1024)

# let's compress the image before we reduce its quality manually. Returns the outcome size of the file in kbs
def compress_image(image_directory, compress_level):
    # open the image
    image = Image.open(image_directory)
    # save the image with its compres level
    image.save(image_directory, compress_level = compress_level, optimize=True,)
    return math.ceil(os.path.getsize(image_directory)/1024)

# Now let's see if we have any images that are not optimized (processed) to the output folder
def failed_to_optimize_images(origin_directory, copy_directory, image_format):
    # Initialize an empty array to store the non-processed images
    array = []
    # bring original image names
    original_image_names = os.listdir(origin_directory)
    # bring the copy image names
    copy_image_names = os.listdir(copy_directory)
    # create an index iterator
    i = 0
    # iterate through every original_image name
    for image_name in original_image_names:
        # change the name to include the new extension it might have
        image_name = image_name.split('.')[0]+'.'+image_format
        # If that name is not 
        if (image_name not in copy_image_names):
            array.append(image_name)
        i+=1
    return array

# Creating thumbnails that of size 800x800 pixels
def create_thumbnail(image_directory,thumbnail_directory):
    image = Image.open(image_directory)
    image.thumbnail((800,800),resample=3,reducing_gap=2.0)
    image.save(thumbnail_directory)


# This is not worth it, colors are important for me. Let's keep them there, plus it is not losing much file size, only around 10 kbs
# This function is not being used in the algorithm.
def reduce_colors(image_directory):
    image = Image.open(image_directory)
    # get the number of colors
    # num_colors = len(image.getcolors())
    num_colors = image.getcolors()
    # Color options could be:
    # 127
    # 63
    # 31
    # 15
    image = image.convert("P", palette=Image.ADAPTIVE, colors=63)
    image.save(image_directory)
    return (math.ceil(os.path.getsize(image_directory)/1024))

# Below function copies the file and saves it at the copy_destination, and returns the size of the file copied in kbs
def copy_file(original_destination, copy_destination):
    shutil.copy(original_destination, copy_destination)
    return math.ceil(os.path.getsize(copy_destination) / 1024)

# next step is to returning images from the functions and 
def optimize():
    # Let's get the current directory in a string form
    path = os.getcwd()
    # First tell the program where the input images are located.
    input_folder = path + "\\input\\"
    # Now let's define where to save our optimized output images
    output_folder = path + "\\output\\"

    # If the above folders do not already exist, then the application itself creates it
    if(os.path.isdir('input')==False):
        os.mkdir(input_folder)
        # Exit application with error message
        return('Error: There were no input folder found \nPlease add your image files in the now created input folder')
    # Creates the output folder
    if(os.path.isdir('output')==False):
        os.mkdir(output_folder)

    # assign image names to the array raw_images
    input_image_names = os.listdir(input_folder)
    # Let's also check how many images we need to optimize
    number_of_images = len(input_image_names)
    # We will count how many images we optimized, so let's initialize the integer to 0
    optimized_image_counter = 0
    # Do below operations for every image
    for input_image_name in input_image_names:
        output_image_name = input_image_name
        # Iterate with each optimized image
        optimized_image_counter += 1
        # below is to know how many images are left to optimize and what is being currently optimized, and what percentage has been completed.
        print(f"-------- Image: {input_image_name} ---------: {optimized_image_counter}/{number_of_images} ({math.floor(optimized_image_counter/number_of_images*100)}%)")

        #Now we will need to copy all the images before we work on them.
        # Define original file destination
        original_destination = input_folder + input_image_name
        # Define where to copy the file
        copy_destination = output_folder + input_image_name

        # ---- OPERATION 1 ------> IMAGE COPYING
        # Copy the file and get its size so we can compare
        # Check to see if the file already exists i
        if os.path.isfile(copy_destination)==False:
            file_size = copy_file(original_destination, copy_destination)

        # ---- OPERATION 2 ------> IMAGE RESIZING
        # now let's resize the image if it needs it (one or two of its dimensions is above 1500 pixels)
        # below variable is false if the image does not need resizing, or equal to three different variables: file_size, new_width, new_height if it went thru resizing

        # set a limit the largest dimension the image can have and store it in the dim_thresold variable 
        dim_treshold = 1500
        image_resize_output = image_resize(copy_destination,dim_treshold)
        # If it does not resizing
        if image_resize_output!=False:
            # reside the image and get the output values
            file_size, new_width, new_height = image_resize_output
            print(
                f"Image needed dimension resizing. The new size is: {file_size} and New Width: {new_width}, New Height: {new_height}"
            )

        # ---- OPERATION 3 ------> CONVERT TO WEBP
        # lets convert it to webp for further optimization
        image_format = 'webp'
        if(input_image_name.split('.')[1]!= image_format):
            print('The file needs to be converted to webp')
            file_size, output_image_name = image_change_format(image_name = input_image_name,image_folder = output_folder, format = image_format)
            print(f'File size after converting to webp is: {file_size}')

        # ---- OPERATION 4 ------> COMPRESS IMAGE
        # The compression level is a measure of the compression quality. It is expressed as an integer in the range 1 - 9. 
        # Compression quality and performance are conflicting goals. 
        # Compression level 1 provides best performance at the expense of quality.
        file_size = compress_image(output_folder + output_image_name, compress_level=2)
        print(f'File size after compressing the image is: {file_size}')

        # Cancelled operation due to inefficiency
        # file_size = reduce_colors(output_folder+new_image_name)
        # print(f'File size after reducing the colors of the image is: {file_size}')
        quality = 100
        while(file_size>200 and quality>40):
            quality -= 10
            file_size = image_lower_quality(output_folder+output_image_name, quality)
            print(f'Image is compressed again,\nfinal size is {file_size}')


        # --------- Operation 5 - Creating Thumbnail -----------
        # first input is the location of non-thumbnail image. Second is the destination where it will be saved (includes the file name too).
        create_thumbnail(output_folder + output_image_name, output_folder+'/thumbnail/thumbnail_'+output_image_name)

    # Below function returns an array
    failed_to_optimize = failed_to_optimize_images(input_folder,output_folder, image_format)
    if (len(failed_to_optimize)!=0):
        print(f'below things are not copied')
        print(failed_to_optimize)

        









optimize()

# def trial(image_path = os.getcwd()):
#     # image_path += '\\images\\1404T-2.jpeg'
#     # reduce_colors(image_path)
#     raw_images_folder = "C:\\Users\\firat\\Desktop\\code\\karven\\frontend\\public\\CurtainFabricCodesPics\\"
#     output_folder = ("C:\\Users\\firat\\Desktop\\code\\karven\\frontend\\public\\images_optimized\\")
#     print(len(os.listdir(raw_images_folder)))
#     print(len(os.listdir(output_folder)))
#     failed_to_optimize = failed_to_optimize_images(raw_images_folder,output_folder)
#     print(f'below things are not copied, there are {len(failed_to_optimize)} files')
#     print(failed_to_optimize)

# trial()