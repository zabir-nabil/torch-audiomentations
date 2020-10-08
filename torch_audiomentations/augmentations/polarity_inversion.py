from ..core.transforms_interface import BaseWaveformTransform


class PolarityInversion(BaseWaveformTransform):
    """
    Flip the audio samples upside-down, reversing their polarity. In other words, multiply the
    waveform by -1, so negative values become positive, and vice versa. The result will sound
    the same compared to the original when played back in isolation. However, when mixed with
    other audio sources, the result may be different. This waveform inversion technique
    is sometimes used for audio cancellation or obtaining the difference between two waveforms.
    However, in the context of audio data augmentation, this transform can be useful when
    training phase-aware machine learning models.
    """

    supports_multichannel = True

    def __init__(self, p: float = 0.5):
        """
        :param p:
        """
        super().__init__(p)

    def randomize_parameters(self, samples, sample_rate: int):
        super().randomize_parameters(samples, sample_rate)

    def apply_transform(self, selected_samples, sample_rate: int):
        return -selected_samples
