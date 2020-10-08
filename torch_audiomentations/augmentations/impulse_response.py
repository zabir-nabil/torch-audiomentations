import random

import torch

from ..core.transforms_interface import BaseWaveformTransform, EmptyPathException
from ..utils.convolution import convolve
from ..utils.file import find_audio_files, load_audio


class ApplyImpulseResponse(BaseWaveformTransform):
    """
    Convolves an input signal with an impulse response.
    """

    def __init__(
        self, ir_path, device=torch.device("cpu"), convolve_mode="full", p=0.5
    ):
        # TODO: infer device from the given samples instead
        super(ApplyImpulseResponse, self).__init__(p)

        self.ir_path = find_audio_files(ir_path)

        if len(self.ir_path) == 0:
            raise EmptyPathException("There are no supported audio files found.")

        self.convolve_mode = convolve_mode
        self.device = device

    def randomize_parameters(self, samples, sample_rate: int):
        super(ApplyImpulseResponse, self).randomize_parameters(samples, sample_rate)
        if self.parameters["should_apply"] and samples.size(0) > 0:
            ir_paths = random.choices(self.ir_path, k=samples.size(0))
            ir_sounds = []
            max_ir_sound_length = 0
            for ir_path in ir_paths:
                ir_samples = load_audio(ir_path, sample_rate)
                num_samples = len(ir_samples)
                if num_samples > max_ir_sound_length:
                    max_ir_sound_length = num_samples
                ir_samples = torch.from_numpy(ir_samples)
                ir_sounds.append(ir_samples)
            for i in range(len(ir_sounds)):
                placeholder = torch.zeros(
                    size=(max_ir_sound_length,), dtype=torch.float32
                )
                placeholder[0 : len(ir_sounds[i])] = ir_sounds[i]
                ir_sounds[i] = placeholder
            self.parameters["ir_sounds"] = torch.stack(ir_sounds)

    def apply_transform(self, selected_samples, sample_rate: int):
        selected_samples = selected_samples.to(self.device)
        ir = self.parameters["ir_sounds"].to(self.device)
        return convolve(selected_samples, ir, mode=self.convolve_mode)
