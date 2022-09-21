#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Pocsag
# GNU Radio version: 3.10.4.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import gnuradio.mixalot as mixalot




class pocsag(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Pocsag", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.mixalot_pocencode_0 = mixalot.pocencode(1, 1200, 123456, 'Signal identification challenge #12: flag{b4cK_to_pag3_0n3}', 38400)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'pocsag.dat', False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.mixalot_pocencode_0, 0), (self.blocks_file_sink_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=pocsag, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
