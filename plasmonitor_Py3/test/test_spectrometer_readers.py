"""Basic tests for spectrometer readers"""
from pathlib import Path
import unittest
import shutil

from plasmonitor.spectrometers import get_reader_for, Spectrometer


class GetSpectrometerReader(unittest.TestCase):
    def test_spectrometer_is_not_specified(self):
        with self.assertRaisesRegex(ValueError, 'Spectrometer was not specified'):
            get_reader_for(None, '')

    def test_spectrometer_is_not_supported(self):
        with self.assertRaisesRegex(ValueError, 'Spectrometer not supported'):
            get_reader_for('', '')

    def test_directory_is_not_specified(self):
        with self.assertRaisesRegex(ValueError, 'A directory was not specified'):
            get_reader_for(Spectrometer.BASE, None)

    def test_directory_does_not_exist(self):
        with self.assertRaisesRegex(ValueError, 'The directory does not exist'):
            get_reader_for(Spectrometer.BASE, 'invalid_directory')


class ReadFromAvantesSpectrometer(unittest.TestCase):
    ROOT_PATH = Path('test/avantes')
    @classmethod
    def setUpClass(cls):
        cls.ROOT_PATH.mkdir()

    @classmethod
    def tearDownClass(cls):
        cls.ROOT_PATH.rmdir()

    def setUp(self):
        self.paths = PathManagerFixture(self.ROOT_PATH.resolve())

    def tearDown(self):
        self.paths.clear()

    def test_invalid_directory_structure(self):
        with self.assertRaisesRegex(ValueError, 'UV and VIS folders are required'):
            get_reader_for(Spectrometer.AVANTES, 'test/avantes')

    def test_first_file_not_found(self):
        """First file not found throws an error"""
        self.paths.create_dirs('UV', 'VIS')
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        with self.assertRaisesRegex(ValueError, 'No file found in selected directory'):
            next(reader.spectra)

    def test_files_from_different_spectrometers_found_in_uv(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'UV/1703146U2_0001.Raw8.txt').write_text('')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt').write_text('')
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        with self.assertRaisesRegex(ValueError, 'Files from more than one spectrometer found!'):
            next(reader.spectra)

    def test_files_from_different_spectrometers_found_in_vis(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'VIS/1703147U2_0001.Raw8.txt').write_text('')
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt').write_text('')
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        with self.assertRaisesRegex(ValueError, 'Files from more than one spectrometer found!'):
            next(reader.spectra)

    def test_get_spectrometer_brand(self):
        self.paths.create_dirs('UV', 'VIS')
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        self.assertEqual(reader.spectrometer_brand, 'AVANTES')

    def test_get_spectrometer_name(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1703147U2'))
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704147U2'))
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        self.assertEqual(reader.spectrometer_name,
                         'UV: 1704146U2 - VIS: 1704147U2')

    def test_read_empty_file_uv(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt').write_text('')
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt').write_text('')
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        with self.assertRaisesRegex(ValueError, 'Invalid format in UV file: Empty file!'):
            next(reader.spectra)

    def test_read_empty_file_vis(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704146U2'))
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt').write_text('')
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        with self.assertRaisesRegex(ValueError, 'Invalid format in VIS file: Empty file!'):
            next(reader.spectra)

    def test_read_file_with_too_few_lines_uv(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt') \
            .write_text('\n'.join(get_avantes_file('1704146U2')
                                  .splitlines()[:6]))
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704147U2'))
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        with self.assertRaisesRegex(ValueError, 'Invalid format in UV file: Too few lines'):
            next(reader.spectra)

    def test_read_file_with_too_few_lines_vis(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704146U2'))
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt') \
            .write_text('\n'.join(get_avantes_file('1704147U2')
                                  .splitlines()[:6]))
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        with self.assertRaisesRegex(ValueError, 'Invalid format in VIS file: Too few lines'):
            next(reader.spectra)

    def test_read_file_with_incorrect_spectrometer_name_uv(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704146U2').replace('1704146U2', '1704156U2'))
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704147U2'))
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        with self.assertRaisesRegex(ValueError,
                                    'Invalid format in UV file: Wrong spectrometer name'):
            next(reader.spectra)

    def test_read_file_with_incorrect_spectrometer_name_vis(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704146U2'))
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704147U2').replace('1704147U2', '1704157U2'))
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        with self.assertRaisesRegex(ValueError,
                                    'Invalid format in VIS file: Wrong spectrometer name'):
            next(reader.spectra)

    def test_read_file_with_incorrect_column_count_uv(self):
        self.paths.create_dirs('UV', 'VIS')
        uv_content = get_avantes_file('1704146U2')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt') \
            .write_text(uv_content[:uv_content.rfind(';')])
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704147U2'))
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        with self.assertRaisesRegex(ValueError,
                                    'Invalid format in UV file: There should be exactly four data columns'):
            next(reader.spectra)

    def test_read_file_with_incorrect_column_count_vis(self):
        self.paths.create_dirs('UV', 'VIS')
        vis_content = get_avantes_file('1704147U2')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704146U2'))
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt') \
            .write_text(vis_content[:vis_content.rfind(';')])
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        with self.assertRaisesRegex(ValueError,
                                    'Invalid format in VIS file: There should be exactly four data columns'):
            next(reader.spectra)

    def test_uv_file_not_found_on_subsequent_reads(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704146U2'))
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704147U2'))
        (self.ROOT_PATH / 'VIS/1704147U2_0002.Raw8.txt') \
            .write_text(get_avantes_file('1704147U2'))
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        next(reader.spectra)
        with self.assertRaisesRegex(ValueError, 'UV file not found!'):
            next(reader.spectra)

    def test_vis_file_not_found_on_subsequent_reads(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704146U2'))
        (self.ROOT_PATH / 'UV/1704146U2_0002.Raw8.txt') \
            .write_text(get_avantes_file('1704146U2'))
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704147U2'))
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        next(reader.spectra)
        with self.assertRaisesRegex(ValueError, 'VIS file not found!'):
            next(reader.spectra)

    def test_read_first_spectrum(self):
        self.paths.create_dirs('UV', 'VIS')
        (self.ROOT_PATH / 'UV/1704146U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704146U2'))
        (self.ROOT_PATH / 'VIS/1704147U2_0001.Raw8.txt') \
            .write_text(get_avantes_file('1704147U2'))
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        spectrum = next(reader.spectra)
        self.assertIsNotNone(spectrum)

    def test_read_second_spectrum(self):
        self.paths.create_dirs('UV', 'VIS')
        for i in range(1, 3):
            (self.ROOT_PATH / f'UV/1704146U2_000{i}.Raw8.txt') \
                .write_text(get_avantes_file('1704146U2'))
            (self.ROOT_PATH / f'VIS/1704147U2_000{i}.Raw8.txt') \
                .write_text(get_avantes_file('1704147U2'))
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        for _ in range(2):
            spectrum = next(reader.spectra)
        self.assertIsNotNone(spectrum)

    def test_read_no_spectra_left(self):
        self.paths.create_dirs('UV', 'VIS')
        for i in range(1, 3):
            (self.ROOT_PATH / f'UV/1704146U2_000{i}.Raw8.txt') \
                .write_text(get_avantes_file('1704146U2'))
            (self.ROOT_PATH / f'VIS/1704147U2_000{i}.Raw8.txt') \
                .write_text(get_avantes_file('1704147U2'))
        reader = get_reader_for(Spectrometer.AVANTES, 'test/avantes')
        for _ in range(2):
            next(reader.spectra)
        with self.assertRaises(StopIteration):
            next(reader.spectra)


class PathManagerFixture:
    def __init__(self, root_path: str):
        self.root = Path(root_path)
        self.files = []

    def create_dirs(self, *paths):
        for path in paths:
            (self.root / path).mkdir()

    def clear(self):
        for path in self.root.iterdir():
            if path.is_dir:
                shutil.rmtree(path.resolve())
            elif path.is_file:
                path.unlink()


def get_avantes_file(spectrometer_name: str):
    return f"""

    Integration time [ms]: 500.000
    Averaging Nr. [scans]: 2
    Smoothing Nr. [pixels]: 0
    Data measured with spectrometer [name]: {spectrometer_name}
    Wave   ;Sample   ;Dark     ;Reference;Scope
    [nm]   ;[counts] ;[counts] ;[counts]

    1.002; -1.002;    0.000;    0.000
    """
