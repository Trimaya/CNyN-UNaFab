import unittest

from plasmonitor.spectra import Spectrum


class SpectrumDataModel(unittest.TestCase):
    INPUT_PAIRS = [(3, 5), (1.3, 4.9), (6.5, 5.7), (2, 8)]

    def test_sort_values_by_wavelength(self):
        expected_values = [(1.3, 4.9), (2, 8), (3, 5), (6.5, 5.7)]
        spectrum = Spectrum(self.INPUT_PAIRS)
        self.assertEqual(spectrum.values, expected_values)

    def test_get_spectrum_intensities(self):
        expected_intensities = [4.9, 8, 5, 5.7]
        spectrum = Spectrum(self.INPUT_PAIRS)
        self.assertEqual(spectrum.intensities(), expected_intensities)

    def test_get_spectrum_wavelengths(self):
        expected_wavelengths = [1.3, 2, 3, 6.5]
        spectrum = Spectrum(self.INPUT_PAIRS)
        self.assertEqual(spectrum.wavelengths, expected_wavelengths)

    def test_interval_out_of_range(self):
        interval = Spectrum(self.INPUT_PAIRS).interval(7, 8)
        self.assertEqual(interval, [])

    def test_interval_inside_bounds(self):
        interval = Spectrum(self.INPUT_PAIRS).interval(1.5, 6)
        self.assertEqual(interval, [(2, 8), (3, 5)])

    def test_interval_includes_bounds(self):
        expected_values = [(1.3, 4.9), (2, 8), (3, 5), (6.5, 5.7)]
        interval = Spectrum(self.INPUT_PAIRS).interval(1.3, 6.5)
        self.assertEqual(interval, expected_values)

    def test_interval_inversed_bounds(self):
        interval = Spectrum(self.INPUT_PAIRS).interval(6, 1.5)
        self.assertEqual(interval, [(2, 8), (3, 5)])

    def test_interval_equal_bounds(self):
        interval = Spectrum(self.INPUT_PAIRS).interval(2, 2)
        self.assertEqual(interval, [(2, 8)])
