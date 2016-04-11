import command
import os.path


class ExpandPageWithFill(command.PageCommand):
    """
    Expand the side of a page by expanding the edges of the page with a fill
    color. This function only does this with the color white.
    """
    def __init__(self, source, target, width, height):
        self.command    = 'convert'
        self.extent     = '-extent {}x{}'.format(width, height)
        self.background = '-background white'
        self.gravity    = '-gravity Center'
        self.source     = source
        self.target     = target
        self.width      = width
        self.height     = height

    def as_python_subprocess(self):
        return [self.command, self.extent, self.background, self.gravity, '\"{}\"'.format(self.source), '\"{}\"'.format(self.target)]

    def as_terminal_command(self):
        quoted_source = '\"{}\"'.format(self.source)
        quoted_target = '\"{}\"'.format(self.target)
        final_arg = '{}[{}x{}]'.format(quoted_target, self.width, self.height)
        
        return \
            '{} {} {} {} {} {}' \
            .format(self.command, self.extent, self.background, self.gravity, quoted_source, final_arg)


def expand_page_with_fill(width, height, source, target=''):
    """
    Expand the side of a page by expanding the edges of the page with a fill
    color. This function only does this with the color white.
    """
    if not target:
        new_target = command.temp_file_name(source)
        return ExpandPageWithFill(source, new_target, width, height)

    return ExpandPageWithFill(source, target, width, height)


def multi_expand_page(width, height, sources, target):
    actions = {}

    for source in sources:
        action = expand_page_with_fill(source, width, height)
        actions[source] = action

    return actions


def process_args(arg_dict):
    try:
        input      = arg_dict['input']
        dimensions = arg_dict['dimensions']
    except KeyError as e:
        raise e

    try: 
        width = dimensions[0]
        height = dimensions[1]

        if width <= 0 or height <= 0:
            raise ValueError('Dimensions must be positive integers: Got {}x{}'.format(width, height))
    except TypeError as e:
        raise e
    except ValueError as e:
        raise e


    if os.path.isfile(input):
        try:
            output = arg_dict['output']
        except KeyError as e:
            # Use input as the target file.
            output = input


        return expand_page_with_fill(width, height, input, output)

    elif os.path.isdir(input):
        try:
            output = arg_dict['output']
        except KeyError as e:
            # Derive output directory from input directory
            output = os.path.join(input, command.default_subdirectory())

        files = command.with_extension('.tiff', input)

        return multi_expand_page(resolution, files, output)

    else:
        raise FileNotFoundError('File or directory does not exist: {}'.format(input))
