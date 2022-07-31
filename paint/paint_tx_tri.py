#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Paint Tx
# GNU Radio version: v3.11.0.0git-181-g643e1337

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
        self.resamp_taps = resamp_taps = firdes.low_pass(2.0, samp_rate, (samp_rate / 2)*0.48,(samp_rate / 2)*0.05, window.WIN_HAMMING, 6.76)
        self.rate = rate = 10
        self.data = data = (0,)*4096
        self.center_freq = center_freq = 923500000

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=2,
                decimation=1,
                taps=resamp_taps,
                fractional_bw=0)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
            rate,
            taps=None,
            flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)
        self.blocks_vector_source_x_0 = blocks.vector_source_c(data, False, 1, [])
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'final.c32', False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.pfb_arb_resampler_xxx_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_resamp_taps(firdes.low_pass(2.0, self.samp_rate, (self.samp_rate / 2)*0.48, (self.samp_rate / 2)*0.05, window.WIN_HAMMING, 6.76))

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

    rows = os.path.getsize("rect.c32") // (8 * 4096)
    f = open("rect.c32", "rb")

    for n in range(rows):
        print(n)
        row = f.read(8 * 4096)
        floats = struct.unpack("f" * (2 * 4096), row)
        samples = []
        for x in range(4096):
            samples.append(complex(floats[2*x], floats[2*x+1]))

        tb.set_data(samples)
        tb.set_rate(100**(n / rows))
        tb.run()

    f.close()



if __name__ == '__main__':
    main()
