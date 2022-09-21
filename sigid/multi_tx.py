#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Multi Tx
# GNU Radio version: 3.10.4.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from rds_tx import rds_tx  # grc-generated hier_block
import ham
import math
import morse_table



from gnuradio import qtgui

class multi_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Multi Tx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Multi Tx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "multi_tx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.audio_rate = audio_rate = 48000
        self.samp_rate = samp_rate = audio_rate * 20
        self.wpm = wpm = 8
        self.resamp_taps = resamp_taps = firdes.low_pass(samp_rate // audio_rate, samp_rate, audio_rate / 2,audio_rate / 20, window.WIN_HAMMING, 6.76)
        self.m17_deviation = m17_deviation = 800
        self.interpolation_rate = interpolation_rate = samp_rate // 4800
        self.center_freq = center_freq = 441000000

        ##################################################
        # Blocks
        ##################################################
        self.root_raised_cosine_filter_1 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                audio_rate,
                5,
                0.35,
                200))
        self.root_raised_cosine_filter_0_0 = filter.interp_fir_filter_fff(
            interpolation_rate,
            firdes.root_raised_cosine(
                interpolation_rate,
                interpolation_rate,
                1,
                0.5,
                (interpolation_rate*11+1)))
        self.root_raised_cosine_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.root_raised_cosine(
                1,
                audio_rate,
                5,
                0.35,
                200))
        self.rds_tx_0 = rds_tx()
        self.rational_resampler_xxx_3 = filter.rational_resampler_ccc(
                interpolation=192,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_2 = filter.rational_resampler_ccc(
                interpolation=(samp_rate // audio_rate),
                decimation=1,
                taps=resamp_taps,
                fractional_bw=0)
        self.rational_resampler_xxx_1_1 = filter.rational_resampler_ccc(
                interpolation=(samp_rate // audio_rate // 2),
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1_0 = filter.rational_resampler_ccc(
                interpolation=(samp_rate // audio_rate // 2),
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=(samp_rate // audio_rate // 2),
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_ccc(
                interpolation=(samp_rate // 38400),
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.9, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            audio_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            8192, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_1 = filter.interp_fir_filter_ccf(
            1,
            firdes.low_pass(
                0.5,
                audio_rate,
                5000,
                400,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_1 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                audio_rate,
                12500,
                5000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                audio_rate,
                12500,
                5000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                audio_rate,
                12500,
                5000,
                window.WIN_HAMMING,
                6.76))
        self.ham_varicode_tx_0 = ham.varicode_tx()
        self.digital_psk_mod_0 = digital.psk.psk_mod(
            constellation_points=2,
            mod_code="none",
            differential=True,
            samples_per_symbol=8,
            excess_bw=0.35,
            verbose=False,
            log=False)
        self.digital_map_bb_0 = digital.map_bb([1,0])
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bf([+1.0,+3.0,-1.0,-3.0], 1)
        self.blocks_wavfile_source_1_1 = blocks.wavfile_source('sstv-pad.wav', False)
        self.blocks_wavfile_source_1_0 = blocks.wavfile_source('flag2-3-pad.wav', True)
        self.blocks_wavfile_source_1 = blocks.wavfile_source('flag1-pad.wav', True)
        self.blocks_wavfile_source_0_1_0 = blocks.wavfile_source('flag6-pad.wav', True)
        self.blocks_wavfile_source_0_1 = blocks.wavfile_source('flag7-pad.wav', True)
        self.blocks_wavfile_source_0_0 = blocks.wavfile_source('aprs-pad.wav', True)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('flag5-pad.wav', True)
        self.blocks_vector_source_x_2_0 = blocks.vector_source_c((1,0,0,0,0), True, 1, [])
        self.blocks_vector_source_x_2 = blocks.vector_source_c((1,0,0,0,0), True, 1, [])
        self.blocks_vector_source_x_1 = blocks.vector_source_b([ord(c) for c in "This is VE3IRR. Signal identification challenge #11: flag{no_31_b4uD_i5_en0ugH}\n"], True, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_c((0,)*90 + morse_table.morse_seq("This is VE3IRR   -   For signal identification challenge 8 the flag is itelilelcsemzpcc") + (0,)*91, True, 1, [])
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_rotator_cc_2_0_0_0_0 = blocks.rotator_cc((-20e3 * 2 * math.pi / audio_rate), False)
        self.blocks_rotator_cc_2_0_0_0 = blocks.rotator_cc((12e3 * 2 * math.pi / audio_rate), False)
        self.blocks_rotator_cc_2_0_0 = blocks.rotator_cc((-14e3 * 2 * math.pi / audio_rate), False)
        self.blocks_rotator_cc_2_0 = blocks.rotator_cc((20e3 * 2 * math.pi / audio_rate), False)
        self.blocks_rotator_cc_2 = blocks.rotator_cc((0e3 * 2 * math.pi / audio_rate), False)
        self.blocks_rotator_cc_1_2 = blocks.rotator_cc((-400e3 * 2 * math.pi / samp_rate), False)
        self.blocks_rotator_cc_1_1_0_0 = blocks.rotator_cc((300e3 * 2 * math.pi / samp_rate), False)
        self.blocks_rotator_cc_1_1_0 = blocks.rotator_cc((-100e3 * 2 * math.pi / samp_rate), False)
        self.blocks_rotator_cc_1_1 = blocks.rotator_cc((-200e3 * 2 * math.pi / samp_rate), False)
        self.blocks_rotator_cc_1_0 = blocks.rotator_cc((400e3 * 2 * math.pi / samp_rate), False)
        self.blocks_rotator_cc_1 = blocks.rotator_cc((-300e3 * 2 * math.pi / samp_rate), False)
        self.blocks_rotator_cc_0 = blocks.rotator_cc((100e3 * 2 * math.pi / samp_rate), False)
        self.blocks_repeat_1_0 = blocks.repeat(gr.sizeof_gr_complex*1, 57600)
        self.blocks_repeat_1 = blocks.repeat(gr.sizeof_gr_complex*1, (48000*2))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, (int(1.2 * audio_rate / wpm)))
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, 2, "", False, gr.GR_MSB_FIRST)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.11)
        self.blocks_float_to_complex_0_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_1 = blocks.file_source(gr.sizeof_char*1, 'pocsag-pad.dat', True, 0, 0)
        self.blocks_file_source_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, 'flag9.bin', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'sigid.sigmf-data', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_xx_1 = blocks.add_vcc(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_cc(0.5)
        self.band_pass_filter_0_0 = filter.interp_fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                5,
                audio_rate,
                (-2800),
                (-200),
                200,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.interp_fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                5,
                audio_rate,
                200,
                2800,
                200,
                window.WIN_HAMMING,
                6.76))
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, (1e-1), 0)
        self.analog_nbfm_tx_0_1 = analog.nbfm_tx(
        	audio_rate=audio_rate,
        	quad_rate=(audio_rate * 2),
        	tau=(75e-6),
        	max_dev=5e3,
        	fh=(-1.0),
                )
        self.analog_nbfm_tx_0_0 = analog.nbfm_tx(
        	audio_rate=audio_rate,
        	quad_rate=(audio_rate * 2),
        	tau=(75e-6),
        	max_dev=5e3,
        	fh=(-1.0),
                )
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=audio_rate,
        	quad_rate=(audio_rate * 2),
        	tau=(75e-6),
        	max_dev=5e3,
        	fh=(-1.0),
                )
        self.analog_frequency_modulator_fc_0_0 = analog.frequency_modulator_fc((m17_deviation * 2 * math.pi / samp_rate))
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc((2.0 * math.pi * 4500 / 38400))


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_frequency_modulator_fc_0_0, 0), (self.blocks_rotator_cc_1_1_0, 0))
        self.connect((self.analog_nbfm_tx_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.analog_nbfm_tx_0_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.analog_nbfm_tx_0_1, 0), (self.low_pass_filter_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 7))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_rotator_cc_2_0_0, 0))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_rotator_cc_2_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_rotator_cc_2, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.blocks_add_xx_1, 0), (self.rational_resampler_xxx_2, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.blocks_file_source_1, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.blocks_float_to_complex_0_0_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.rational_resampler_xxx_1_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.root_raised_cosine_filter_1, 0))
        self.connect((self.blocks_repeat_1, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_repeat_1_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_rotator_cc_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_rotator_cc_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_rotator_cc_1_0, 0), (self.blocks_add_xx_0, 4))
        self.connect((self.blocks_rotator_cc_1_1, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_rotator_cc_1_1_0, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.blocks_rotator_cc_1_1_0_0, 0), (self.blocks_add_xx_0, 5))
        self.connect((self.blocks_rotator_cc_1_2, 0), (self.blocks_add_xx_0, 6))
        self.connect((self.blocks_rotator_cc_2, 0), (self.blocks_add_xx_1, 0))
        self.connect((self.blocks_rotator_cc_2_0, 0), (self.blocks_add_xx_1, 1))
        self.connect((self.blocks_rotator_cc_2_0_0, 0), (self.blocks_add_xx_1, 2))
        self.connect((self.blocks_rotator_cc_2_0_0_0, 0), (self.blocks_add_xx_1, 3))
        self.connect((self.blocks_rotator_cc_2_0_0_0_0, 0), (self.blocks_add_xx_1, 4))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_psk_mod_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_vector_source_x_1, 0), (self.ham_varicode_tx_0, 0))
        self.connect((self.blocks_vector_source_x_2, 0), (self.blocks_repeat_1, 0))
        self.connect((self.blocks_vector_source_x_2_0, 0), (self.blocks_repeat_1_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_wavfile_source_0_0, 0), (self.analog_nbfm_tx_0_0, 0))
        self.connect((self.blocks_wavfile_source_0_1, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.blocks_wavfile_source_0_1_0, 0), (self.blocks_float_to_complex_0_0_0, 0))
        self.connect((self.blocks_wavfile_source_1, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.blocks_wavfile_source_1_0, 0), (self.rds_tx_0, 0))
        self.connect((self.blocks_wavfile_source_1_0, 1), (self.rds_tx_0, 1))
        self.connect((self.blocks_wavfile_source_1_1, 0), (self.analog_nbfm_tx_0_1, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.root_raised_cosine_filter_0_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.digital_psk_mod_0, 0), (self.rational_resampler_xxx_3, 0))
        self.connect((self.ham_varicode_tx_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_1_1, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_rotator_cc_1_1_0_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_rotator_cc_1, 0))
        self.connect((self.rational_resampler_xxx_1_0, 0), (self.blocks_rotator_cc_1_1, 0))
        self.connect((self.rational_resampler_xxx_1_1, 0), (self.blocks_rotator_cc_1_2, 0))
        self.connect((self.rational_resampler_xxx_2, 0), (self.blocks_rotator_cc_1_0, 0))
        self.connect((self.rational_resampler_xxx_3, 0), (self.blocks_rotator_cc_2_0_0_0_0, 0))
        self.connect((self.rds_tx_0, 0), (self.blocks_rotator_cc_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_rotator_cc_2_0_0_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.analog_frequency_modulator_fc_0_0, 0))
        self.connect((self.root_raised_cosine_filter_1, 0), (self.root_raised_cosine_filter_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "multi_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_audio_rate(self):
        return self.audio_rate

    def set_audio_rate(self, audio_rate):
        self.audio_rate = audio_rate
        self.set_resamp_taps(firdes.low_pass(self.samp_rate // self.audio_rate, self.samp_rate, self.audio_rate / 2, self.audio_rate / 20, window.WIN_HAMMING, 6.76))
        self.set_samp_rate(self.audio_rate * 20)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(5, self.audio_rate, 200, 2800, 200, window.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(5, self.audio_rate, (-2800), (-200), 200, window.WIN_HAMMING, 6.76))
        self.blocks_repeat_0.set_interpolation((int(1.2 * self.audio_rate / self.wpm)))
        self.blocks_rotator_cc_2.set_phase_inc((0e3 * 2 * math.pi / self.audio_rate))
        self.blocks_rotator_cc_2_0.set_phase_inc((20e3 * 2 * math.pi / self.audio_rate))
        self.blocks_rotator_cc_2_0_0.set_phase_inc((-14e3 * 2 * math.pi / self.audio_rate))
        self.blocks_rotator_cc_2_0_0_0.set_phase_inc((12e3 * 2 * math.pi / self.audio_rate))
        self.blocks_rotator_cc_2_0_0_0_0.set_phase_inc((-20e3 * 2 * math.pi / self.audio_rate))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.audio_rate, 12500, 5000, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.audio_rate, 12500, 5000, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.audio_rate, 12500, 5000, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(0.5, self.audio_rate, 5000, 400, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.audio_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.audio_rate, 5, 0.35, 200))
        self.root_raised_cosine_filter_1.set_taps(firdes.root_raised_cosine(1, self.audio_rate, 5, 0.35, 200))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_interpolation_rate(self.samp_rate // 4800)
        self.set_resamp_taps(firdes.low_pass(self.samp_rate // self.audio_rate, self.samp_rate, self.audio_rate / 2, self.audio_rate / 20, window.WIN_HAMMING, 6.76))
        self.analog_frequency_modulator_fc_0_0.set_sensitivity((self.m17_deviation * 2 * math.pi / self.samp_rate))
        self.blocks_rotator_cc_0.set_phase_inc((100e3 * 2 * math.pi / self.samp_rate))
        self.blocks_rotator_cc_1.set_phase_inc((-300e3 * 2 * math.pi / self.samp_rate))
        self.blocks_rotator_cc_1_0.set_phase_inc((400e3 * 2 * math.pi / self.samp_rate))
        self.blocks_rotator_cc_1_1.set_phase_inc((-200e3 * 2 * math.pi / self.samp_rate))
        self.blocks_rotator_cc_1_1_0.set_phase_inc((-100e3 * 2 * math.pi / self.samp_rate))
        self.blocks_rotator_cc_1_1_0_0.set_phase_inc((300e3 * 2 * math.pi / self.samp_rate))
        self.blocks_rotator_cc_1_2.set_phase_inc((-400e3 * 2 * math.pi / self.samp_rate))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_wpm(self):
        return self.wpm

    def set_wpm(self, wpm):
        self.wpm = wpm
        self.blocks_repeat_0.set_interpolation((int(1.2 * self.audio_rate / self.wpm)))

    def get_resamp_taps(self):
        return self.resamp_taps

    def set_resamp_taps(self, resamp_taps):
        self.resamp_taps = resamp_taps
        self.rational_resampler_xxx_2.set_taps(self.resamp_taps)

    def get_m17_deviation(self):
        return self.m17_deviation

    def set_m17_deviation(self, m17_deviation):
        self.m17_deviation = m17_deviation
        self.analog_frequency_modulator_fc_0_0.set_sensitivity((self.m17_deviation * 2 * math.pi / self.samp_rate))

    def get_interpolation_rate(self):
        return self.interpolation_rate

    def set_interpolation_rate(self, interpolation_rate):
        self.interpolation_rate = interpolation_rate
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(self.interpolation_rate, self.interpolation_rate, 1, 0.5, (self.interpolation_rate*11+1)))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq




def main(top_block_cls=multi_tx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
