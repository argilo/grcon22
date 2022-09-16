#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Paint Tx
# GNU Radio version: 3.10.4.0

from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.filter import pfb
import os
import struct




class paint_tx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Paint Tx", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2000000
        self.resamp_taps = resamp_taps = firdes.low_pass(8, samp_rate * 8, samp_rate * 0.48,samp_rate * 0.05, window.WIN_HAMMING, 6.76)
        self.rate = rate = 10
        self.noise_amp = noise_amp = 0
        self.data = data = (0,)*4096
        self.center_freq = center_freq = 923500000

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=8,
                decimation=7,
                taps=resamp_taps,
                fractional_bw=0)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
            rate,
            taps=None,
            flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        self.blocks_vector_source_x_0 = blocks.vector_source_c(data, False, 1, [])
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'signal_to_noise.sigmf-data', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise_amp, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.pfb_arb_resampler_xxx_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_resamp_taps(firdes.low_pass(8, self.samp_rate * 8, self.samp_rate * 0.48, self.samp_rate * 0.05, window.WIN_HAMMING, 6.76))

    def get_resamp_taps(self):
        return self.resamp_taps

    def set_resamp_taps(self, resamp_taps):
        self.resamp_taps = resamp_taps
        self.rational_resampler_xxx_0.set_taps(self.resamp_taps)

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate
        self.pfb_arb_resampler_xxx_0.set_rate(self.rate)

    def get_noise_amp(self):
        return self.noise_amp

    def set_noise_amp(self, noise_amp):
        self.noise_amp = noise_amp
        self.analog_noise_source_x_0.set_amplitude(self.noise_amp)

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        self.blocks_vector_source_x_0.set_data(self.data, [])

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq




def main(top_block_cls=paint_tx, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    fft_size = 512

    rows = os.path.getsize("rect.c32") // (8 * fft_size)
    f = open("rect.c32", "rb")

    for n in range(rows):
        print(n)
        row = f.read(8 * fft_size)
        floats = struct.unpack("f" * (2 * fft_size), row)
        samples = []
        for x in range(fft_size):
            samples.append(complex(floats[2*x], floats[2*x+1]))

        tb.set_data(samples)
        tb.set_rate(300**(n / rows))
        tb.set_noise_amp(0 if n < 640 else 1.5 * ((n - 640) / (rows - 640)))
        tb.run()

    f.close()



if __name__ == '__main__':
    main()
