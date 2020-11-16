----------
Tutorials
----------

This is the good place to start if you know a tiny bit of Python but very little about G'MIC commands.

If you are in a hurry, you may head to the related `G'MIC Python script <https://github.com/myselfhimself/gmic-py/blob/master/examples/tutorial1-simple-filter-and-io/simple_filter_and_io.py>`_ and run it right away after a `pip install gmic`.

Tutorial 1 - G'MIC commands syntax
####################################################################

Here is a little theory about G'MIC commands signature, commands piping and buffer indexes.
This sounds complicated but is not at all. This tutorial is for very beginner and easy to follow.

Little theory on G'MIC commands
********************************

For this section, you do not need to code or run anything at this point. Just meditate.

G'MIC provides more that 500 commands or filters. Which can get updated from the internet by running the `update` or `up` command.
This spares you from updating your gmic binary runtime frequently. Instead, a definitions file of many G'MIC commands gets refreshed on your machine, downloaded from `gmic.eu <gmic.eu>`_.

G'MIC stores images internally in the x,y,z,c space (or width, height, depth, channels), allowing you to work with 2D greyscale images, 2D color images, or voxels (3D points) for many applications.

For executing expressions, the G'MIC language parser allows you to pipe commands from left to right:

.. code-block::

    <command 1> <command 2> <command 3>

where the result(s) of command 1 is piped as the input of command 2 which outputs in turn to command 3.

In G'MIC each command outputs most of the time a G'MIC Image (or G'MIC Image list if several images are there).

Commands outputting corresponds most of the time to **in-place** transformation within an input images list. Some times (or always when prefixed with a `+` sign, eg. `+blur`), commands can append a new result image to an input images list.

G'MIC commands thus take as input: G'MIC image(s) (or "buffers"), coming from their left side, and also scalar parameters (integers, floats, strings..) on the right side:

.. code-block::

     <former command's output images> <command 1> <command 1 scalar parameters>

Example:

.. code-block::

    input myimage.png blur 3,1

.. gmicpic:: sample earth blur 3,1

The above command will:

1. open `myimage.png` from the G'MIC executable current directory,
2. load it into an G'MIC Images list, which will have 1 item only,
3. then pipe the list as input to the `blur command <https://gmic.eu/reference/blur.html>`_ with parameters `3` (standard deviation) and `1` (Neumann boundary conditions).

From there you will see nothing unless you use the G'MIC command line executable (it pops a display window automatically), so `output <filename>` or `display` are your friends for writing or showing a result window.

Here is a more complex example with more commands piping, where the G'MIC List of 2 G'MIC Images is passed modified in place from left to right:

.. code-block::

    input image1.png image2.png blur 4 sharpen 30 smooth 200 display

You can add a '-' prefix before your G'MIC commands to make them stand out a little more. It changes absolutely nothing for the result.

.. code-block::

    -input image1.png image2.png -blur 4 -sharpen 30 -smooth 200 -display

If you want any command in your chain to use only a subset of the leftside results, use the `[]` index suffix, it will keep the images in your list in place though

.. code-block::

    -input image1.png image2.png blur[1] 3 display[0]

The above command will actually blur `image2.png` but display `image1.png` only, which is not blurred.

Note that G'MIC is a full fledged scripting language, with variables and control flow: `repeat, if condition etc.. <https://gmic.eu/reference/list_of_commands.html#control_flow>`_. You may also create `custom commands or filters <https://github.com/dtschump/gmic-community/wiki/How-to-create-a-custom-filter-in-the-G%E2%80%99mic-plug-in>`_.

The `gmic.eu website technical's reference <https://gmic.eu/reference/>`_ and the `G'MIC community Github repository <https://discuss.pixls.us/c/software/gmic>`_ are good friends to learn and ask about G'MIC.

**Now is the time to learn some very basic foundational commands** for learning and working with G'MIC.

The ``help <some command>`` command
*************************************

.. code-block:: python

    import gmic
    gmic.run("help blur")

    # Outputs
    """


      gmic: GREYC's Magic for Image Computing: command-line interface
            (https://gmic.eu)
            Version 2.9.1

            Copyright (c) 2008-2020, David Tschumperlé / GREYC / CNRS.
            (https://www.greyc.fr)

        blur (+):
            std_deviation>=0[%],_boundary_conditions,_kernel |
            axes,std_deviation>=0[%],_boundary_conditions,_kernel

          Blur selected images by a quasi-gaussian or gaussian filter (recursive implementation).
          (eq. to 'b').

          'boundary_conditions' can be { 0=dirichlet | 1=neumann }.
          'kernel' can be { 0=quasi-gaussian (faster) | 1=gaussian }.
          When specified, argument 'axes' is a sequence of { x | y | z | c }.
          Specifying one axis multiple times apply also the blur multiple times.
          Default values: 'boundary_conditions=1' and 'kernel=0'.

          Example: [#1]  image.jpg +blur 5,0 +blur[0] 5,1

                   [#2]  image.jpg +blur y,10%

          Tutorial: https://gmic.eu/tutorial/_blur.shtml

    """

The ``sample`` or ``sp`` command
*********************************
The ``sample`` or ``sp`` command allows you to load sample images provided by G'MIC. None are pre-downloaded by default.

If you see network errors when running examples for this section, you should change your firewall settings or just skip using the sample command for now.
You may also skip reading to the section about ``input`` instead, which allows you to load your own images.

First pop some ``help`` about the command, and notice how many sample image names you can use as a first parameter.

.. code-block:: python

    import gmic
    gmic.run("help sample") # or "help sp"

    # OUTPUTS
    """
      gmic: GREYC's Magic for Image Computing: command-line interface
            (https://gmic.eu)
            Version 2.9.1

            Copyright (c) 2008-2020, David Tschumperlé / GREYC / CNRS.
            (https://www.greyc.fr)

        sample:
            _name1={ ? | apples | balloons | barbara | boats | bottles | butterfly | \
             cameraman | car | cat | cliff | chick | colorful | david | dog | duck | eagle | \
             elephant | earth | flower | fruits | gmicky | gmicky_mahvin | gmicky_wilber | \
             greece | gummy | house | inside | landscape | leaf | lena | leno | lion | \
             mandrill | monalisa | monkey | parrots | pencils | peppers | portrait0 | \
             portrait1 | portrait2 | portrait3 | portrait4 | portrait5 | portrait6 | \
             portrait7 | portrait8 | portrait9 | roddy | rooster | rose | square | swan | \
             teddy | tiger | tulips | wall | waterfall | zelda },_name2,...,_nameN,_width={ \
             >=0 | 0 (auto) },_height = { >=0 | 0 (auto) } |
            (no arg)

          Input a new sample RGB image (opt. with specified size).
          (eq. to 'sp').

          Argument 'name' can be replaced by an integer which serves as a sample index.

          Example: [#1]  repeat 6 sample done
    """


Let us run the command once, to download an ``apples`` file if not on your computer yet, and loading it into our now empty images buffer:

.. code-block:: python

    import gmic
    gmic.run("sample apples") # A display window would pop up in gmic's command line executable, but not in Python that is intended!

.. gmicpic:: sample apples

The ``display`` command
************************
The display command is twofolds:
- it displays textual information about an image,
- if the environment (operating system, terminal, IPython-like shell...) allows it, tries to show the image in some G'MIC image window, matplotlib view etc..

.. code-block:: python

    import gmic
    gmic.run("sample apples display") # This will pop up a display window showing your image, without it needing to be saved anyway on your drive
    gmic.run("sample duck sample apples display[0]") # Same but will show only index 0 image, ie. the duck

    # OUTPUTS
    """
    [gmic]-1./ Display image [0] = 'apples', from point (320,200,0).
    [0] = 'apples':
      size = (640,400,1,3) [3000 Kio of floats].
      data = (20,22,20,20,20,22,22,22,22,22,22,20,(...),1,1,1,1,1,1,1,1,1,1,1,1).
      min = 1, max = 250, mean = 58.5602, std = 59.8916, coords_min = (317,306,0,1), coords_max = (430,135,0,0).
    [gmic]-2./ Display image [0] = 'duck', from point (320,240,0).
    [0] = 'duck':
      size = (640,480,1,3) [3600 Kio of floats].
      data = (89,89,74,89,89,89,74,89,89,89,89,89,(...),177,190,177,215,181,194,206,201,153,201,161,209).
      min = 1, max = 253, mean = 125.444, std = 57.4846, coords_min = (364,72,0,2), coords_max = (413,123,0,0).
    """

.. gmicpic:: sample apples

.. gmicpic:: sample duck

The ``print`` command
************************

This command is similar to the ``display`` command except that it shows no picture, it just outputs text.

.. code-block:: python

    import gmic
    gmic.run("sp leno print")

    # OUTPUTS
    """
    [gmic]-1./ Print image [0] = 'leno'.
    [0] = 'leno':
      size = (512,512,1,3) [3072 Kio of floats].
      data = (224,224,223,224,224,225,224,224,224,224,224,224,(...),69,85,85,79,87,79,85,90,77,77,79,84).
      min = 1, max = 255, mean = 128.318, std = 58.3599, coords_min = (508,71,0,1), coords_max = (124,189,0,0).
    """

The `output <file>` command
********************************

This command writes your images list's contents to files, using file extension detection.

.. code-block:: python

    import gmic
    gmic.run("sample earth output myearth.png") # outputs the result of the earth sample to a path you want (.png, .jpeg, .tiff, .bmp, .pbm and more are supported)
    gmic.run("sample earth elephant output mysamples.jpeg") # outputs the result to mysamples_NNNN.jpeg
    gmic.run("sample earth elephant output[1] myelephant.jpeg") # outputs the second image (index 1, starting at 0) to a single JPEG file

The ``input <somefile>`` command (simple and short form)
*********************************************************

This command fills your image(s) list with the contents of files.
Note that G'MIC `may also allows to open video files directly <https://gmic.eu/reference/list_of_commands.html#image_sequences_and_videos>`_, especially if OpenCV is linked, although the official gmic-py release does not link to OpenCV.

.. code-block:: python

    import gmic

    # LOADING AND SHOWING A SINGLE IMAGE
    gmic.run("input myearth.png display") # opens myearth.png and then trying a display
    gmic.run("myearth.png display") # here is the short form, where 'input' can be omitted. Note that the 'display' command is not obligatory, it is left for you as a proof that it works.

    # LOADING AND SAVING MULTIPLE IMAGES
    gmic.run("sample earth sample apples output myimages.png display") # saves to myimages_000000.png  myimages_000001.png. The display command is optional.
    gmic.run("myimages_000000.png  myimages_000001.png display") # loads myimages_000000.png  myimages_000001.png and displays them. Note the 'input' command name was omitted.

Applying a one or more filter(s)
*********************************
Filtering images is what G'MIC is good at, and especially what most users do with G'MIC.

Official filters and commands are listed at: https://gmic.eu/reference/, especially `in the Filtering section <https://gmic.eu/reference/list_of_commands.html#filtering>`_.

The G'MIC QT plug-in for GIMP and other graphic software provide more filters, which usually wrap those official filters and have internal layer management specificities.
If you use the latter (they are usually prefixed in ``fx_`` or ``gimp_`` or ``gui_``, beware their community authors do not always care about stability or allowing the same parameters' order or meaning!
A `Gist file explains this in more technical detail <https://gist.github.com/myselfhimself/1eba99d5317190aa04cf65c06d4ebe35>`_ if you are very curious.

To get inspiration for commands to run, you may also head to the `G'MIC gallery <https://gmic.eu/gallery/>`_ and click the images to see corresponding commands.

Here are some example commands and filters:

.. code-block:: python

    import gmic
    gmic.run("sample apples blur 4 display") # blur's documentation with a nice preview is also at https://gmic.eu/reference/blur.html not just through the "help blur" command

.. gmicpic:: sample apples blur 4

.. code-block:: python

    import gmic
    gmic.run("sample apples rodilius 10 display") # more at https://gmic.eu/reference/rodilius.html

.. gmicpic:: sample apples rodilius 10

.. code-block:: python

    # SELECTING IMAGES BY INDEX
    import gmic
    gmic.run("sample apples sample earth blur[1] 4 display") # Here the blur was applied only to image with second position

.. gmicpic:: sample apples sample earth blur[1] 4 keep[1]

.. code-block:: python

    import gmic
    # APPLYING THE FAMOUS 'STYLIZE' STYLE TRANSFER FILTER
    gmic.run("sp leno display") # this is the portrait we will want to be stylized
    gmic.run("_fx_stylize landscapenearantwerp display") # let us be hackish and use the internal _fx_stylize function to preview one of Antwerp's painting as a future style

    gmic.run("sample leno _fx_stylize landscapenearantwerp +stylize . keep[2] display")
    # the keep[index] command allows to remove all images in Gmic Image list but the 'index' one
    # The + sign in front stylize forces the filter to append its result
    # image to the end of the Gmic Image list, instead of filtering in place
    # The . stands for "default" value

.. gmicpic:: sp leno

.. gmicpic:: _fx_stylize landscapenearantwerp

.. gmicpic:: sample leno _fx_stylize landscapenearantwerp +stylize . keep[2]

.. code-block:: python

    # APPLYING MULTIPLE FILTERS
    # ONCE
    gmic.run("sample duck smooth 40,0,1,1,2 display")
    # 3 TIMES
    gmic.run("sample duck repeat 3 smooth 40,0,1,1,2 done display")
    # SEVERAL FILTERS IN A ROW
    gmic.run("sample duck repeat 3 smooth 40,0,1,1,2 done blur xy,5 rodilius , display")

.. gmicpic:: sample duck smooth 40,0,1,1,2

.. gmicpic:: sample duck repeat 3 smooth 40,0,1,1,2 done blur xy,5 rodilius ,