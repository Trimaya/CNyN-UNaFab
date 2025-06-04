
"""Spectra related concepts"""


class Line:
    def __init__(self, name, center, width):
        self.name = name
        self.center = center
        self.width = width

    @property
    def interval(self):
        half_width = self.width / 2.0
        return (self.center - half_width, self.center + half_width)


class Spectrum:
    """Defines a collection of wavelength-intensity pairs"""

    def __init__(self, pairs):
        self.pairs = sorted(pairs, key=lambda pair: pair[0])

    def intensities(self, interval=None):
        pairs = self.interval(
            interval[0], interval[1]) if interval else self.pairs
        return [pair[1] for pair in pairs]

    def interval(self, start: float, end: float):
        lower = start if start <= end else end
        upper = end if start <= end else start
        return [pair for pair in self.pairs
                if lower <= pair[0] and pair[0] <= upper]

    @property
    def values(self):
        return [pair for pair in self.pairs]

    @property
    def wavelengths(self):
        return [pair[0] for pair in self.pairs]
