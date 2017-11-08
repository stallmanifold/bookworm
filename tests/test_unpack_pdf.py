import unittest
import bookworm.unpack_pdf as unpack_pdf
import bookworm.util       as util
import os, os.path


class TestUnpackPDF(unittest.TestCase):

    def test_unpack_pdf(self):
        """
        UnpackPDF should derive a local directory from the path to the source pdf file.
        """
        source_pdf = './foo/bar/baz/quux.pdf'
        target_dir = f'./foo/bar/baz/{util.default_subdirectory()}'

        action = unpack_pdf.make(source_pdf)

        self.assertEqual(action.image_dir(), target_dir)


    def test_action_setup_should_reject_non_existent_output_directory(self):
        """
        The UnpackPDF class's ``setup`` method should fail when the 
        output directory does not exist.
        """
        source_pdf = 'sample/doesnotexist.pdf'
        target_dir = 'sample/'
        arg_dict = {'input': source_pdf, 'output': target_dir}

        action = unpack_pdf.process_args(arg_dict)

        with self.assertRaises(FileNotFoundError):
            unpack_pdf.Runner.setup(action)


    def test_unpack_pdf_generates_correct_terminal_command(self):
        """
        An ``UnpackPDF`` object should be a valid python subprocess.
        """
        source_pdf = 'sample/sample.pdf'
        target_dir = f'sample/{util.default_subdirectory()}'
        arg_dict = {'input': source_pdf, 'output': target_dir}

        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)

        action = unpack_pdf.process_args(arg_dict)

        terminal_command = [
            'gs', '-q', '-dNOPAUSE', '-dBATCH',   '-sDEVICE=tiff24nc', 
            '-sCompression=lzw',     '-r600x600', 
            f'-sOutputFile={target_dir}_Page_%04d.tiff',
            source_pdf
        ]

        os.rmdir(target_dir)
        
        self.assertEqual(action.as_subprocess(), terminal_command)


class TestUnpackPDFProcessArgs(unittest.TestCase):

    def test_process_args(self):
        """
        The ``UnpackPDF`` class's ``process_args`` method should correctly
        take an input pdf, and create an action that will pass the contents
        of the pdf into a default subdirectory in the same directory as the 
        pdf file.
        """
        source_pdf = 'sample/sample.pdf'
        target_dir = f'sample/{util.default_subdirectory()}'
        arg_dict = {'input': source_pdf, 'output': target_dir}

        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)
        
        action = unpack_pdf.process_args(arg_dict)
        os.rmdir(target_dir)

        self.assertIsInstance(action, unpack_pdf.UnpackPDF)


class TestRunner(unittest.TestCase):

    def test_unpack_pdf_setup(self):
        """
        An UnpackPDF object's setup function should make the target directory
        if it does not exist.
        """
        source_pdf = 'sample/sample.pdf'
        target_dir = f'sample/{util.default_subdirectory()}'
        arg_dict = {'input': source_pdf, 'output': target_dir}

        action = unpack_pdf.process_args(arg_dict)

        try:
            unpack_pdf.Runner.setup(action)
        except FileNotFoundError as e:
            os.rmdir(target_dir)
            self.fail()

        if not os.path.isdir(target_dir):
            os.rmdir(target_dir)
            self.fail()

        os.rmdir(target_dir)

        self.assertEqual(action.target_dir, target_dir)


    def test_unpack_pdf_should_not_write_to_a_directory_with_existing_files(self):
        pass


    def test_unpack_pdf_runner_executes_entire_process(self):
        source_pdf = 'sample/sample.pdf'
        target_dir = f'sample/{util.default_subdirectory()}'
        arg_dict = {'input': source_pdf, 'output': target_dir}

        action = unpack_pdf.process_args(arg_dict)

        try:
            unpack_pdf.Runner.setup(action)
            unpack_pdf.Runner.execute(action)
            unpack_pdf.Runner.commit(action)
        except FileNotFoundError as e:
            os.rmdir(target_dir)
            self.fail()

        os.rmdir(target_dir)

        self.assertEqual(action.target_dir, target_dir)


    def test_unpack_pdf_runner_unpacks_a_pdf_to_a_directory(self):
        source_pdf = 'sample/sample.pdf'
        target_dir = f'sample/{util.default_subdirectory()}'
        arg_dict = {'input': source_pdf, 'output': target_dir}

        action = unpack_pdf.process_args(arg_dict)

        try:
            unpack_pdf.Runner.setup(action)
            unpack_pdf.Runner.execute(action)
            unpack_pdf.Runner.commit(action)
        except FileNotFoundError as e:
            os.rmdir(target_dir)
            self.fail()

        if not os.path.isdir(target_dir):
            os.rmdir(target_dir)
            self.fail()

        os.rmdir(target_dir)

        self.assertEqual(action.target_dir, target_dir)

