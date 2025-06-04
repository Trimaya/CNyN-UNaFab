from enum import Enum, auto
from pathlib import Path

from plasmonitor.spectra import Spectrum


class Spectrometer(Enum):
    """Brands of spectrometers available"""
    BASE = auto()
    AVANTES = auto()


def get_reader_for(spectrometer: Spectrometer, directory: str):
    if spectrometer is None:
        raise ValueError('Spectrometer was not specified')
    if spectrometer not in Spectrometer:
        raise ValueError('Spectrometer not supported')
    if directory is None:
        raise ValueError('A directory was not specified')
    if not Path(directory).is_dir():
        raise ValueError('The directory does not exist')
    if spectrometer is Spectrometer.AVANTES:
        reader = AvantesReader(directory)
    return reader


class AvantesReader:
    def __init__(self, directory):
        self.directory = Path(directory)
        if not ((self.directory / 'UV').is_dir()
                and (self.directory / 'VIS').is_dir()):
            raise ValueError('UV and VIS folders are required')
        self._current_file_index = 1
        self._spectra = None
        self._spectrometer_name = None
        self._spectrometer_brand = Spectrometer.AVANTES

    def _find_file(self, spec_type: str, index: int):
        files = self.directory.glob(
            f'{spec_type}/*_{str(index).zfill(4)}.Raw8.txt')
        file = next(files, None)
        if next(files, None) is not None:
            raise ValueError(
                'Files from more than one spectrometer found!')
        return file

    def _find_files(self, index: int):
        uv_file = self._find_file('UV', index)
        vis_file = self._find_file('VIS', index)
        if index == 1 and (not uv_file or not vis_file):
            raise ValueError('No file found in selected directory')
        if not uv_file and vis_file:
            raise ValueError('UV file not found!')
        if uv_file and not vis_file:
            raise ValueError('VIS file not found!')
        return (uv_file, vis_file)

    @property
    def current_file(self):
        uv_file, vis_file = self._find_files(self._current_file_index)
        return f'UV: {uv_file.name} - VIS: {vis_file.name}'

    def _read_file(self, file, spec_type):
        file_content = file.read_text().strip()
        if not file_content:
            raise ValueError(
                f'Invalid format in {spec_type} file: Empty file!')
        content_lines = file_content.split('\n')
        if len(content_lines) < 8:
            raise ValueError(
                f'Invalid format in {spec_type} file: Too few lines')
        if self._get_spectrometer_name()[spec_type] not in content_lines[3]:
            raise ValueError(
                f'Invalid format in {spec_type} file: Wrong spectrometer name in file')
        columns = [col.strip()
                   for col in content_lines[7].strip(';').split(';')]
        if len(columns) != 4:
            raise ValueError(
                f'Invalid format in {spec_type} file: There should be exactly four data columns')

        return [[float(column.strip())
                 for column in line.strip(';').split(';')[:2]]
                for line in content_lines[7:]]

    def _get_spectrometer_name(self):
        if self._spectrometer_name is None:
            uv_file, vis_file = self._find_files(self._current_file_index)
            uv_name = uv_file.name[:uv_file.name.index('_')]
            vis_name = vis_file.name[:vis_file.name.index('_')]
            self._spectrometer_name = {'UV': uv_name, 'VIS': vis_name}
        return self._spectrometer_name

    @property
    def spectrometer_name(self):
        spectrometer_name = self._get_spectrometer_name()
        return f"UV: {spectrometer_name['UV']} - VIS: {spectrometer_name['VIS']}"

    @property
    def spectrometer_brand(self):
        return self._spectrometer_brand.name

    @property
    def spectra(self):
        def _start_spectra_generator():
            while True:
                uv_file, vis_file = self._find_files(self._current_file_index)
                if not uv_file and not vis_file:
                    self._spectra = None
                    break
                yield Spectrum(self._read_file(uv_file, 'UV') +
                               self._read_file(vis_file, 'VIS'))
                self._current_file_index += 1

        if not self._spectra:
            self._spectra = _start_spectra_generator()
        return self._spectra
